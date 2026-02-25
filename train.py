"""
EntropyHunter — Qwen2.5-7B LoRA Fine-Tuning

Uses Unsloth for 2x faster training with 60% less memory.

Usage:
    python train.py                          # Default settings
    python train.py --epochs 5               # More epochs
    python train.py --push-to-hub kemal/entropy-hunter-7b   # Push to HF
"""

import argparse
import json
import os
from pathlib import Path


def main(args):
    # ============================================================
    # Step 1: Load model with Unsloth (4-bit quantized for LoRA)
    # ============================================================
    from unsloth import FastLanguageModel

    print("🔥 Loading Qwen2.5-7B...")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Qwen2.5-7B-Instruct",  # Unsloth optimized
        max_seq_length=args.max_seq_length,
        dtype=None,      # auto-detect (float16 on L4)
        load_in_4bit=True,  # 4-bit quantization for LoRA training
    )

    print(f"   Model loaded. Max seq length: {args.max_seq_length}")

    # ============================================================
    # Step 2: Configure LoRA adapters
    # ============================================================
    print("🔧 Configuring LoRA...")

    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_r,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",  # attention
            "gate_proj", "up_proj", "down_proj",       # MLP
        ],
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        bias="none",
        use_gradient_checkpointing="unsloth",  # 30% less VRAM
        random_state=42,
    )

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"   Trainable: {trainable:,} / {total:,} ({trainable/total*100:.2f}%)")

    # ============================================================
    # Step 3: Load dataset (ChatML format)
    # ============================================================
    print("📚 Loading dataset...")

    from datasets import load_dataset

    dataset = load_dataset("json", data_files={
        "train": args.train_file,
        "validation": args.val_file,
    })

    print(f"   Train: {len(dataset['train'])} examples")
    print(f"   Val:   {len(dataset['validation'])} examples")

    # ============================================================
    # Step 4: Format with chat template
    # ============================================================
    print("📝 Applying chat template...")

    def format_chat(example):
        """Apply Qwen2.5 chat template to messages."""
        text = tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
        return {"text": text}

    dataset = dataset.map(format_chat, num_proc=4)

    # Check token lengths
    sample_tokens = tokenizer(dataset["train"][0]["text"], return_length=True)
    print(f"   Sample token length: {sample_tokens['length'][0]}")

    # Filter out examples that exceed max_seq_length
    def check_length(example):
        tokens = tokenizer(example["text"], return_length=True)
        return tokens["length"][0] <= args.max_seq_length

    orig_train_len = len(dataset["train"])
    dataset["train"] = dataset["train"].filter(check_length, num_proc=4)
    filtered = orig_train_len - len(dataset["train"])
    if filtered > 0:
        print(f"   ⚠️  Filtered {filtered} examples exceeding {args.max_seq_length} tokens")

    # ============================================================
    # Step 5: Training configuration
    # ============================================================
    print("🏋️ Setting up trainer...")

    from trl import SFTTrainer
    from transformers import TrainingArguments

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.learning_rate,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        weight_decay=0.01,
        fp16=False,
        bf16=True,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        report_to="wandb" if args.wandb else "none",
        run_name="entropy-hunter-7b" if args.wandb else None,
        seed=42,
        optim="adamw_8bit",  # 8-bit optimizer, saves VRAM
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        args=training_args,
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
        packing=True,  # Pack short examples together (faster)
    )

    # ============================================================
    # Step 6: Train!
    # ============================================================
    print(f"\n{'='*55}")
    print(f"🚀 Starting training")
    print(f"   Epochs: {args.epochs}")
    print(f"   Batch size: {args.batch_size} x {args.grad_accum} grad_accum = {args.batch_size * args.grad_accum} effective")
    print(f"   Learning rate: {args.learning_rate}")
    print(f"   LoRA r={args.lora_r}, alpha={args.lora_alpha}")
    print(f"   Output: {args.output_dir}")
    print(f"{'='*55}\n")

    trainer_stats = trainer.train()

    print(f"\n✅ Training complete!")
    print(f"   Total steps: {trainer_stats.global_step}")
    print(f"   Train loss: {trainer_stats.training_loss:.4f}")

    # ============================================================
    # Step 7: Save
    # ============================================================

    # Save LoRA adapter
    lora_dir = Path(args.output_dir) / "lora"
    model.save_pretrained(lora_dir)
    tokenizer.save_pretrained(lora_dir)
    print(f"   💾 LoRA adapter saved: {lora_dir}")

    # Save merged model (full weights, for inference)
    if args.save_merged:
        print("   Merging LoRA into base model...")
        merged_dir = Path(args.output_dir) / "merged"
        model.save_pretrained_merged(
            merged_dir,
            tokenizer,
            save_method="merged_16bit",
        )
        print(f"   💾 Merged model saved: {merged_dir}")

    # Save GGUF for llama.cpp (optional)
    if args.save_gguf:
        print("   Converting to GGUF...")
        gguf_dir = Path(args.output_dir) / "gguf"
        model.save_pretrained_gguf(
            gguf_dir,
            tokenizer,
            quantization_method=["q4_k_m", "q8_0"],
        )
        print(f"   💾 GGUF saved: {gguf_dir}")

    # Push to HuggingFace Hub
    if args.push_to_hub:
        print(f"   Pushing to HuggingFace: {args.push_to_hub}")
        model.push_to_hub_merged(
            args.push_to_hub,
            tokenizer,
            save_method="merged_16bit",
            token=os.environ.get("HF_TOKEN"),
        )
        print(f"   🤗 Pushed: https://huggingface.co/{args.push_to_hub}")

    # ============================================================
    # Step 8: Quick eval
    # ============================================================
    print(f"\n{'='*55}")
    print(f"🧪 Quick inference test")
    print(f"{'='*55}")

    FastLanguageModel.for_inference(model)

    test_prompt = """Perform a complete exergy analysis for a screw compressor.

Operating conditions:
- Electrical power input: 75 kW
- Air inlet temperature: 25°C
- Inlet pressure: 1.013 bar (atmospheric)
- Discharge pressure: 8 bar
- Isentropic efficiency: 72%
- Volume flow rate (FAD at inlet conditions): 10.5 m³/min
- Operating mode: full_load"""

    messages = [
        {"role": "system", "content": "You are EntropyHunter, an expert thermodynamic analysis assistant specializing in exergy (second-law) analysis of industrial equipment."},
        {"role": "user", "content": test_prompt},
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)

    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=2048,
        temperature=0.7,
        do_sample=True,
    )

    response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
    print(response[:1000])
    print(f"\n... ({len(response)} chars total)")
    print(f"\n✅ Done! Model ready at: {args.output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EntropyHunter Fine-Tuning")

    # Data
    parser.add_argument("--train-file", default="data/train.jsonl")
    parser.add_argument("--val-file", default="data/val.jsonl")
    parser.add_argument("--output-dir", default="output/entropy-hunter-7b")

    # Model
    parser.add_argument("--max-seq-length", type=int, default=8192,
                        help="Max sequence length (default: 8192)")

    # LoRA
    parser.add_argument("--lora-r", type=int, default=32,
                        help="LoRA rank (default: 32)")
    parser.add_argument("--lora-alpha", type=int, default=64,
                        help="LoRA alpha (default: 64, typically 2×r)")

    # Training
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Per-device batch size (default: 1 for L4 24GB)")
    parser.add_argument("--grad-accum", type=int, default=16,
                        help="Gradient accumulation steps (effective batch = batch_size × grad_accum)")
    parser.add_argument("--learning-rate", type=float, default=2e-4)

    # Output
    parser.add_argument("--save-merged", action="store_true",
                        help="Save full merged model (base + LoRA)")
    parser.add_argument("--save-gguf", action="store_true",
                        help="Save GGUF for llama.cpp")
    parser.add_argument("--push-to-hub", type=str, default=None,
                        help="Push to HuggingFace Hub (e.g. username/model-name)")

    # Tracking
    parser.add_argument("--wandb", action="store_true",
                        help="Log to Weights & Biases")

    args = parser.parse_args()
    main(args)
