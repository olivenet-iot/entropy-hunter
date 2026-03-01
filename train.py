"""
EntropyHunter v0.4 — Qwen3-8B LoRA Fine-Tuning

Changes from v0.2 (Qwen2.5-7B):
  - Base model: Qwen3-8B (unsloth/Qwen3-8B)
  - Thinking mode: DISABLED (enable_thinking=False)
    Our training data has no <think> blocks. SFT with thinking OFF
    trains the model to respond directly, like Qwen2.5 did.
  - Training data: 1235 train / 134 val (v0.4 scaffold format)
  - Data path: datagen/data/v0.4/training/ (repo-relative)
  - LoRA: r=16, alpha=32 (same as v0.2)
  - Output: output/entropy-hunter-8b-v04/

Uses Unsloth for 2x faster training with 60% less memory.

Usage:
    python train_v04.py                              # Default settings
    python train_v04.py --epochs 5                   # More epochs
    python train_v04.py --save-gguf                  # Export GGUF after training
    python train_v04.py --lora-r 32                  # Higher LoRA rank
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

    print("=" * 60)
    print("🔥 EntropyHunter v0.4 — Qwen3-8B Fine-Tuning")
    print("=" * 60)
    print()
    print(f"   Base model:      {args.model_name}")
    print(f"   LoRA rank:       {args.lora_r}")
    print(f"   LoRA alpha:      {args.lora_alpha}")
    print(f"   Learning rate:   {args.lr}")
    print(f"   Epochs:          {args.epochs}")
    print(f"   Max seq length:  {args.max_seq_length}")
    print(f"   Batch size:      {args.batch_size}")
    print(f"   Grad accum:      {args.grad_accum}")
    print(f"   Effective batch:  {args.batch_size * args.grad_accum}")
    print()

    print("📦 Loading Qwen3-8B...")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model_name,
        max_seq_length=args.max_seq_length,
        dtype=None,          # auto-detect (bf16 on L4)
        load_in_4bit=True,   # 4-bit quantization for LoRA training
    )

    print(f"   Model loaded. Max seq: {args.max_seq_length}")

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
    # Step 3: Load dataset (ChatML format from v0.4 pipeline)
    # ============================================================
    print("📚 Loading dataset...")

    from datasets import load_dataset

    dataset = load_dataset("json", data_files={
        "train": args.train_file,
        "validation": args.val_file,
    })

    print(f"   Train: {len(dataset['train'])} examples")
    print(f"   Val:   {len(dataset['validation'])} examples")

    # Validate a sample
    sample = dataset["train"][0]
    assert "messages" in sample, "Dataset must have 'messages' field (ChatML format)"
    roles = [m["role"] for m in sample["messages"]]
    assert "system" in roles and "user" in roles and "assistant" in roles, \
        f"Messages must have system/user/assistant roles, got: {roles}"
    print(f"   Sample roles: {roles}")
    print(f"   System prompt length: {len(sample['messages'][0]['content'])} chars")

    # ============================================================
    # Step 4: Format with Qwen3 chat template (thinking DISABLED)
    # ============================================================
    print("📝 Applying Qwen3 chat template (thinking=OFF)...")

    def format_chat(example):
        """Apply Qwen3 chat template with thinking disabled.

        Critical: enable_thinking=False because our training data
        contains direct analysis responses, no <think> blocks.
        This trains the model to respond directly like Qwen2.5 did.
        """
        text = tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
            enable_thinking=False,  # KEY: no <think> blocks
        )
        return {"text": text}

    dataset = dataset.map(format_chat)

    # Check token lengths
    sample_text = dataset["train"][0]["text"]
    sample_tokens = len(tokenizer.encode(sample_text))
    print(f"   Sample formatted length: {len(sample_text)} chars, ~{sample_tokens} tokens")

    # Warn if any examples might be truncated
    if sample_tokens > args.max_seq_length * 0.9:
        print(f"   ⚠️  Sample is {sample_tokens} tokens, close to max {args.max_seq_length}")

    # ============================================================
    # Step 5: Configure training
    # ============================================================
    print("⚙️  Configuring trainer...")

    from trl import SFTTrainer, SFTConfig

    output_dir = args.output_dir

    training_args = SFTConfig(
        # Output
        output_dir=output_dir,

        # Training schedule
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,

        # Learning rate
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,

        # Precision
        fp16=False,
        bf16=True,    # L4 GPU supports bf16

        # Logging
        logging_steps=5,
        logging_first_step=True,

        # Evaluation
        eval_strategy="steps",
        eval_steps=25,

        # Saving
        save_strategy="steps",
        save_steps=50,
        save_total_limit=3,

        # Sequence
        max_seq_length=args.max_seq_length,
        dataset_text_field="text",
        packing=False,  # No packing — each example is one sequence

        # Misc
        seed=42,
        report_to="none",  # Set to "wandb" if you want W&B tracking
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        args=training_args,
    )

    # ============================================================
    # Step 6: Train!
    # ============================================================
    print()
    print("=" * 60)
    print("🚀 Starting training...")
    print("=" * 60)
    print()

    stats = trainer.train()

    print()
    print("=" * 60)
    print("✅ Training complete!")
    print(f"   Total steps:    {stats.global_step}")
    print(f"   Training loss:  {stats.training_loss:.4f}")
    print(f"   Runtime:        {stats.metrics['train_runtime']:.0f}s "
          f"({stats.metrics['train_runtime']/60:.1f} min)")
    print("=" * 60)

    # ============================================================
    # Step 7: Save LoRA adapter
    # ============================================================
    lora_dir = os.path.join(output_dir, "lora")
    print(f"\n💾 Saving LoRA adapter to {lora_dir}...")
    model.save_pretrained(lora_dir)
    tokenizer.save_pretrained(lora_dir)
    print("   LoRA saved.")

    # Save training metadata
    metadata = {
        "project": "entropy-hunter",
        "version": "v0.4",
        "base_model": args.model_name,
        "lora_r": args.lora_r,
        "lora_alpha": args.lora_alpha,
        "learning_rate": args.lr,
        "epochs": args.epochs,
        "train_examples": len(dataset["train"]),
        "val_examples": len(dataset["validation"]),
        "max_seq_length": args.max_seq_length,
        "training_loss": stats.training_loss,
        "total_steps": stats.global_step,
        "runtime_seconds": stats.metrics["train_runtime"],
        "thinking_mode": False,
        "notes": "v0.4: Qwen3-8B + 1369 scaffold examples (Opus 4.6 teacher)"
    }
    meta_path = os.path.join(output_dir, "training_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"   Metadata saved to {meta_path}")

    # ============================================================
    # Step 8: GGUF export (optional)
    # ============================================================
    if args.save_gguf:
        print()
        print("=" * 60)
        print("📦 Exporting GGUF (Q4_K_M)...")
        print("=" * 60)

        gguf_dir = os.path.join(output_dir, "gguf")
        model.save_pretrained_gguf(
            gguf_dir,
            tokenizer,
            quantization_method=["q4_k_m"],
        )
        print(f"   GGUF saved to {gguf_dir}")

        # List output files
        gguf_path = Path(gguf_dir)
        # Unsloth creates a subdirectory with _gguf suffix
        for p in sorted(Path(output_dir).rglob("*.gguf")):
            size_gb = p.stat().st_size / (1024**3)
            print(f"   📄 {p.name} ({size_gb:.1f} GB)")

    # ============================================================
    # Step 9: Quick inference test
    # ============================================================
    if args.test:
        print()
        print("=" * 60)
        print("🧪 Quick inference test...")
        print("=" * 60)

        FastLanguageModel.for_inference(model)

        test_messages = [
            {"role": "system", "content": "You are an expert thermodynamics engineer specializing in exergy (second-law) analysis of industrial equipment."},
            {"role": "user", "content": (
                "Perform a basic exergy analysis for a centrifugal compressor.\n"
                "Operating conditions: inlet air at 25°C, 101.325 kPa; "
                "outlet at 215°C, 800 kPa; mass flow 2.5 kg/s; "
                "power input 520 kW; isentropic efficiency 78%.\n"
                "Dead state: T₀ = 25°C, P₀ = 101.325 kPa."
            )}
        ]

        inputs = tokenizer.apply_chat_template(
            test_messages,
            tokenize=True,
            add_generation_prompt=True,
            enable_thinking=False,
            return_tensors="pt",
        ).to(model.device)

        from transformers import TextStreamer
        streamer = TextStreamer(tokenizer, skip_prompt=True)

        print("\n--- Model response ---")
        output = model.generate(
            input_ids=inputs,
            streamer=streamer,
            max_new_tokens=2048,
            temperature=0.7,
            top_p=0.8,
            top_k=20,
            do_sample=True,
        )
        print("--- End response ---\n")

    print()
    print("🏁 All done!")
    if not args.save_gguf:
        print("   Next: python train_v04.py --save-gguf  (to export GGUF)")
    print("   Next: Download GGUF → ollama create → benchmark")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EntropyHunter v0.4 Training")

    # Model
    parser.add_argument("--model-name", default="unsloth/Qwen3-8B",
                        help="Base model (default: unsloth/Qwen3-8B)")
    parser.add_argument("--max-seq-length", type=int, default=8192,
                        help="Max sequence length (default: 8192)")

    # Data — relative to script location or absolute
    script_dir = Path(__file__).parent
    default_train = script_dir / "datagen" / "data" / "v0.4" / "training" / "train.jsonl"
    default_val = script_dir / "datagen" / "data" / "v0.4" / "training" / "val.jsonl"

    parser.add_argument("--train-file", default=str(default_train),
                        help="Training data JSONL (ChatML)")
    parser.add_argument("--val-file", default=str(default_val),
                        help="Validation data JSONL (ChatML)")

    # LoRA
    parser.add_argument("--lora-r", type=int, default=16,
                        help="LoRA rank (default: 16)")
    parser.add_argument("--lora-alpha", type=int, default=32,
                        help="LoRA alpha (default: 32)")

    # Training
    parser.add_argument("--lr", type=float, default=1e-4,
                        help="Learning rate (default: 1e-4)")
    parser.add_argument("--epochs", type=int, default=3,
                        help="Training epochs (default: 3)")
    parser.add_argument("--batch-size", type=int, default=2,
                        help="Per-device batch size (default: 2)")
    parser.add_argument("--grad-accum", type=int, default=4,
                        help="Gradient accumulation steps (default: 4)")

    # Output
    parser.add_argument("--output-dir", default="output/entropy-hunter-8b-v04",
                        help="Output directory")

    # Actions
    parser.add_argument("--save-gguf", action="store_true",
                        help="Export GGUF after training")
    parser.add_argument("--test", action="store_true", default=True,
                        help="Run inference test after training (default: True)")
    parser.add_argument("--no-test", dest="test", action="store_false",
                        help="Skip inference test")

    args = parser.parse_args()
    main(args)
