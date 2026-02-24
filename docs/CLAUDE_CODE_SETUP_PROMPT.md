# Claude Code Agent Prompt — EntropyHunter GitHub Setup

Aşağıdaki prompt'u Claude Code ajanına (home/ubuntu) ver:

---

## PROMPT:

EntropyHunter-7B projesi için GitHub repo oluştur ve push et. Dosyalar `/path/to/entropy-hunter/` dizininde hazır.

Adımlar:

1. GitHub'da `entropy-hunter` adında PUBLIC repo oluştur (GitHub CLI ile):
```bash
cd /path/to/entropy-hunter
gh repo create entropy-hunter --public --description "The world's first open-source fine-tuned model for industrial exergy analysis and entropy generation detection" --source . --push
```

Eğer `gh` kurulu değilse:
```bash
sudo apt install gh
gh auth login
```

2. Git init ve ilk commit:
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
- Project roadmap and Faz 1 taxonomy documentation
- CLAUDE.md project instructions

Faz 1 (Taxonomy) complete. Ready for Faz 2 (Data Generation)."
```

3. Remote ekle ve push et:
```bash
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/entropy-hunter.git
git push -u origin main
```

4. GitHub repo ayarları:
- Topics ekle: `exergy-analysis`, `thermodynamics`, `entropy`, `fine-tuning`, `lora`, `industrial-iot`, `energy-efficiency`, `second-law`
- About kısmına yaz: "🔥 The world's first open-source fine-tuned model for industrial exergy analysis and entropy generation detection. Built on ExergyLab."
- Wiki'yi kapat, Issues'ı aç, Discussions'ı aç

5. Doğrulama:
```bash
# ExergyLab path kontrolü
cd /path/to/entropy-hunter
python datagen/config.py
```

Bu komut ExergyLab'ın knowledge ve skill dosyalarını bulabildiğini doğrulayacak. Eğer bulamazsa:
```bash
export EXERGYLAB_PATH=/path/to/exergy-lab
```

---

NOT: `/path/to/entropy-hunter/` ve `YOUR_USERNAME` kısımlarını kendi değerlerinle değiştir.
ExergyLab repo'sunun sibling directory olarak (`../exergy-lab/`) mevcut olduğundan emin ol.
