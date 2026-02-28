# CLAUDE.md — EntropyHunter Project Instructions

## Project Overview

EntropyHunter-7B is a domain-specific language model fine-tuned for industrial exergy analysis and entropy generation detection. It is the world's first open-source model for second-law thermodynamic analysis.

**Owner:** Kemal Düzkar / Olivenet Ltd.
**Status:** Phase 2 (Data Generation) complete, Phase 3 (Evaluation) complete for v0.2. Next: v0.4 planning.

## Repository Structure

```
entropy-hunter/
├── taxonomy/          # Equipment & analysis type definitions (YAML)
├── datagen/           # Synthetic training data generation pipeline
│   ├── config.py      # API config, ExergyLab path, quality thresholds
│   ├── templates/     # Prompt templates for each analysis family (A-J)
│   ├── generate.py    # Main generation orchestrator
│   └── quality.py     # Thermodynamic consistency checks
├── data/              # Generated datasets (gitignored, uploaded to HF separately)
├── training/          # LoRA fine-tuning scripts (Unsloth)
├── eval/              # Evaluation benchmarks & results
└── serving/           # Deployment configs (vLLM, GGUF)
```

## Key Dependencies

- **ExergyLab** is a sibling repo at `../exergy-lab/`. It provides:
  - `knowledge/` (317 markdown files) — domain knowledge for prompt context
  - `skills/` (18 markdown files) — system prompt personas
  - `engine/` — reference constants (BAT, Bejan grades, SPECO correlations)
  - DO NOT copy ExergyLab files into this repo. Reference them via path.

## Thermodynamic Rules (CRITICAL)

These are non-negotiable physical laws. All generated data must satisfy:

1. **Exergy balance:** Ex_in = Ex_out + Ex_destroyed (±1%)
2. **Second law:** Ex_destroyed ≥ 0 (entropy generation is never negative)
3. **Gouy-Stodola:** Ex_destroyed = T₀ × S_gen (±2%)
4. **Dead state:** T₀ = 298.15 K (25°C), P₀ = 101.325 kPa (unless specified)
5. **Bejan number:** 0 ≤ N_s ≤ 1
6. **AV/UN split:** avoidable + unavoidable = total destruction
7. **SPECO:** 0 ≤ f-factor ≤ 1
8. **COP:** Cannot exceed Carnot COP for the given temperatures

## ExergyLab Engine Constants

When generating data or writing code that references thermodynamic constants,
use the values from ExergyLab's engines:

- `engine/core.py` — DeadState, ExergyResult, heat_exergy(), carnot_factor()
- `engine/exergoeconomic.py` — COST_CORRELATIONS, CRF calculation
- `engine/advanced_exergy.py` — BASE_ISOLATION_FACTORS, INTERACTION_COEFFICIENTS
- `engine/entropy_generation.py` — ENTROPY_DECOMPOSITION_FRACTIONS, BEJAN_GRADES
- `engine/bat_references.py` — BAT_REFERENCES for 8 process types

## Coding Conventions

- Python 3.10+
- Type hints everywhere
- Docstrings for public functions
- YAML for configuration, JSON for data
- Alpaca format for training data: {"instruction": ..., "input": ..., "output": ...}
- All temperatures in Kelvin for calculations, Celsius for display
- All pressures in kPa internally, bar for display

## Current Phase: v0.4 Planning

v0.2 is the active model (85.5%, Grade B+, 40 tests x 3 runs).
v0.3 JSON-free experiment failed (-7.2pp regression), archived in `archive/v03-json-free-attempt/`.

Next steps:
1. Evaluate 14B base model (Qwen2.5-14B) for improved reasoning
2. Replace JSON scaffold with `## Calculation Summary` markdown format
3. Add more EGM and exergoeconomic training examples (weakest categories)
4. Target: 90%+ on 40-test benchmark

## Do NOT

- Do not hallucinate thermodynamic values — if unsure, flag for review
- Do not copy ExergyLab source code into this repo
- Do not commit API keys or data files to git
- Do not modify taxonomy without discussion (it maps to ExergyLab engines)
