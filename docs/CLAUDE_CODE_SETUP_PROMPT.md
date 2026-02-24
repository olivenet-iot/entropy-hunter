# Claude Code Agent Prompt — EntropyHunter GitHub Setup

Give the following prompt to the Claude Code agent (home/ubuntu):

---

## PROMPT:

Create a GitHub repo for the EntropyHunter-7B project and push it. Files are ready at `/path/to/entropy-hunter/`.

Steps:

1. Create a PUBLIC repo named `entropy-hunter` on GitHub (using GitHub CLI):
```bash
cd /path/to/entropy-hunter
gh repo create entropy-hunter --public --description "The world's first open-source fine-tuned model for industrial exergy analysis and entropy generation detection" --source . --push
```

If `gh` is not installed:
```bash
sudo apt install gh
gh auth login
```

2. Git init and first commit:
```bash
cd /path/to/entropy-hunter
git init
git add .
git commit -m "feat: initial project structure — taxonomy, datagen pipeline, quality checks

EntropyHunter-7B: Domain-specific LLM for industrial exergy analysis.

Includes:
- Equipment taxonomy (7 types, 48 subtypes) from ExergyLab
- Analysis types taxonomy (14 types across 7 engines)
- Data generation config with ExergyLab integration
- Thermodynamic quality control checks
- Project roadmap and Phase 1 taxonomy documentation
- CLAUDE.md project instructions

Phase 1 (Taxonomy) complete. Ready for Phase 2 (Data Generation)."
```

3. Add remote and push:
```bash
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/entropy-hunter.git
git push -u origin main
```

4. GitHub repo settings:
- Add topics: `exergy-analysis`, `thermodynamics`, `entropy`, `fine-tuning`, `lora`, `industrial-iot`, `energy-efficiency`, `second-law`
- Set About to: "The world's first open-source fine-tuned model for industrial exergy analysis and entropy generation detection. Built on ExergyLab."
- Disable Wiki, enable Issues, enable Discussions

5. Verification:
```bash
# ExergyLab path check
cd /path/to/entropy-hunter
python datagen/config.py
```

This command will verify that ExergyLab's knowledge and skill files are accessible. If not:
```bash
export EXERGYLAB_PATH=/path/to/exergy-lab
```

---

NOTE: Replace `/path/to/entropy-hunter/` and `YOUR_USERNAME` with your own values.
Make sure the ExergyLab repo exists as a sibling directory (`../exergy-lab/`).
