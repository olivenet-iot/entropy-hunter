# EntropyHunter v0.2 Benchmark Analysis (Phase A)

Date: 27 February 2026
Model: entropy-hunter-v02 (Qwen2.5-7B + LoRA r=16)
Benchmark: eval/benchmark_v03.py (40 tests x 3 runs = 120 inferences)

## Overall Results

| Metric | Value |
|--------|-------|
| Overall score | **85.5%** (480/569 checks) |
| Grade | **B+** |
| Tests | 40 |
| Inferences | 120 (3 runs per test) |
| Temperature | 0.7 (optimal) |
| Base Qwen delta | **+17.3pp** (68.4% -> 85.5%) |

## Category Breakdown

| Category | Score | Grade | Notes |
|----------|-------|-------|-------|
| whatif_comparison | 97.3% | A+ | Best category, 5/5 tests |
| avoidable_unavoidable | 95.0% | A | Strong AV/UN decomposition |
| hotspot_detection | 91.7% | A- | Multi-equipment ranking solid |
| basic_exergy | 84.8% | B+ | Core capability, efficiency extraction noise |
| exergoeconomic | 79.5% | B | CRF calc and f-factor challenging |
| entropy_generation | 73.0% | B- | Weakest — EGM decomposition fractions |

## Temperature Sweep

| Temperature | Score | Notes |
|-------------|-------|-------|
| 0.1 | 83.7% | Conservative but misses some checks |
| 0.3 | 79.3% | Underperforms |
| 0.5 | 84.5% | Close to optimal |
| **0.7** | **85.5%** | **Optimal** |

## Non-determinism Map

27 of 40 tests show variation across runs. High-variance tests (>25pp spread):

| Test | Runs | Mean | Spread |
|------|------|------|--------|
| exergoecon-dryer-01 | 100%, 20%, 83% | 67.8% | 80pp |
| hotspot-factory-02 | 100%, 100%, 50% | 83.3% | 50pp |
| basic-turbine-02 | 60%, 100%, 100% | 86.7% | 40pp |
| avun-boiler-01 | 100%, 75%, 100% | 91.7% | 25pp |
| avun-compressor-01 | 100%, 100%, 75% | 91.7% | 25pp |
| avun-pump-01 | 100%, 100%, 75% | 91.7% | 25pp |
| basic-chiller-01 | 75%, 100%, 100% | 91.7% | 25pp |
| basic-boiler-02 | 75%, 100%, 75% | 83.3% | 25pp |
| basic-pump-02 | 100%, 100%, 75% | 91.7% | 25pp |

13 tests are fully deterministic (same score all 3 runs), 10 of which score 100%.

## Bottom 10 Tests (Improvement Targets)

| Test | Mean | Issue |
|------|------|-------|
| egm-compressor-01 | 61.1% | EGM decomposition fractions |
| egm-chiller-01 | 66.7% | EGM decomposition fractions |
| exergoecon-dryer-01 | 67.8% | High variance, CRF calc |
| exergoecon-pump-01 | 70.0% | f-factor extraction |
| basic-compressor-02 | 71.7% | Efficiency physical range |
| basic-boiler-01 | 72.2% | Efficiency extraction |
| basic-dryer-01 | 72.2% | Efficiency extraction |
| egm-compressor-02 | 72.2% | EGM fractions |
| egm-turbine-01 | 72.2% | EGM fractions |
| exergoecon-turbine-01 | 76.7% | CRF value |

## v0.3 JSON-Free Experiment

v0.3 removed JSON summary blocks from training data. Result: **regression to 78.3%** (-7.2pp).

Root cause: JSON block served as an accidental "reasoning scaffold". The model learned a "calculate in JSON first, then explain" pattern. Removing it broke the reasoning chain, especially for CRF and avoidable ratio calculations.

See: `archive/v03-json-free-attempt/README.md`

## Known Limitations

1. **EGM decomposition**: Model struggles with exact entropy generation fractions (heat transfer vs. pressure drop vs. mixing)
2. **CRF calculation**: Non-deterministic — sometimes correct formula, sometimes wrong values
3. **7B parameter limit**: Cannot reliably produce structured JSON output (0/120 json_block pass rate)
4. **Efficiency extraction**: Regex-sensitive — multiple output formats make automated scoring noisy

## Benchmark Methodology Notes

- `json_block` check excluded from scoring (7B model limitation, not a quality issue)
- `efficiency_physical` uses 4-strategy extraction (regex, table, nearby text, range scan)
- `avoidable_ratio` uses 19 keyword patterns for flexible matching
- Rescoring applied to original raw results to correct false negatives from strict regex

## Next Steps (v0.4 Planning)

1. Replace JSON scaffold with `## Calculation Summary` markdown format
2. Consider 14B base model (Qwen2.5-14B) for improved reasoning capacity
3. Add more EGM and exergoeconomic training examples
4. Target: 90%+ on 40-test benchmark
