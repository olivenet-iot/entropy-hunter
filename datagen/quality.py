"""
EntropyHunter — Thermodynamic Quality Control (v5 — Scaffold Parser)

CHANGE LOG v4→v5:
- _extract_from_scaffold() ADDED as primary extraction method
- Extraction priority: Scaffold → JSON (backward compat) → Table regex → Inline regex
- scaffold_present check added for training data QC
- All existing regex patterns PRESERVED for backward compatibility (v0.2 benchmark)

Every generated example must pass these checks before
being included in the training dataset.

Based on ExergyLab engine constraints and second law requirements.
"""

import json
import re
from dataclasses import dataclass
from typing import Optional
from config import QUALITY, DEAD_STATE


@dataclass
class QualityResult:
    passed: bool
    checks: dict[str, bool]
    errors: list[str]
    warnings: list[str]


def check_example(example: dict) -> QualityResult:
    """
    Run all quality checks on a generated example.
    Returns QualityResult with pass/fail and details.
    """
    checks = {}
    errors = []
    warnings = []
    output_text = example.get("output", "")

    # 0. Scaffold presence check (for v0.4 training data QC)
    checks["scaffold_present"] = "## Calculation Summary" in output_text
    if not checks["scaffold_present"]:
        warnings.append("No ## Calculation Summary scaffold found in output")

    # 1. Energy balance check (Ex_in = Ex_out + Ex_waste + Ex_destroyed)
    values = extract_numeric_values(output_text)
    if values.get("exergy_in") and values.get("exergy_out") and values.get("exergy_destroyed"):
        ex_in = values["exergy_in"]
        ex_out = values["exergy_out"]
        ex_d = values["exergy_destroyed"]
        ex_waste = values.get("exergy_waste", 0.0)
        
        # Try with waste first
        balance_with_waste = abs(ex_in - ex_out - ex_waste - ex_d)
        # Try without waste (in case parser grabbed wrong waste value)
        balance_without_waste = abs(ex_in - ex_out - ex_d)
        
        # Use the better-closing balance
        balance = min(balance_with_waste, balance_without_waste)
        tolerance = QUALITY["energy_balance_tolerance_pct"] / 100 * ex_in
        
        checks["energy_balance"] = balance <= tolerance
        if not checks["energy_balance"]:
            errors.append(
                f"Energy balance violation: |{ex_in:.1f} - {ex_out:.1f} "
                f"- {ex_waste:.1f}(waste) - {ex_d:.1f}| = {balance_with_waste:.1f}, "
                f"without waste = {balance_without_waste:.1f}, tol = {tolerance:.1f}"
            )
    else:
        checks["energy_balance"] = None  # cannot verify
        warnings.append("Could not extract exergy values for balance check")

    # 2. Efficiency range
    if values.get("efficiency"):
        eff = values["efficiency"]
        checks["efficiency_range"] = QUALITY["min_efficiency_pct"] < eff < QUALITY["max_efficiency_pct"]
        if not checks["efficiency_range"]:
            errors.append(f"Efficiency {eff:.1f}% outside valid range")
    else:
        checks["efficiency_range"] = None

    # 3. Second law (non-negative exergy destruction)
    if values.get("exergy_destroyed") is not None:
        checks["second_law"] = values["exergy_destroyed"] >= QUALITY["min_exergy_destroyed_kW"]
        if not checks["second_law"]:
            errors.append(f"Second law violation: Ex_destroyed = {values['exergy_destroyed']:.2f} < 0")
    else:
        checks["second_law"] = None

    # 4. Gouy-Stodola consistency
    if values.get("exergy_destroyed") and values.get("entropy_generation"):
        T0 = DEAD_STATE["T0_K"]
        gouy_stodola = T0 * values["entropy_generation"]
        deviation = abs(gouy_stodola - values["exergy_destroyed"])
        tolerance = QUALITY["gouy_stodola_tolerance_pct"] / 100 * values["exergy_destroyed"]
        checks["gouy_stodola"] = deviation <= tolerance
        if not checks["gouy_stodola"]:
            errors.append(
                f"Gouy-Stodola mismatch: T₀×S_gen = {gouy_stodola:.2f} vs "
                f"Ex_d = {values['exergy_destroyed']:.2f} (Δ = {deviation:.2f})"
            )
    else:
        checks["gouy_stodola"] = None

    # 5. Bejan number range
    if values.get("bejan_number") is not None:
        Ns = values["bejan_number"]
        lo, hi = QUALITY["bejan_number_range"]
        checks["bejan_range"] = lo <= Ns <= hi
        if not checks["bejan_range"]:
            errors.append(f"Bejan number N_s = {Ns:.3f} outside [{lo}, {hi}]")
    else:
        checks["bejan_range"] = None

    # 6. SPECO factors range
    if values.get("f_factor") is not None:
        f = values["f_factor"]
        lo, hi = QUALITY["f_factor_range"]
        checks["f_factor_range"] = lo <= f <= hi
        if not checks["f_factor_range"]:
            errors.append(f"f-factor = {f:.3f} outside [{lo}, {hi}]")
    else:
        checks["f_factor_range"] = None

    # 7. Dead state consistency
    if "298.15" in output_text or "25°C" in output_text or "25 °C" in output_text:
        checks["dead_state"] = True
    else:
        checks["dead_state"] = None
        warnings.append("Dead state reference not found in output")

    # 8. Avoidable/Unavoidable split consistency
    if values.get("avoidable") and values.get("unavoidable") and values.get("exergy_destroyed"):
        split_sum = values["avoidable"] + values["unavoidable"]
        deviation = abs(split_sum - values["exergy_destroyed"])
        tolerance = 0.01 * values["exergy_destroyed"]
        checks["av_un_split"] = deviation <= tolerance
        if not checks["av_un_split"]:
            errors.append(f"AV+UN = {split_sum:.2f} ≠ Ex_d = {values['exergy_destroyed']:.2f}")
    else:
        checks["av_un_split"] = None

    # Determine overall pass/fail
    # scaffold_present is a warning, not a hard fail (backward compat with v0.2 data)
    verified_checks = {k: v for k, v in checks.items()
                       if v is not None and k != "scaffold_present"}
    passed = all(verified_checks.values()) if verified_checks else False

    return QualityResult(
        passed=passed,
        checks=checks,
        errors=errors,
        warnings=warnings,
    )


# ============================================================
# VALUE EXTRACTION — 4-phase priority chain
# ============================================================

def extract_numeric_values(text: str) -> dict[str, Optional[float]]:
    """
    Extract key numeric values from generated analysis text.
    
    STRATEGY (priority order):
    1. Calculation Summary scaffold (v0.4 primary format)
    2. JSON summary block (v0.2 backward compatibility)
    3. Markdown table extraction with unit validation
    4. Inline pattern extraction with physical validity filtering
    
    Falls back gracefully through each phase.
    """
    # === PHASE 0: Try Calculation Summary scaffold first (v0.4) ===
    values = _extract_from_scaffold(text)
    if values and len(values) >= 3:
        # Sanity check: if physically impossible, fall through to regex
        ei = values.get("exergy_in")
        eo = values.get("exergy_out")
        ed = values.get("exergy_destroyed")
        if ei and eo and ei > 0 and eo > ei * 5:
            # exergy_out >> exergy_in → parser grabbed wrong values
            pass  # fall through to regex
        elif ei and ed and ei > 0 and ed > ei * 2:
            # exergy_destroyed >> exergy_in → parser grabbed wrong values
            pass  # fall through
        else:
            return values

    # === PHASE 1: Try JSON summary block (v0.2 backward compat) ===
    values = _extract_from_json_block(text)
    if values and len(values) >= 3:
        return values

    # === PHASE 2+3: Regex fallback ===
    return _extract_from_regex(text)


# ============================================================
# PHASE 0: SCAFFOLD PARSER (v0.4 — primary)
# ============================================================

# Key normalization: scaffold label → internal key
SCAFFOLD_KEY_MAP = {
    # Basic exergy — standard labels
    "exergy in": "exergy_in",
    "exergy out": "exergy_out",
    "exergy out (product)": "exergy_out",
    "exergy destroyed": "exergy_destroyed",
    "exergy destroyed (total)": "exergy_destroyed",
    "exergy efficiency": "efficiency",
    "exergy efficiency (actual)": "efficiency",
    "entropy generation": "entropy_generation",
    "entropy generation (sgen)": "entropy_generation",
    "total entropy generation": "entropy_generation",
    "total entropy generation (sgen)": "entropy_generation",
    "bejan number": "bejan_number",
    "bejan number (ns)": "bejan_number",

    # Exergy in — Opus label variants (fallback)
    "electrical power input": "exergy_in",
    "electrical power input (exergy fuel)": "exergy_in",
    "electrical input": "exergy_in",
    "fuel exergy input": "exergy_in",
    "fuel exergy": "exergy_in",
    "exergy input": "exergy_in",
    "total exergy input": "exergy_in",
    "motor shaft power input": "exergy_in",
    "compressor power input": "exergy_in",
    "thermal exergy input": "exergy_in",

    # Exergy out — Opus label variants (fallback)
    "exergy output": "exergy_out",
    "product exergy": "exergy_out",
    "useful exergy output": "exergy_out",
    "hydraulic power (exergy product)": "exergy_out",
    "hydraulic power": "exergy_out",
    "flow exergy increase": "exergy_out",
    "steam exergy output": "exergy_out",
    "cooling exergy output": "exergy_out",
    "exergy of product": "exergy_out",

    # Exergy destroyed — Opus label variants
    "exergy destruction": "exergy_destroyed",
    "total exergy destruction": "exergy_destroyed",
    "exergy destroyed (total)": "exergy_destroyed",

    # Waste exergy
    "exergy waste": "exergy_waste",
    "waste exergy": "exergy_waste",
    "waste stream exergy": "exergy_waste",
    "flue gas exergy loss": "exergy_waste",

    # Exergoeconomic
    "crf": "crf",
    "capital recovery factor": "crf",
    "capital recovery factor (crf)": "crf",
    "investment cost rate (zdot)": "z_dot",
    "investment cost rate": "z_dot",
    "fuel cost rate (cf)": "c_fuel",
    "fuel cost rate": "c_fuel",
    "destruction cost rate (cdotd)": "c_dot_d",
    "destruction cost rate": "c_dot_d",
    "exergoeconomic factor (f)": "f_factor",
    "exergoeconomic factor": "f_factor",
    "total cost rate": "total_cost_rate",

    # EGM mechanism values
    "heat transfer (sgen,ht)": "sgen_ht",
    "pressure drop (sgen,dp)": "sgen_dp",
    "mixing/chemical (sgen,mix)": "sgen_mix",
    # Opus variants
    "s_gen,ht (heat transfer)": "sgen_ht",
    "s_gen,dp (pressure drop)": "sgen_dp",
    "s_gen,mix (mixing/chemical)": "sgen_mix",
    "heat transfer irreversibility": "sgen_ht",
    "pressure drop irreversibility": "sgen_dp",
    "mixing irreversibility": "sgen_mix",

    # AV/UN
    "unavoidable exergy destruction": "unavoidable",
    "avoidable exergy destruction": "avoidable",
    "avoidable ratio": "avoidable_ratio",
    # Opus variants
    "unavoidable destruction": "unavoidable",
    "avoidable destruction": "avoidable",

    # What-if
    "annual energy savings": "annual_energy_savings",
    "annual cost savings": "annual_cost_savings",
    "delta exergy destroyed": "delta_exd",
}


def _extract_from_scaffold(text: str) -> dict[str, Optional[float]]:
    """
    Extract values from ## Calculation Summary scaffold sections.
    
    Handles two value formats:
    1. Simple:   `- Exergy in: 55.00 kW`
    2. Equation: `- Fuel exergy input: Ex_fuel = 515.46 × 1.04 = 536.08 kW`
    
    Strategy: For each bullet line, find the LAST number followed by a recognized unit.
    This handles equations naturally (takes the final result, not intermediates).
    
    For whatif, returns BASELINE values for core fields and COMPARISON values for deltas.
    Returns empty dict if no scaffold found.
    """
    # Find all Calculation Summary sections
    sections = re.findall(
        r"## Calculation Summary[^\n]*\n(.*?)(?=\n## (?!Calculation)|$)",
        text, re.DOTALL
    )

    if not sections:
        return {}

    values = {}

    # Units we recognize (order matters — longer first to avoid partial matches)
    UNIT_PATTERN = r"(kWh/yr|EUR/yr|EUR/kWh|EUR/h|kW/K|h/yr|kW|kJ|°C|EUR|pp|%|K)"
    
    # Preferred unit per internal key — parser picks match with this unit first
    # Falls back to last match if preferred unit not found
    PREFERRED_UNIT = {
        "exergy_in": "kW", "exergy_out": "kW", "exergy_destroyed": "kW",
        "exergy_waste": "kW", "avoidable": "kW", "unavoidable": "kW",
        "efficiency": "%", "avoidable_ratio": "%",
        "entropy_generation": "kW/K",
        "sgen_ht": "kW/K", "sgen_dp": "kW/K", "sgen_mix": "kW/K",
        "z_dot": "EUR/h", "c_dot_d": "EUR/h", "c_fuel": "EUR/kWh",
        "total_cost_rate": "EUR/h",
        "annual_energy_savings": "kWh/yr", "annual_cost_savings": "EUR/yr",
    }

    # Pattern to find ALL (number, unit) pairs on a line
    num_unit_pattern = re.compile(
        r"~?([\d]+[.,][\d]+|[\d]+(?:,\d{3})*)"   # Number (with optional comma thousands)
        r"\s*" + UNIT_PATTERN,                      # Followed by recognized unit
        re.IGNORECASE
    )
    
    # Simpler pattern for dimensionless values (no unit, end of meaningful content)
    num_bare_pattern = re.compile(
        r"=\s*([\d]+[.,][\d]+|[\d]+)\s*$"
    )

    for section in sections:
        for line in section.strip().split('\n'):
            line = line.strip()
            if not line.startswith(('-', '*')):
                continue

            # Split at first colon to get label and value part
            colon_pos = line.find(':')
            if colon_pos < 0:
                continue
            
            # Extract label (strip leading - or * and whitespace)
            label_raw = line[:colon_pos].lstrip('-* \t')
            label = label_raw.strip().lower()
            value_part = line[colon_pos + 1:]

            # Find ALL number+unit matches in value part
            matches = list(num_unit_pattern.finditer(value_part))
            
            # Also extract first bare number (no unit) — critical for dimensionless values
            # CRF: 0.07095 (i = 5%, n = 25 years) → bare = 0.07095, unit match = 5%
            first_bare_match = re.match(r"\s*~?([\d]+[.,][\d]+|[\d]+)", value_part)
            bare_val = None
            if first_bare_match:
                try:
                    bare_val = float(first_bare_match.group(1).replace(',', '.'))
                except ValueError:
                    pass
            
            if matches:
                parsed_matches = []
                for m in matches:
                    try:
                        num_str = m.group(1).replace(',', '')
                        if ',' in m.group(1) and '.' not in m.group(1):
                            num_str = m.group(1).replace(',', '.')
                        parsed_matches.append((float(num_str), m.group(2)))
                    except ValueError:
                        continue
                
                if not parsed_matches and bare_val is None:
                    continue
            elif bare_val is not None:
                parsed_matches = []
            else:
                continue

            # Look up internal key
            internal_key = SCAFFOLD_KEY_MAP.get(label)
            
            if not internal_key:
                # Partial matching: find LONGEST matching key (prevents "exergy in" 
                # matching inside "exergy increase" before "exergy out" gets a chance)
                best_match_len = 0
                for map_key, internal in SCAFFOLD_KEY_MAP.items():
                    if map_key in label and len(map_key) > best_match_len:
                        best_match_len = len(map_key)
                        internal_key = internal
            
            if not internal_key:
                label_concepts = {
                    "exergy_in": ["exergy in", "exergy fuel", "fuel exergy", "power input",
                                  "exergy input", "exergy transfer hot"],
                    "exergy_out": ["exergy out", "exergy product", "product exergy", "exergy of cooling",
                                   "useful exergy", "flow exergy increase", "exergy transfer cold"],
                    "exergy_destroyed": ["exergy destroy", "exergy destruct"],
                    "efficiency": ["exergy efficien", "η_ex"],
                    "exergy_waste": ["exergy lost", "exergy loss", "stack gas exergy", "waste stream",
                                     "exergy rejected"],
                    "entropy_generation": ["entropy generation", "sgen"],
                    "bejan_number": ["bejan number", "bejan (ns)", "(ns)"],
                }
                # Check longest concept first to avoid substring collisions
                best_concept_len = 0
                for ikey, concepts in label_concepts.items():
                    for c in concepts:
                        if c in label and len(c) > best_concept_len:
                            best_concept_len = len(c)
                            internal_key = ikey

            if internal_key:
                # Select best match based on key type
                preferred = PREFERRED_UNIT.get(internal_key)
                val = None
                
                # Keys that MUST match their preferred unit (no fallback to wrong unit)
                # Prevents "waste streams at 80°C" → exergy_waste = 80 kW
                STRICT_UNIT_KEYS = {
                    "exergy_in", "exergy_out", "exergy_destroyed", "exergy_waste",
                    "avoidable", "unavoidable",
                    "sgen_ht", "sgen_dp", "sgen_mix", "entropy_generation",
                    "z_dot", "c_dot_d", "c_fuel", "total_cost_rate",
                    "annual_energy_savings", "annual_cost_savings",
                }
                
                if preferred and parsed_matches:
                    # Key has a preferred unit (kW, kW/K, %, etc.)
                    preferred_vals = [v for v, u in parsed_matches if u == preferred]
                    if preferred_vals:
                        val = preferred_vals[-1]  # Last match with correct unit
                
                if val is None and not preferred and bare_val is not None:
                    # Dimensionless key (CRF, Bejan, f-factor): prefer bare number
                    val = bare_val
                
                if val is None and parsed_matches and internal_key not in STRICT_UNIT_KEYS:
                    # Non-strict keys: take last match regardless of unit
                    val = parsed_matches[-1][0]
                
                if val is None and bare_val is not None and internal_key not in STRICT_UNIT_KEYS:
                    val = bare_val

                if val is not None:
                    comparison_keys = {"delta_exd", "annual_energy_savings", "annual_cost_savings"}
                    if internal_key not in values or internal_key in comparison_keys:
                        values[internal_key] = val

    return values


# ============================================================
# PHASE 1: JSON BLOCK PARSER (v0.2 backward compat)
# ============================================================

def _extract_from_json_block(text: str) -> dict[str, Optional[float]]:
    """
    Extract values from the machine-readable JSON block.
    Returns empty dict if no valid JSON block found.
    """
    key_map = {
        "exergy_in_kW": "exergy_in",
        "exergy_out_kW": "exergy_out",
        "exergy_waste_kW": "exergy_waste",
        "exergy_destroyed_kW": "exergy_destroyed",
        "efficiency_pct": "efficiency",
        "entropy_generation_kW_K": "entropy_generation",
        "bejan_number": "bejan_number",
        "avoidable_kW": "avoidable",
        "unavoidable_kW": "unavoidable",
        "f_factor": "f_factor",
    }

    # Find JSON block
    match = re.search(r'```json\s*\n?\s*(\{[^}]+\})\s*\n?\s*```', text, re.DOTALL)
    if not match:
        match = re.search(r'(\{"exergy_in_kW"[^}]+\})', text, re.DOTALL)
    if not match:
        return {}

    try:
        raw = json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError):
        return {}

    values = {}
    for json_key, internal_key in key_map.items():
        val = raw.get(json_key)
        if val is not None and isinstance(val, (int, float)):
            values[internal_key] = float(val)

    core_keys = {"exergy_in", "exergy_out", "exergy_destroyed", "efficiency"}
    if len(core_keys & set(values.keys())) < 3:
        return {}

    return values


# ============================================================
# PHASE 2+3: REGEX FALLBACK (backward compat)
# ============================================================

def _extract_from_regex(text: str) -> dict[str, Optional[float]]:
    """
    Regex-based extraction (fallback for pre-scaffold examples or model inference output).
    
    3-phase strategy:
    1. Strict kW table patterns
    2. Other table patterns (%, dimensionless)
    3. Inline patterns with physical validity filtering
    """
    values = {}

    valid_ranges = {
        "exergy_in": (0.01, 100000),
        "exergy_out": (0.01, 100000),
        "exergy_destroyed": (-1000, 100000),
        "efficiency": (0.0, 200.0),
        "entropy_generation": (0.0001, 1000),
        "bejan_number": (0.0, 1.0),
        "f_factor": (0.0, 1.0),
        "avoidable": (0.0, 100000),
        "unavoidable": (0.0, 100000),
    }

    # === PHASE 2: Table extraction ===
    table_patterns_kw = {
        "exergy_in": r"\|\s*(?:[Ee]xergy\s+[Ii]nput|[Ee]lectrical\s+power\s+input)[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "exergy_out": r"\|\s*(?:[Ee]xergy\s+(?:[Oo]utput|[Pp]roduct)|[Ff]low\s+exergy\s+increase|[Uu]seful\s+exergy\s+output)[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "exergy_destroyed": r"\|\s*[Ee]xergy\s+[Dd]estruction\s*\([^)]*\)\s*\|\s*(-?[\d,.]+)\s*\|\s*kW\s*\|",
        "entropy_generation": r"\|\s*[Ee]ntropy\s+[Gg]eneration[^|]*\|\s*([\d,.]+)\s*\|\s*kW/K\s*\|",
        "avoidable": r"\|\s*[Aa]voidable\s+(?:exergy\s+)?(?:destruction\s*)?\(?[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
        "unavoidable": r"\|\s*[Uu]navoidable\s+(?:exergy\s+)?(?:destruction\s*)?\(?[^|]*\|\s*([\d,.]+)\s*\|\s*kW\s*\|",
    }

    table_patterns_other = {
        "efficiency": r"\|\s*[Ee]xergy\s+[Ee]fficiency[^|]*\|\s*([\d,.]+)\s*\|\s*%\s*\|",
        "bejan_number": r"\|\s*(?:[Ee]xergy\s+[Dd]estruction\s+ratio|[Dd]imensionless\s+entropy|[Ee]ntropy\s+generation\s+number)\s*[^|]*\|\s*([\d,.]+)\s*\|\s*[—–-]\s*\|",
        "f_factor": r"\|\s*[Ee]xergoeconomic\s+[Ff]actor[^|]*\|\s*([\d,.]+)\s*\|",
    }

    for patterns in [table_patterns_kw, table_patterns_other]:
        for key, pattern in patterns.items():
            if key in values:
                continue
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                try:
                    val = float(matches[-1].group(1).replace(",", "."))
                    lo, hi = valid_ranges.get(key, (0, 1e9))
                    if lo <= val <= hi:
                        values[key] = val
                except ValueError:
                    pass

    # Loose table patterns (no unit check)
    table_patterns_loose = {
        "exergy_in": r"\|\s*(?:[Ee]xergy\s+[Ii]nput|[Ee]lectrical\s+power\s+input)[^|]*\|\s*([\d,.]+)\s*\|",
        "exergy_out": r"\|\s*(?:[Ee]xergy\s+(?:[Oo]utput|[Pp]roduct)|[Ff]low\s+exergy\s+increase|[Uu]seful\s+exergy\s+output)[^|]*\|\s*([\d,.]+)\s*\|",
        "exergy_destroyed": r"\|\s*[Ee]xergy\s+[Dd]estruction(?!\s+ratio)[^|]*\|\s*(-?[\d,.]+)\s*\|",
        "efficiency": r"\|\s*[Ee]xergy\s+[Ee]fficiency[^|]*\|\s*([\d,.]+)\s*\|",
        "bejan_number": r"\|\s*(?:[Ee]xergy\s+[Dd]estruction\s+ratio|[Dd]imensionless\s+entropy|[Ee]ntropy\s+generation\s+number)[^|]*\|\s*([\d,.]+)\s*\|",
        "entropy_generation": r"\|\s*[Ee]ntropy\s+[Gg]eneration[^|]*\|\s*([\d,.]+)\s*\|",
        "avoidable": r"\|\s*[Aa]voidable[^|]*\|\s*([\d,.]+)\s*\|\s*kW",
        "unavoidable": r"\|\s*[Uu]navoidable[^|]*\|\s*([\d,.]+)\s*\|\s*kW",
    }

    for key, pattern in table_patterns_loose.items():
        if key in values:
            continue
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            try:
                val = float(matches[-1].group(1).replace(",", "."))
                lo, hi = valid_ranges.get(key, (0, 1e9))
                if lo <= val <= hi:
                    values[key] = val
            except ValueError:
                pass

    # === PHASE 3: Inline extraction ===
    inline_patterns = {
        "exergy_in": [
            r"Ėx_in\s*=\s*([\d,.]+)\s*kW",
            r"Ex_in\s*=\s*([\d,.]+)\s*kW",
            r"[Ee]lectrical\s+power\s+input\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_out": [
            r"Ėx_out\s*=\s*([\d,.]+)\s*kW",
            r"Ex_out\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_destroyed": [
            r"Ėx_d\s*=\s*(-?[\d,.]+)\s*kW",
            r"Ex_d\s*=\s*(-?[\d,.]+)\s*kW",
        ],
        "efficiency": [
            r"η_?ex\s*=\s*([\d,.]+)\s*%",
            r"[Ee]xergy\s+[Ee]fficiency\s*=\s*([\d,.]+)\s*%",
        ],
        "entropy_generation": [
            r"[SṠ]_gen\s*=\s*([\d,.]+)\s*kW/K",
            r"Ṡ_gen\s*=\s*([\d,.]+)\s*kW/K",
            r"[SṠ]_gen.*=\s*([\d,.]+)\s*kW/K",
        ],
        "bejan_number": [
            r"N_s\s*=\s*([\d,.]+)(?:\s*$|\s+[^/]|\s*\n)",
            r"N_s\s*=\s*[\d,.]+\s*/\s*[\d,.]+\s*=\s*([\d,.]+)",
        ],
        "f_factor": [
            r"f[_-]?factor\s*=\s*([\d,.]+)(?:\s|$|\n)",
        ],
        "avoidable": [
            r"I_AV\s*=\s*([\d,.]+)\s*kW",
            r"Ėx_d,AV\s*=\s*([\d,.]+)\s*kW",
        ],
        "unavoidable": [
            r"I_UN\s*=\s*([\d,.]+)\s*kW",
            r"Ėx_d,UN\s*=\s*([\d,.]+)\s*kW",
        ],
    }

    for key, pattern_list in inline_patterns.items():
        if key in values:
            continue

        lo, hi = valid_ranges.get(key, (0, 1e9))

        for pattern in pattern_list:
            matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
            valid_matches = []
            for m in matches:
                try:
                    val = float(m.group(1).replace(",", "."))
                    if lo <= val <= hi:
                        valid_matches.append(val)
                except ValueError:
                    pass

            if valid_matches:
                values[key] = valid_matches[-1]
                break

    return values


# ============================================================
# BATCH QUALITY CHECK
# ============================================================

def batch_quality_check(dataset_path: str) -> dict:
    """
    Run quality checks on an entire dataset file.
    Returns summary statistics.
    """
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    results = {
        "total": len(dataset),
        "passed": 0,
        "failed": 0,
        "unverifiable": 0,
        "errors_by_type": {},
    }

    for i, example in enumerate(dataset):
        qr = check_example(example)
        if qr.passed:
            results["passed"] += 1
        elif any(v is False for v in qr.checks.values()):
            results["failed"] += 1
            for err in qr.errors:
                err_type = err.split(":")[0]
                results["errors_by_type"][err_type] = results["errors_by_type"].get(err_type, 0) + 1
        else:
            results["unverifiable"] += 1

    results["pass_rate"] = results["passed"] / results["total"] * 100 if results["total"] > 0 else 0

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        summary = batch_quality_check(sys.argv[1])
        print(f"\n📊 Quality Check Summary for {sys.argv[1]}")
        print(f"   Total examples: {summary['total']}")
        print(f"   ✅ Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   ❓ Unverifiable: {summary['unverifiable']}")
        if summary["errors_by_type"]:
            print(f"\n   Error breakdown:")
            for err_type, count in sorted(summary["errors_by_type"].items(), key=lambda x: -x[1]):
                print(f"     {err_type}: {count}")
    else:
        print("Usage: python quality.py <dataset.json>")
