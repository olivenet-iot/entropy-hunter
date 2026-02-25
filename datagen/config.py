"""
EntropyHunter — Data Generation Configuration

Connects to ExergyLab's knowledge base and engine constants
without copying them into this repo.
"""

import os
from pathlib import Path

# === ExergyLab Integration ===
# Set EXERGYLAB_PATH env var or use default sibling directory
EXERGYLAB_PATH = Path(os.environ.get("EXERGYLAB_PATH", "../exergy-lab"))
KNOWLEDGE_DIR = EXERGYLAB_PATH / "knowledge"
SKILLS_DIR = EXERGYLAB_PATH / "skills"
ENGINE_DIR = EXERGYLAB_PATH / "engine"

# === API Configuration ===
# Teacher model for synthetic data generation
TEACHER_MODEL = os.environ.get("TEACHER_MODEL", "claude-opus-4-6")
TEACHER_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Fallback: use Claude Code CLI subprocess
USE_CLI = os.environ.get("USE_CLI", "false").lower() == "true"

# === Generation Settings ===
MAX_CONCURRENT_REQUESTS = 5
REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3
TIMEOUT_SECONDS = 120

# === Output Paths ===
DATA_DIR = Path("data")
DATA_V01_DIR = DATA_DIR / "v0.1"
DATA_REJECTED_DIR = DATA_DIR / "rejected"

# === Dead State (Global Reference) ===
DEAD_STATE = {
    "T0_K": 298.15,
    "T0_C": 25.0,
    "P0_kPa": 101.325,
}

# === Quality Thresholds ===
QUALITY = {
    "energy_balance_tolerance_pct": 1.0,  # max 1% deviation
    "min_efficiency_pct": 0.1,
    "max_efficiency_pct": 99.9,
    "min_exergy_destroyed_kW": 0.0,  # second law: S_gen >= 0
    "gouy_stodola_tolerance_pct": 2.0,
    "bejan_number_range": (0.0, 1.0),
    "f_factor_range": (0.0, 1.0),
}

# === Version Targets ===
TARGETS = {
    "v0.1": {
        "total_examples": 800,
        "analysis_types": ["basic_exergy", "exergoeconomic", "entropy_generation",
                           "avoidable_unavoidable", "whatif_comparison", "hotspot_detection"],
    },
    "v0.2": {
        "total_examples": 3000,
        "analysis_types": "all_primary",
    },
}


def validate_exergylab_path():
    """Check that ExergyLab is accessible."""
    if not EXERGYLAB_PATH.exists():
        print(f"⚠️  ExergyLab not found at {EXERGYLAB_PATH}")
        print(f"   Set EXERGYLAB_PATH env var or clone exergy-lab as sibling directory")
        return False

    checks = {
        "knowledge/": KNOWLEDGE_DIR.exists(),
        "skills/": SKILLS_DIR.exists(),
        "engine/": ENGINE_DIR.exists(),
    }

    all_ok = all(checks.values())
    for path, exists in checks.items():
        status = "✅" if exists else "❌"
        print(f"  {status} {path}")

    if all_ok:
        knowledge_count = sum(1 for _ in KNOWLEDGE_DIR.rglob("*.md"))
        skill_count = sum(1 for _ in SKILLS_DIR.rglob("*.md"))
        print(f"\n  📚 Knowledge files: {knowledge_count}")
        print(f"  🎯 Skill files: {skill_count}")

    return all_ok


if __name__ == "__main__":
    print(f"ExergyLab path: {EXERGYLAB_PATH.resolve()}")
    print(f"Teacher model: {TEACHER_MODEL}")
    print()
    validate_exergylab_path()
