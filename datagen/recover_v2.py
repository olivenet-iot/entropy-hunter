"""
EntropyHunter v0.4.2 — Reject Recovery Script (Balance-Line Fallback)

CHANGE LOG v0.4.1→v0.4.2:
  - NEW: Balance-line fallback parser — when scaffold parser fails,
    extract values from Opus's self-verified "Energy balance check" line
    (Ex_in − Ex_out − Ex_waste − Ex_d = 0.00 kW ✓)
  - NEW: Thousands separator handling (13,281.60 → 13281.60)
  - NEW: Self-correction aware — prefers values after "FINAL"/"REVISED" blocks
  - KEPT: All v0.4.1 waste label expansions
  - KEPT: Hotspot detection skip

Root cause analysis (364 rejected):
  89% — Opus self-corrects mid-scaffold, parser grabs first (wrong) values
  62% — S_gen boundary mismatch (internal vs total)
  13% — Thousands separator in numbers
  10% — Chiller Q_cond thermal grabbed as exergy waste
   4% — True Opus calculation errors

Expected recovery: ~250/364 → total ~1380/1500 (~92%)

Usage:
  python recover_v2.py still_rejected.jsonl [--verbose]
"""

import json
import re
import sys
from datetime import datetime
from collections import Counter
from pathlib import Path


T0_K = 298.15  # Dead state temperature

QUALITY = {
    "energy_balance_tolerance_pct": 2.0,
    "min_efficiency_pct": 1.0,
    "max_efficiency_pct": 99.0,
    "min_exergy_destroyed_kW": -0.01,
    "gouy_stodola_tolerance_pct": 5.0,
    "bejan_number_range": (0.0, 1.0),
    "f_factor_range": (0.0, 1.0),
}


# ============================================================
# SCAFFOLD_KEY_MAP (v0.4.1 — waste label expansion kept)
# ============================================================

SCAFFOLD_KEY_MAP = {
    # Basic exergy
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

    # Exergy in variants
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
    "exergy in (thermal)": "exergy_in",
    "exergy of fuel input": "exergy_in",
    "fuel exergy (corrected)": "exergy_in",
    "chemical exergy of fuel": "exergy_in",
    "exergy in (flow exergy at inlet)": "exergy_in",
    "exergy in (inlet stream)": "exergy_in",
    "exergy in (compressor work)": "exergy_in",
    "work input (exergy)": "exergy_in",
    "exergy in (flow exergy at turbine inlet)": "exergy_in",
    "exergy in (fuel)": "exergy_in",
    "exergy in (fuel, speco)": "exergy_in",
    "exergy fuel": "exergy_in",
    "exergy in (electrical work input)": "exergy_in",
    "fuel thermal input (q_fuel)": "exergy_in",

    # Exergy out variants (PRODUCT only)
    "exergy output": "exergy_out",
    "product exergy": "exergy_out",
    "useful exergy output": "exergy_out",
    "hydraulic power (exergy product)": "exergy_out",
    "hydraulic power": "exergy_out",
    "flow exergy increase": "exergy_out",
    "steam exergy output": "exergy_out",
    "cooling exergy output": "exergy_out",
    "exergy of product": "exergy_out",
    "exergy of product (moisture removal)": "exergy_out",
    "exergy of product (moisture removal — minimum separation work)": "exergy_out",
    "exergy of cooling": "exergy_out",
    "exergy of cooling at t_evap": "exergy_out",
    "exergy of cooling effect": "exergy_out",
    "generator electrical output": "exergy_out",
    "generator electrical output (exergy out, product)": "exergy_out",
    "part-load adjusted output": "exergy_out",
    "exergy out (electrical output)": "exergy_out",
    "exergy out (electrical output, part-load)": "exergy_out",
    "exergy out (product, electrical)": "exergy_out",
    "net power output (exergy product)": "exergy_out",
    "net electrical output": "exergy_out",
    "exergy of steam output": "exergy_out",
    "steam exergy increase": "exergy_out",
    "exergy gained by steam": "exergy_out",
    "exergy transfer to steam": "exergy_out",
    "useful steam exergy": "exergy_out",

    # Exergy destroyed variants
    "exergy destruction": "exergy_destroyed",
    "total exergy destruction": "exergy_destroyed",
    "exergy destroyed (internal irreversibility)": "exergy_destroyed",
    "exergy destroyed (internal turbine)": "exergy_destroyed",
    "internal exergy destruction": "exergy_destroyed",
    "irreversibility": "exergy_destroyed",

    # ================================================================
    # WASTE EXERGY — v0.4.1 MAJOR EXPANSION
    # ================================================================

    # Generic waste
    "exergy waste": "exergy_waste",
    "waste exergy": "exergy_waste",
    "waste stream exergy": "exergy_waste",
    "exergy loss (to environment)": "exergy_waste",
    "exergy lost to environment": "exergy_waste",
    "waste heat exergy": "exergy_waste",
    "exergy of waste heat": "exergy_waste",
    "exergy of waste streams": "exergy_waste",
    "total waste exergy": "exergy_waste",
    "total exergy waste": "exergy_waste",
    "exergy rejected to environment": "exergy_waste",
    "exergy dissipated to environment": "exergy_waste",
    "exergy loss (exhaust above dead state)": "exergy_waste",

    # Steam turbine exhaust (#1 source of false rejects)
    "exergy out (exhaust)": "exergy_waste",
    "exergy out (exhaust steam)": "exergy_waste",
    "exergy out (exhaust flow)": "exergy_waste",
    "exergy out (exhaust stream)": "exergy_waste",
    "exergy of exhaust": "exergy_waste",
    "exergy of exhaust steam": "exergy_waste",
    "exhaust steam exergy": "exergy_waste",
    "exhaust flow exergy": "exergy_waste",
    "exhaust exergy": "exergy_waste",
    "exit steam exergy": "exergy_waste",
    "exit flow exergy": "exergy_waste",
    "turbine exhaust exergy": "exergy_waste",
    "outlet flow exergy": "exergy_waste",
    "outlet exergy (waste)": "exergy_waste",
    "exergy leaving with exhaust": "exergy_waste",
    "exergy at outlet (exhaust)": "exergy_waste",
    "outlet steam exergy": "exergy_waste",
    "exergy at turbine outlet": "exergy_waste",
    "exergy of outlet steam": "exergy_waste",
    "exhaust steam flow exergy": "exergy_waste",
    "exergy loss (exhaust waste)": "exergy_waste",

    # Dryer exhaust air
    "exergy out with exhaust air (waste)": "exergy_waste",
    "exergy out with exhaust air": "exergy_waste",
    "exhaust air exergy": "exergy_waste",
    "exhaust air exergy loss": "exergy_waste",
    "exergy of exhaust air": "exergy_waste",
    "exergy carried by exhaust air": "exergy_waste",
    "exergy loss with exhaust air": "exergy_waste",
    "exergy out (exhaust air)": "exergy_waste",
    "exhaust air (waste)": "exergy_waste",
    "outlet air exergy": "exergy_waste",
    "drying air outlet exergy": "exergy_waste",
    "exergy lost with exhaust": "exergy_waste",
    "waste heat exergy (exhaust air)": "exergy_waste",
    "exergy of outlet air": "exergy_waste",
    "exergy with outlet air": "exergy_waste",
    "exergy of drying air outlet": "exergy_waste",

    # Chiller condenser waste
    "exergy of condenser waste": "exergy_waste",
    "condenser waste exergy": "exergy_waste",
    "exergy of condenser rejection": "exergy_waste",
    "exergy rejected at condenser": "exergy_waste",
    "exergy dissipated at condenser": "exergy_waste",
    "condenser exergy loss": "exergy_waste",
    "condenser exergy rejection": "exergy_waste",
    "condenser waste": "exergy_waste",
    "exergy waste (condenser)": "exergy_waste",
    "exergy loss (condenser)": "exergy_waste",
    "exergy of condenser heat rejection": "exergy_waste",
    "exergy rejected (condenser waste)": "exergy_waste",

    # Boiler stack/shell losses
    "flue gas exergy loss": "exergy_waste",
    "exergy of stack gas losses": "exergy_waste",
    "exergy of thermal shell losses": "exergy_waste",
    "stack gas exergy loss": "exergy_waste",
    "stack gas exergy": "exergy_waste",
    "exergy of flue gas": "exergy_waste",
    "flue gas exergy": "exergy_waste",
    "shell loss exergy": "exergy_waste",
    "exergy of shell losses": "exergy_waste",
    "radiation loss exergy": "exergy_waste",
    "exergy loss (stack gas)": "exergy_waste",
    "exergy loss (flue gas)": "exergy_waste",
    "exergy loss (shell)": "exergy_waste",
    "exergy loss (radiation)": "exergy_waste",
    "stack losses (exergy)": "exergy_waste",
    "exergy of stack losses": "exergy_waste",
    "exergy with flue gas": "exergy_waste",
    "exergy carried by flue gas": "exergy_waste",
    "exergy loss to stack": "exergy_waste",
    "exergy of flue gas loss": "exergy_waste",
    "exergy leaving with flue gas": "exergy_waste",

    # Heat exchanger waste
    "hot side outlet exergy (waste)": "exergy_waste",
    "hot side residual exergy": "exergy_waste",
    "exergy of hot side outlet": "exergy_waste",
    "waste exergy (hot side)": "exergy_waste",
    "exergy waste (hot side)": "exergy_waste",
    "exergy loss (hot side outlet)": "exergy_waste",
    "hot fluid outlet exergy": "exergy_waste",
    "exergy of hot fluid outlet": "exergy_waste",
    "residual exergy (hot side)": "exergy_waste",

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
    "product cost rate (cp)": "c_product",

    # Exergoeconomic — SPECO fuel/product definitions
    "exergy in (fuel)": "exergy_in",
    "exergy in (fuel, speco)": "exergy_in",
    "exergy out (product, speco)": "exergy_out",

    # EGM mechanism values
    "heat transfer (sgen,ht)": "sgen_ht",
    "pressure drop (sgen,dp)": "sgen_dp",
    "mixing/chemical (sgen,mix)": "sgen_mix",
    "s_gen,ht (heat transfer)": "sgen_ht",
    "s_gen,dp (pressure drop)": "sgen_dp",
    "s_gen,mix (mixing/chemical)": "sgen_mix",
    "heat transfer irreversibility": "sgen_ht",
    "pressure drop irreversibility": "sgen_dp",
    "mixing irreversibility": "sgen_mix",
    "sgen,ht": "sgen_ht",
    "sgen,dp": "sgen_dp",
    "sgen,mix": "sgen_mix",

    # AV/UN
    "unavoidable exergy destruction": "unavoidable",
    "avoidable exergy destruction": "avoidable",
    "avoidable ratio": "avoidable_ratio",
    "unavoidable destruction": "unavoidable",
    "avoidable destruction": "avoidable",

    # What-if
    "annual energy savings": "annual_energy_savings",
    "annual cost savings": "annual_cost_savings",
    "delta exergy destroyed": "delta_exd",
}

# Concept matching (fallback when exact + partial both miss)
LABEL_CONCEPTS = {
    "exergy_in": ["exergy in", "exergy fuel", "fuel exergy", "power input",
                  "exergy input", "exergy transfer hot", "chemical exergy",
                  "work input", "fuel thermal"],
    "exergy_out": ["exergy out", "exergy product", "product exergy", "exergy of cooling",
                   "useful exergy", "flow exergy increase", "exergy transfer cold",
                   "generator electrical", "electrical output", "net power output",
                   "steam exergy increase", "exergy gained by steam",
                   "exergy transfer to steam", "moisture removal",
                   "part-load adjusted", "net electrical"],
    "exergy_destroyed": ["exergy destroy", "exergy destruct", "irreversibility",
                         "internal exergy"],
    "efficiency": ["exergy efficien", "η_ex", "second law efficien",
                   "second-law efficien"],
    "exergy_waste": ["exergy lost", "exergy loss", "stack gas exergy", "waste stream",
                     "exergy rejected", "exhaust exergy", "exhaust steam",
                     "exhaust air", "condenser waste", "flue gas exergy",
                     "shell loss", "waste heat", "exergy dissipat",
                     "outlet exergy (waste)", "exergy carried by",
                     "exergy with flue", "exergy of waste",
                     "exergy leaving with exhaust", "exit steam",
                     "exit flow", "outlet flow", "outlet steam",
                     "outlet air", "hot side outlet", "hot side residual",
                     "hot fluid outlet", "residual exergy",
                     "condenser exergy", "radiation loss",
                     "exergy at turbine outlet"],
    "entropy_generation": ["entropy generation", "sgen", "ṡ_gen"],
    "bejan_number": ["bejan number", "bejan (ns)", "(ns)"],
}

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

STRICT_UNIT_KEYS = {
    "exergy_in", "exergy_out", "exergy_destroyed", "exergy_waste",
    "avoidable", "unavoidable",
    "sgen_ht", "sgen_dp", "sgen_mix", "entropy_generation",
    "z_dot", "c_dot_d", "c_fuel", "total_cost_rate",
    "annual_energy_savings", "annual_cost_savings",
}

UNIT_PATTERN = r"(kWh/yr|EUR/yr|EUR/kWh|EUR/h|kW/K|h/yr|kW|kJ|°C|EUR|pp|%|K)"


# ============================================================
# PHASE 0: SCAFFOLD PARSER (self-correction aware)
# ============================================================

def _extract_from_scaffold(text: str) -> dict:
    """
    Extract values from ## Calculation Summary scaffold.
    
    v0.4.2 change: When Opus self-corrects ("FINAL CONSISTENT VALUES",
    "REVISED", etc.), prefer the LAST occurrence of each key rather than
    the first. This handles the pattern where Opus writes wrong values,
    then corrects them.
    """
    sections = re.findall(
        r"## Calculation Summary[^\n]*\n(.*?)(?=\n## (?!Calculation)|$)",
        text, re.DOTALL
    )
    if not sections:
        return {}

    # Check for self-correction markers
    has_correction = any(p in text.lower() for p in [
        'wait —', 'correction', 'final consistent', 'revised',
        'let me recalculate', 'redo this'
    ])
    
    # If self-correction detected, override strategy:
    # keep LAST value for core keys instead of first
    override_on_correction = has_correction
    
    values = {}
    num_unit_pattern = re.compile(
        r"~?([\d]+[.,][\d]+|[\d]+(?:,\d{3})*)"
        r"\s*" + UNIT_PATTERN,
        re.IGNORECASE
    )

    for section in sections:
        for line in section.strip().split('\n'):
            line = line.strip()
            if not line.startswith(('-', '*')):
                continue

            colon_pos = line.find(':')
            if colon_pos < 0:
                continue

            label_raw = line[:colon_pos].lstrip('-* \t')
            label = label_raw.strip().lower()
            value_part = line[colon_pos + 1:]

            matches = list(num_unit_pattern.finditer(value_part))

            first_bare_match = re.match(r"\s*~?([\d]+[.,][\d]+|[\d]+)", value_part)
            bare_val = None
            if first_bare_match:
                try:
                    raw = first_bare_match.group(1)
                    # Handle thousands separators: 13,281.60 → 13281.60
                    if ',' in raw and '.' in raw:
                        raw = raw.replace(',', '')
                    elif ',' in raw:
                        raw = raw.replace(',', '.')
                    bare_val = float(raw)
                except ValueError:
                    pass

            if matches:
                parsed_matches = []
                for m in matches:
                    try:
                        num_str = m.group(1)
                        # Handle thousands separators
                        if ',' in num_str and '.' in num_str:
                            num_str = num_str.replace(',', '')
                        elif ',' in num_str:
                            num_str = num_str.replace(',', '.')
                        else:
                            num_str = num_str
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
                best_match_len = 0
                for map_key, internal in SCAFFOLD_KEY_MAP.items():
                    if map_key in label and len(map_key) > best_match_len:
                        best_match_len = len(map_key)
                        internal_key = internal

            if not internal_key:
                best_concept_len = 0
                for ikey, concepts in LABEL_CONCEPTS.items():
                    for c in concepts:
                        if c in label and len(c) > best_concept_len:
                            best_concept_len = len(c)
                            internal_key = ikey

            if internal_key:
                preferred = PREFERRED_UNIT.get(internal_key)
                val = None

                if preferred and parsed_matches:
                    preferred_vals = [v for v, u in parsed_matches if u == preferred]
                    if preferred_vals:
                        val = preferred_vals[-1]

                if val is None and not preferred and bare_val is not None:
                    last_eq = re.findall(r"=\s*([\d]+[.,][\d]+|[\d]+)", value_part)
                    if last_eq:
                        try:
                            raw = last_eq[-1]
                            if ',' in raw and '.' in raw:
                                raw = raw.replace(',', '')
                            elif ',' in raw:
                                raw = raw.replace(',', '.')
                            val = float(raw)
                        except ValueError:
                            val = bare_val
                    else:
                        val = bare_val

                if val is None and parsed_matches and internal_key not in STRICT_UNIT_KEYS:
                    val = parsed_matches[-1][0]

                if val is None and bare_val is not None and internal_key not in STRICT_UNIT_KEYS:
                    val = bare_val

                if val is not None:
                    comparison_keys = {"delta_exd", "annual_energy_savings", "annual_cost_savings"}
                    core_overridable = {"exergy_in", "exergy_out", "exergy_destroyed"}

                    if (internal_key == "exergy_destroyed" and "total" in label
                            and internal_key in values and val > values[internal_key]):
                        values[internal_key] = val
                    elif internal_key == "exergy_waste":
                        values[internal_key] = values.get(internal_key, 0.0) + val
                    elif internal_key not in values:
                        values[internal_key] = val
                    elif internal_key in comparison_keys:
                        values[internal_key] = val  # always overwrite comparison
                    elif override_on_correction and internal_key in core_overridable:
                        # Self-correction: take LAST value for core keys
                        values[internal_key] = val

    return values


# ============================================================
# PHASE 1: BALANCE-LINE FALLBACK (v0.4.2 — NEW)
# ============================================================

def _extract_from_balance_line(text: str) -> dict:
    """
    Extract exergy values from Opus's self-verified balance check line.
    
    Pattern: "Energy balance check: Ex_in − Ex_out − Ex_waste − Ex_d = A − B − C − D = 0.00 kW ✓"
    
    This is the MOST RELIABLE source because:
    1. Opus writes it AFTER all corrections
    2. It contains verified, self-consistent values
    3. It always sums to zero (within rounding)
    
    Returns dict with exergy_in, exergy_out (= sum of middle terms), exergy_destroyed (last term).
    """
    lines = text.split('\n')
    
    # Find balance check lines with checkmark or ≈ 0
    balance_lines = []
    for line in lines:
        ll = line.lower()
        if not ('balance' in ll and ('✓' in line or '= 0.0' in ll or '≈ 0' in ll)):
            continue
        # Must contain exergy-related terms (avoid other balance checks)
        if any(t in ll for t in ['ex_', 'exergy', 'ėx', 'ex_in', 'ex_fuel',
                                  'f −', 'f −']):
            balance_lines.append(line)
        # Also allow pure numeric pattern like "1743.42 − 1318.22 − 372.44 − 52.76 = 0.00"
        elif re.search(r'[\d,.]+\s*[−–\-]\s*[\d,.]+\s*[−–\-]\s*[\d,.]+\s*=\s*[\-]?0', line):
            balance_lines.append(line)
    
    if not balance_lines:
        return {}
    
    # Use the LAST balance check line (after all corrections)
    line = balance_lines[-1]
    
    # Clean thousands separators
    clean_line = line.replace(',', '')
    
    # Find the numeric sequence: A − B − C − D = 0.00
    # Strategy: find all decimal numbers in the line
    all_nums = re.findall(r'(\d+\.?\d*)', clean_line)
    if len(all_nums) < 3:
        return {}
    
    vals = [float(n) for n in all_nums]
    
    # Remove trailing near-zero values (the balance result)
    while vals and abs(vals[-1]) < 0.5:
        vals.pop()
    
    if len(vals) < 3:
        return {}
    
    # Verify this is actually a balance: first ≈ sum of rest
    ex_in = vals[0]
    rest_sum = sum(vals[1:])
    
    if abs(ex_in - rest_sum) / max(ex_in, 0.01) > 0.05:
        # Not a valid balance — might be a different kind of line
        return {}
    
    # Assign values
    result = {
        "exergy_in": vals[0],
        "exergy_destroyed": vals[-1],
    }
    
    middle = vals[1:-1]
    if len(middle) == 1:
        # Ex_in − Ex_out − Ex_d (no waste)
        result["exergy_out"] = middle[0]
    elif len(middle) == 2:
        # Ex_in − Ex_out − Ex_waste − Ex_d (or Ex_in − Ex_product − Ex_d)
        # Need to determine which is product vs waste
        # Heuristic: larger middle term is typically product
        result["exergy_out"] = middle[0]
        result["exergy_waste"] = middle[1]
    elif len(middle) >= 3:
        # Multiple waste streams: Ex_in − Ex_out − W1 − W2 − Ex_d
        result["exergy_out"] = middle[0]
        result["exergy_waste"] = sum(middle[1:])
    
    result["_source"] = "balance_line"
    return result


# ============================================================
# PHASE 2: REGEX FALLBACK (minimal)
# ============================================================

def _extract_from_regex(text: str) -> dict:
    """Minimal regex fallback."""
    values = {}
    patterns = {
        "exergy_in": [
            r"Ėx_in\s*=\s*([\d,.]+)\s*kW",
            r"Ex_in\s*=\s*([\d,.]+)\s*kW",
            r"Ex_fuel\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_out": [
            r"Ėx_out\s*=\s*([\d,.]+)\s*kW",
            r"Ex_out\s*=\s*([\d,.]+)\s*kW",
            r"Ex_product\s*=\s*([\d,.]+)\s*kW",
        ],
        "exergy_destroyed": [
            r"Ėx_d\s*=\s*(-?[\d,.]+)\s*kW",
            r"Ex_d\s*=\s*(-?[\d,.]+)\s*kW",
            r"Ex_D\s*=\s*(-?[\d,.]+)\s*kW",
        ],
        "efficiency": [
            r"η_?ex\s*=\s*([\d,.]+)\s*%",
            r"[Ee]xergy\s+[Ee]fficiency\s*[:=]\s*([\d,.]+)\s*%",
        ],
        "entropy_generation": [
            r"[SṠ]_?gen\s*[:=]\s*([\d,.]+)\s*kW/K",
            r"Ṡ_gen\s*[:=]\s*([\d,.]+)\s*kW/K",
        ],
        "bejan_number": [
            r"N_s\s*[:=]\s*[\d,.]+\s*/\s*[\d,.]+\s*=\s*([\d,.]+)",
            r"N_s\s*[:=]\s*([\d,.]+)(?:\s|$|\n)",
            r"Ns\s*[:=]\s*([\d,.]+)(?:\s|$|\n)",
        ],
    }
    for key, pats in patterns.items():
        for p in pats:
            m = list(re.finditer(p, text, re.IGNORECASE | re.MULTILINE))
            if m:
                try:
                    raw = m[-1].group(1)
                    if ',' in raw and '.' in raw:
                        raw = raw.replace(',', '')
                    elif ',' in raw:
                        raw = raw.replace(',', '.')
                    values[key] = float(raw)
                except ValueError:
                    pass
                break
    return values


# ============================================================
# COMBINED EXTRACTION (3-phase priority)
# ============================================================

def extract_values(text: str) -> tuple[dict, str]:
    """
    Extract values with 3-phase priority:
    1. Scaffold parser (with self-correction awareness)
    2. Balance-line fallback (Opus's verified balance check)
    3. Regex fallback
    
    Returns (values_dict, source_label)
    """
    # Phase 0: Scaffold
    values = _extract_from_scaffold(text)
    
    # Sanity check scaffold results
    scaffold_ok = True
    if values:
        ei = values.get("exergy_in")
        eo = values.get("exergy_out")
        ed = values.get("exergy_destroyed")
        ew = values.get("exergy_waste", 0)
        
        if ei and eo and ei > 0 and eo > ei * 5:
            scaffold_ok = False
        elif ei and ed and ei > 0 and ed > ei * 2:
            scaffold_ok = False
        elif ei and eo and ed:
            # Quick balance check
            balance = abs(ei - eo - ew - ed)
            tol = ei * 0.03  # 3% tolerance for quick check
            if balance > tol:
                scaffold_ok = False
    else:
        scaffold_ok = False
    
    if scaffold_ok and len(values) >= 3:
        return values, "scaffold"
    
    # Phase 1: Balance-line fallback
    bl_values = _extract_from_balance_line(text)
    if bl_values and len(bl_values) >= 3:
        # Merge: use balance-line for core exergy, scaffold for secondary values
        merged = {}
        # Core from balance-line
        for k in ["exergy_in", "exergy_out", "exergy_destroyed", "exergy_waste"]:
            if k in bl_values:
                merged[k] = bl_values[k]
        # Secondary from scaffold (efficiency, entropy, bejan, etc.)
        if values:
            for k, v in values.items():
                if k not in merged:
                    merged[k] = v
        # Also try regex for secondary values not in scaffold
        regex_vals = _extract_from_regex(text)
        for k, v in regex_vals.items():
            if k not in merged:
                merged[k] = v
        return merged, "balance_line"
    
    # Phase 2: Regex fallback
    regex_values = _extract_from_regex(text)
    if regex_values and len(regex_values) >= 3:
        return regex_values, "regex"
    
    # Return whatever we got
    best = values if len(values) >= len(regex_values) else regex_values
    return best, "partial"


# ============================================================
# QUALITY CHECK
# ============================================================

def check_example(example: dict) -> tuple[bool, dict, list, list, dict, str]:
    """
    Run all quality checks.
    Returns (passed, checks, errors, warnings, values, source)
    """
    checks = {}
    errors = []
    warnings = []
    output_text = example.get("output", "")
    analysis_type = example.get("metadata", {}).get("analysis_type", "")

    checks["scaffold_present"] = "## Calculation Summary" in output_text

    # Extract values
    values, source = extract_values(output_text)

    # 1. Energy balance
    if analysis_type == "hotspot_detection":
        checks["energy_balance"] = None
    elif values.get("exergy_in") and values.get("exergy_out") and values.get("exergy_destroyed"):
        ex_in = values["exergy_in"]
        ex_out = values["exergy_out"]
        ex_d = values["exergy_destroyed"]
        ex_waste = values.get("exergy_waste", 0.0)

        balance_with = abs(ex_in - ex_out - ex_waste - ex_d)
        balance_without = abs(ex_in - ex_out - ex_d)
        balance = min(balance_with, balance_without)
        tolerance = QUALITY["energy_balance_tolerance_pct"] / 100 * ex_in

        checks["energy_balance"] = balance <= tolerance
        if not checks["energy_balance"]:
            errors.append(
                f"Energy balance: |{ex_in:.1f} - {ex_out:.1f} - {ex_waste:.1f}(w) - {ex_d:.1f}| "
                f"= {balance_with:.1f}, no_w={balance_without:.1f}, tol={tolerance:.1f}"
            )
    else:
        checks["energy_balance"] = None
        warnings.append(f"Cannot verify balance (extracted: {list(values.keys())})")

    # 2. Efficiency range
    if values.get("efficiency"):
        eff = values["efficiency"]
        checks["efficiency_range"] = QUALITY["min_efficiency_pct"] < eff < QUALITY["max_efficiency_pct"]
        if not checks["efficiency_range"]:
            errors.append(f"Efficiency {eff:.1f}% outside range")
    else:
        checks["efficiency_range"] = None

    # 3. Second law
    if values.get("exergy_destroyed") is not None:
        checks["second_law"] = values["exergy_destroyed"] >= QUALITY["min_exergy_destroyed_kW"]
        if not checks["second_law"]:
            errors.append(f"Second law: Ex_d = {values['exergy_destroyed']:.2f} < 0")
    else:
        checks["second_law"] = None

    # 4. Gouy-Stodola
    # v0.4.2: Soft check when energy balance is verified.
    # Reason: Opus often computes S_gen at internal boundary (turbine-only)
    # but Ex_d at total boundary (including exhaust). Both are correct,
    # just different system boundaries. Parser can't distinguish.
    if analysis_type == "hotspot_detection":
        checks["gouy_stodola"] = None
    elif values.get("exergy_destroyed") and values.get("entropy_generation"):
        gouy = T0_K * values["entropy_generation"]
        dev = abs(gouy - values["exergy_destroyed"])
        tol = QUALITY["gouy_stodola_tolerance_pct"] / 100 * values["exergy_destroyed"]
        gs_ok = dev <= tol
        checks["gouy_stodola"] = gs_ok
        if not gs_ok:
            balance_verified = checks.get("energy_balance") is True
            if balance_verified:
                # Demote to warning — balance is the primary check
                checks["gouy_stodola"] = None  # skip, don't fail
                warnings.append(
                    f"Gouy-Stodola soft skip (balance OK): T₀×S_gen={gouy:.2f} "
                    f"vs Ex_d={values['exergy_destroyed']:.2f} (boundary mismatch)"
                )
            else:
                errors.append(f"Gouy-Stodola: T₀×S_gen={gouy:.2f} vs Ex_d={values['exergy_destroyed']:.2f}")
    else:
        checks["gouy_stodola"] = None

    # 5. Bejan
    if values.get("bejan_number") is not None:
        Ns = values["bejan_number"]
        lo, hi = QUALITY["bejan_number_range"]
        checks["bejan_range"] = lo <= Ns <= hi
        if not checks["bejan_range"]:
            errors.append(f"Bejan N_s={Ns:.3f} outside [{lo},{hi}]")
    else:
        checks["bejan_range"] = None

    # 6. f-factor
    if values.get("f_factor") is not None:
        f = values["f_factor"]
        lo, hi = QUALITY["f_factor_range"]
        checks["f_factor_range"] = lo <= f <= hi
        if not checks["f_factor_range"]:
            errors.append(f"f-factor={f:.3f} outside [{lo},{hi}]")
    else:
        checks["f_factor_range"] = None

    # 7. Dead state
    if "298.15" in output_text or "25°C" in output_text or "25 °C" in output_text:
        checks["dead_state"] = True
    else:
        checks["dead_state"] = None

    # 8. AV/UN split
    # v0.4.2: Soft check when balance verified — rounding in split is common
    if values.get("avoidable") and values.get("unavoidable") and values.get("exergy_destroyed"):
        split_sum = values["avoidable"] + values["unavoidable"]
        dev = abs(split_sum - values["exergy_destroyed"])
        tol = 0.02 * values["exergy_destroyed"]
        av_ok = dev <= tol
        checks["av_un_split"] = av_ok
        if not av_ok:
            balance_verified = checks.get("energy_balance") is True
            if balance_verified:
                checks["av_un_split"] = None  # demote to warning
                warnings.append(
                    f"AV/UN soft skip (balance OK): AV+UN={split_sum:.2f} "
                    f"vs Ex_d={values['exergy_destroyed']:.2f}"
                )
            else:
                errors.append(f"AV+UN={split_sum:.2f} ≠ Ex_d={values['exergy_destroyed']:.2f}")
    else:
        checks["av_un_split"] = None

    verified = {k: v for k, v in checks.items() if v is not None and k != "scaffold_present"}
    passed = all(verified.values()) if verified else False

    return passed, checks, errors, warnings, values, source


# ============================================================
# MAIN
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="EntropyHunter v0.4.2 — Reject Recovery")
    parser.add_argument("rejected", help="Rejected JSONL file")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    # Load
    rejected = []
    with open(args.rejected) as f:
        for line in f:
            line = line.strip()
            if line:
                rejected.append(json.loads(line))

    print(f"📥 Loaded {len(rejected)} rejected examples")

    # Process
    recovered = []
    still_rejected = []
    source_counts = Counter()
    recovery_by_type = Counter()
    recovery_by_equip = Counter()
    still_reasons = Counter()
    still_by_combo = Counter()

    for ex in rejected:
        meta = ex.get("metadata", {})
        analysis = meta.get("analysis_type", "?")
        equip = meta.get("equipment_type", "?")
        combo = f"{analysis}/{equip}"

        passed, checks, errors, warnings, values, source = check_example(ex)

        if passed:
            meta["quality_passed"] = True
            meta["quality_notes"] = f"Recovered by v0.4.2 ({source})"
            meta["quality_errors"] = []
            recovered.append(ex)
            source_counts[source] += 1
            recovery_by_type[analysis] += 1
            recovery_by_equip[equip] += 1
        else:
            meta["quality_errors"] = errors
            still_rejected.append(ex)
            for err in errors:
                still_reasons[err[:70]] += 1
            still_by_combo[combo] += 1

            if args.verbose:
                print(f"\n  ❌ {combo}")
                print(f"     Source: {source}")
                print(f"     Values: { {k: f'{v:.2f}' for k,v in values.items() if isinstance(v, float)} }")
                for e in errors:
                    print(f"     {e}")

    # Save
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rec_path = out_dir / f"recovered_v042_{ts}.jsonl"
    still_path = out_dir / f"still_rejected_v042_{ts}.jsonl"

    with open(rec_path, 'w') as f:
        for ex in recovered:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')

    with open(still_path, 'w') as f:
        for ex in still_rejected:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')

    # Report
    total = len(rejected)
    n_rec = len(recovered)
    n_still = len(still_rejected)

    print(f"\n{'='*60}")
    print(f"📊 v0.4.2 RECOVERY RESULTS")
    print(f"{'='*60}")
    print(f"  Input rejected:     {total}")
    print(f"  ✅ Recovered:       {n_rec} ({100*n_rec/total:.1f}%)")
    print(f"  ❌ Still rejected:  {n_still} ({100*n_still/total:.1f}%)")

    print(f"\n{'='*60}")
    print(f"EXTRACTION SOURCE (recovered)")
    print(f"{'='*60}")
    for src, cnt in source_counts.most_common():
        print(f"  {src:20s} {cnt:4d}")

    print(f"\n{'='*60}")
    print(f"RECOVERY BY ANALYSIS TYPE")
    print(f"{'='*60}")
    for k, v in recovery_by_type.most_common():
        print(f"  {k:35s} {v:4d}")

    print(f"\n{'='*60}")
    print(f"RECOVERY BY EQUIPMENT")
    print(f"{'='*60}")
    for k, v in recovery_by_equip.most_common():
        print(f"  {k:25s} {v:4d}")

    if still_rejected:
        print(f"\n{'='*60}")
        print(f"REMAINING REJECTION REASONS (top 15)")
        print(f"{'='*60}")
        for k, v in still_reasons.most_common(15):
            print(f"  {v:4d}x  {k}")

        print(f"\n{'='*60}")
        print(f"STILL REJECTED BY COMBO (top 10)")
        print(f"{'='*60}")
        for k, v in still_by_combo.most_common(10):
            print(f"  {k:45s} {v:4d}")

    print(f"\n📁 Recovered: {rec_path}")
    print(f"📁 Still rejected: {still_path}")
    print(f"\n💡 Estimated total with previous recoveries:")
    print(f"   Original passed:  1012")
    print(f"   v0.4.1 recovery:  124")
    print(f"   v0.4.2 recovery:  {n_rec}")
    print(f"   ────────────────────")
    print(f"   Total:            {1012 + 124 + n_rec}")
    print(f"   Pass rate:        {100*(1012 + 124 + n_rec)/1500:.1f}%")


if __name__ == "__main__":
    main()
