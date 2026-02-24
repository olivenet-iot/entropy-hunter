# 🔥 EntropyHunter-7B

**The world's first open-source fine-tuned model for industrial exergy analysis and entropy generation detection.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-yellow.svg)](https://huggingface.co/OlivenetAI)
[![Status: In Development](https://img.shields.io/badge/Status-In_Development-orange.svg)]()

---

## What is EntropyHunter?

EntropyHunter is a domain-specific language model fine-tuned to perform **second-law thermodynamic analysis** on industrial equipment. Given equipment parameters, it can:

- Calculate **exergy balances** (input, output, destruction, efficiency)
- Identify **entropy generation mechanisms** (heat transfer, pressure drop, mixing)
- Perform **Gouy-Stodola verification** (Ex_destroyed = T₀ × S_gen)
- Classify equipment with **Bejan number grading** (A–F)
- Recommend **practical improvements** based on avoidable/unavoidable decomposition
- Conduct **thermoeconomic analysis** (SPECO methodology)
- Perform **pinch analysis** for heat integration
- Generate **ISO 50001 energy management** assessments

## Supported Equipment

| Equipment | Subtypes | Analysis Depth |
|-----------|----------|---------------|
| Compressor | screw, piston, scroll, centrifugal | Full |
| Boiler | fire-tube, water-tube, condensing, waste heat, biomass, electric | Full |
| Chiller | screw, centrifugal, absorption, air/water-cooled | Full |
| Pump | centrifugal, positive displacement, submersible, vertical turbine | Full |
| Heat Exchanger | shell & tube, plate, air-cooled, economizer, recuperator | Full |
| Steam Turbine | back-pressure, condensing, extraction, ORC, micro | Full |
| Dryer | rotary, fluidized bed, spray, belt, heat pump, infrared | Full |

**7 equipment types × 48 subtypes × 14 analysis types**

## Quick Start

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("OlivenetAI/EntropyHunter-7B")
tokenizer = AutoTokenizer.from_pretrained("OlivenetAI/EntropyHunter-7B")

prompt = """Perform an exergy analysis for a shell & tube heat exchanger.

Operating conditions:
- Hot fluid: Flue gas, inlet 320°C, outlet 180°C, flow rate 2.5 kg/s
- Cold fluid: Water, inlet 25°C, outlet 85°C, flow rate 4.0 kg/s
- Dead state: T₀ = 25°C, P₀ = 101.325 kPa

Provide: exergy balance, efficiency, entropy generation, Bejan number, recommendations."""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=1024, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Project Structure

```
entropy-hunter/
├── taxonomy/          # Equipment & analysis type definitions
├── datagen/           # Synthetic training data generation pipeline
├── data/              # Generated datasets (not tracked in git)
├── training/          # LoRA fine-tuning scripts
├── eval/              # Evaluation benchmarks & results
└── serving/           # Deployment configurations
```

## Training Methodology

EntropyHunter is trained via **knowledge distillation**:

1. **Domain Expert Design** — Thermodynamic scenarios designed by chemical engineers with field experience
2. **Synthetic Data Generation** — High-quality instruction-output pairs generated from frontier models
3. **Quality Control** — Every example verified for thermodynamic consistency (energy balance, second law, Gouy-Stodola)
4. **LoRA Fine-tuning** — Efficient adaptation on Qwen2.5-7B base using Unsloth
5. **Evaluation** — Benchmarked against base model and frontier models on held-out test sets

Training data is informed by the [ExergyLab](https://github.com/your-username/exergy-lab) platform's 7 analysis engines, 317 knowledge files, and industrial reference data.

## Roadmap

- [x] **v0.0** — Project structure, taxonomy, prompt templates
- [ ] **v0.1** — MVP: ~800 examples, basic exergy + EGM + SPECO (target: Q2 2026)
- [ ] **v0.2** — Extended: ~3000 examples, pinch + Tsatsaronis + thermoeconomic
- [ ] **v0.3** — Expert: ~5000+ examples, fault diagnosis + Turkish support
- [ ] **v1.0** — Production: ExergyLab integration, edge deployment

## Technical Foundation

Built on established thermodynamic methodologies:

- **Exergy analysis**: Kotas, Bejan, Tsatsaronis & Moran
- **SPECO methodology**: Tsatsaronis (2009) — Thermoeconomic cost allocation
- **EGM**: Bejan (1996) — Entropy Generation Minimization
- **Advanced exergy**: Tsatsaronis & Morosuk — EN/EX + AV/UN decomposition
- **Pinch analysis**: Linnhoff & Hindmarsh (1983) — Heat integration
- **Gap analysis**: 3-layer exergetic gap (minimum / BAT / actual)

## Author

**Kemal Düzkar** — Chemical Engineer & Founder, [Olivenet Ltd.](https://olivenet.io)

Combining thermodynamic expertise with IoT and AI to hunt entropy in industrial systems.

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.

## Citation

```bibtex
@misc{entropyhunter2026,
  author = {Düzkar, Kemal},
  title = {EntropyHunter-7B: Fine-tuned Model for Industrial Exergy Analysis},
  year = {2026},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/OlivenetAI/EntropyHunter-7B}}
}
```

---

*"Every irreversibility is a missed opportunity. Every entropy generated is value destroyed. This model finds them."*
