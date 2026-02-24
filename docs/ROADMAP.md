# EntropyHunter-7B — Proje Yol Haritası

> Endüstriyel sistemlerde exergy yıkımı ve entropi üretimi analizi yapabilen
> dünyanın ilk açık kaynak fine-tuned modeli.

## Vizyon

```
"Her endüstriyel sistemde gizli entropi üretimi var.
 Bu model onu buluyor."
```

EntropyHunter, bir mühendise ekipman parametrelerini verdiğinde:
- Exergy yıkım noktalarını tespit eder
- Entropi üretim mekanizmalarını açıklar
- İyileştirme önerileri sunar
- Termoekonomik maliyet allokasyonu yapar
- Gouy-Stodola bağlantısını kurar

---

## Faz 0: Hazırlık (Hafta 1-2)

### Donanım & Ortam
- [ ] GPU karar ver (aşağıdaki opsiyon tablosuna bak)
- [ ] Unsloth, vLLM, llama.cpp kurulumu
- [ ] HuggingFace organizasyon oluştur: `OlivenetAI` veya `EntropyHunter`
- [ ] Git repo yapısı kur
- [ ] Wandb/MLflow hesabı (eğitim takibi için)

### GPU Opsiyonları
| Opsiyon | Maliyet | Avantaj | Dezavantaj |
|---------|---------|---------|------------|
| RTX 4090 kendi makinen | ~$1600 tek seferlik | Sürekli erişim, başka işlere de kullanırsın | Başlangıç maliyeti |
| Vast.ai / RunPod | ~$0.30-0.50/saat | Hemen başla, commitment yok | Uzun vadede pahalı |
| Lambda Labs A10G | ~$0.60/saat | Daha güçlü, daha hızlı | Daha pahalı |
| Google Colab Pro+ | $50/ay | En ucuz başlangıç | GPU garantisi yok, session limiti |

### Tavsiye
İlk fazlarda Vast.ai veya RunPod ile başla (düşük commitment).
Proje tutarsa RTX 4090 al — hem bu proje hem diğer işler için kullanırsın.

---

## Faz 1: Veri Seti Tasarımı (Hafta 2-4)

> BU FAZ EN KRİTİK FAZ. Model kalitesinin %80'i veri kalitesinden gelir.
> Senin domain expertise'in burada devreye giriyor.

### 1.1 Taxonomy Oluştur

Hangi ekipman tipleri, hangi analiz türleri, hangi senaryolar?

```
EKIPMAN KATEGORİLERİ
├── Isı Transfer Ekipmanları
│   ├── Shell & tube heat exchanger
│   ├── Plate heat exchanger
│   ├── Finned tube heat exchanger
│   ├── Waste heat recovery boiler (WHRB)
│   ├── Economizer
│   ├── Condenser (surface, air-cooled)
│   ├── Evaporator
│   └── Cooling tower
│
├── Türbomakineler
│   ├── Steam turbine (backpressure, condensing)
│   ├── Gas turbine
│   ├── Compressor (centrifugal, reciprocating, screw)
│   ├── Pump (centrifugal, positive displacement)
│   └── Fan / blower
│
├── Termal Sistemler
│   ├── Boiler (fire tube, water tube)
│   ├── Furnace
│   ├── Kiln
│   ├── Dryer (rotary, spray, fluidized bed)
│   └── Distillation column
│
├── HVAC Sistemleri
│   ├── Chiller (absorption, vapor compression)
│   ├── AHU (air handling unit)
│   ├── Fan coil unit
│   ├── VRF/VRV sistemi
│   ├── Heat pump
│   └── Cooling tower (HVAC)
│
├── Kimyasal Prosesler
│   ├── Reactor (CSTR, PFR, batch)
│   ├── Mixer / blender
│   ├── Separation unit
│   └── Absorption column
│
└── Kombine Sistemler
    ├── Combined cycle (gas + steam)
    ├── Cogeneration (CHP)
    ├── ORC (Organic Rankine Cycle)
    ├── Refrigeration cycle
    └── Heat recovery network
```

### 1.2 Analiz Türleri

Her ekipman için şu analiz türleri üretilecek:

| # | Analiz Türü | Açıklama | Zorluk |
|---|-------------|----------|--------|
| 1 | **Temel exergy analizi** | Exergy giriş/çıkış, yıkım, verimlilik | Kolay |
| 2 | **Entropi üretim analizi** | S_gen hesabı, irreversibility kaynakları | Orta |
| 3 | **Gouy-Stodola bağlantısı** | Ex_d = T₀ · S_gen doğrulaması | Orta |
| 4 | **Parametrik analiz** | Sıcaklık/basınç değişiminin etkisi | Orta |
| 5 | **Termoekonomik analiz** | Maliyet allokasyonu, SPECO yöntemi | Zor |
| 6 | **İyileştirme önerileri** | Pratik mühendislik tavsiyeleri | Orta |
| 7 | **Karşılaştırmalı analiz** | Farklı çalışma koşulları karşılaştırması | Zor |
| 8 | **Arıza teşhisi** | Exergy yıkım pattern'ından arıza tahmini | Zor |

### 1.3 Hedef Veri Seti Boyutları

| Aşama | Örnek Sayısı | Amaç |
|-------|-------------|------|
| v0.1 (MVP) | 500-1000 | Proof of concept, temel exergy analizi |
| v0.2 | 2000-3000 | Tüm ekipman tipleri, çoklu analiz türleri |
| v0.3 | 5000-7000 | Termoekonomik analiz, arıza teşhisi |
| v1.0 | 10000+ | Production-ready, community katkılarıyla |

### 1.4 Veri Kalite Kontrolü

Bu adımı ATLAMA. Her batch'ten sonra:
- [ ] Termodinamik tutarlılık kontrolü (enerji/exergy dengesi)
- [ ] Birim kontrolü (kW vs kJ, °C vs K)
- [ ] Dead state tanım tutarlılığı (T₀=25°C, P₀=1 atm)
- [ ] Formül doğruluğu (entropi hesapları)
- [ ] Pratik anlamlılık (gerçek dünya değerleri mi?)

---

## Faz 2: Sentetik Veri Üretimi (Hafta 4-8)

### 2.1 Prompt Şablonları

Minimum 5 farklı prompt template ailesi:

**Template A — Doğrudan Analiz**
```
Ekipman: [type]
Çalışma koşulları: [parameters]
Dead state: T₀=25°C, P₀=101.325 kPa
Tam exergy analizi yap: exergy dengesi, yıkım, verimlilik.
```

**Template B — Problem Çözme**
```
Bir [type] ekipmanın exergy verimi %[X] olarak ölçülmüş.
Tasarım verimi %[Y] idi. Olası nedenleri analiz et
ve iyileştirme önerileri sun.
```

**Template C — Karşılaştırma**
```
Aynı [type] ekipmanın [condition A] ve [condition B]
koşullarında exergy performansını karşılaştır.
Hangi koşulda entropi üretimi daha fazla ve neden?
```

**Template D — Termoekonomik**
```
[System] sistemindeki [component] için termoekonomik
maliyet allokasyonu yap. Yakıt maliyeti [X] $/GJ.
SPECO yöntemini kullan.
```

**Template E — Teşhis**
```
[type] ekipmanın son 3 aydaki exergy verimlilik trendi:
Ay 1: %[X], Ay 2: %[Y], Ay 3: %[Z]
Bu trend neye işaret ediyor? Olası arıza mekanizması nedir?
```

### 2.2 Parametre Varyasyonu

Her template için realistic parametre aralıkları:

```python
# Örnek: Heat Exchanger parametreleri
heat_exchanger_params = {
    "hot_inlet_temp": range(80, 500, 20),     # °C
    "hot_outlet_temp": range(40, 300, 15),     # °C
    "cold_inlet_temp": range(15, 100, 10),     # °C
    "cold_outlet_temp": range(30, 200, 15),    # °C
    "flow_rate_hot": [0.5, 1, 2, 5, 10, 20],  # kg/s
    "flow_rate_cold": [0.5, 1, 2, 5, 10, 25], # kg/s
    "pressure_drop": [0.1, 0.5, 1, 2, 5],     # bar
    "fouling_factor": [0, 0.0001, 0.0003, 0.0005, 0.001],
    "fluid_hot": ["water", "steam", "therminol", "flue_gas", "air"],
    "fluid_cold": ["water", "glycol_solution", "air", "refrigerant"],
}
```

### 2.3 API Çağrı Stratejisi

```
Toplam bütçe tahmini (Claude Sonnet ile):
- 5000 örnek × ortalama 2000 token output = 10M output token
- Input: ~5M token
- Maliyet: ~$30-40 (Sonnet fiyatıyla)
- Süre: ~8-12 saat (paralel isteklerle)
```

---

## Faz 3: Model Eğitimi (Hafta 8-10)

### 3.1 Base Model Seçimi

| Model | Boyut | Neden? |
|-------|-------|--------|
| **Qwen2.5-7B-Instruct** | 7B | Matematik/hesaplama yeteneği güçlü, çok dilli |
| Llama-3.1-8B-Instruct | 8B | Genel performans iyi, büyük community |
| Mistral-7B-v0.3 | 7B | Verimli, kanıtlanmış mimari |

**Tavsiye: Qwen2.5-7B** — sayısal hesaplama ve formül üretiminde diğerlerinden iyi.
İkinci aday: Llama-3.1-8B.

### 3.2 Eğitim Stratejisi

```
Aşama 1: Continued Pre-training (opsiyonel ama değerli)
├── Termodinamik textbook'lar (Çengel & Boles, Moran & Shapiro)
├── Exergy analizi makaleleri (Bejan, Tsatsaronis, Kotas)
├── Steam tables, refrigerant properties
└── ~50-100M token, 1-2 epoch

Aşama 2: SFT (Supervised Fine-Tuning)
├── Sentetik veri seti (Faz 2'den)
├── LoRA rank=64, alpha=64
├── 3-5 epoch
└── Cosine LR schedule, warmup 5%

Aşama 3: DPO/ORPO (opsiyonel, v0.2+)
├── "İyi analiz" vs "kötü analiz" çiftleri
├── Sen manual olarak değerlendirirsin
└── Model tercih öğrenir
```

### 3.3 Eğitim Hyperparameters (Başlangıç)

```python
# Bu değerler baseline — deney yaparak optimize edilecek
lora_config = {
    "r": 64,
    "lora_alpha": 64,
    "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    "lora_dropout": 0.05,
}

training_config = {
    "num_epochs": 3,
    "batch_size": 2,
    "gradient_accumulation": 4,
    "learning_rate": 2e-4,
    "lr_scheduler": "cosine",
    "warmup_ratio": 0.05,
    "weight_decay": 0.01,
    "max_seq_length": 4096,
}
```

---

## Faz 4: Değerlendirme (Hafta 10-12)

### 4.1 Evaluation Seti

Eğitim verisinden AYRI tutulan 100-200 test örneği.
Her birini 3 boyutta değerlendir:

| Kriter | Nasıl ölçülür | Hedef |
|--------|--------------|-------|
| **Termodinamik doğruluk** | Formül ve hesap kontrolü (sen manual) | >90% |
| **Eksiksizlik** | Tüm analiz adımları var mı | >85% |
| **Pratik anlamlılık** | Değerler gerçekçi mi, öneriler uygulanabilir mi | >80% |
| **Format tutarlılığı** | Raporlama formatına uyuyor mu | >90% |

### 4.2 Karşılaştırma Benchmark

Aynı 50 soruyu şu modellere de sor:
- Ham Qwen2.5-7B (fine-tune öncesi)
- GPT-4o
- Claude Sonnet
- EntropyHunter-7B (senin modelin)

Bu karşılaştırma model kartı ve blog post için altın değerinde.

### 4.3 Başarısızlık Analizi

Modelin nerede hata yaptığını kategorize et:
- Hesaplama hataları (sayısal)
- Kavramsal hatalar (termodinamik)
- Eksik analiz adımları
- Hallucination (uydurma değerler)

Her kategori için veri setine düzeltici örnekler ekle → v0.2'ye aktar.

---

## Faz 5: Yayınlama (Hafta 12-14)

### 5.1 HuggingFace Model Kartı

```
EntropyHunter-7B v0.1

Dünyanın ilk exergy analizi ve entropi üretim tespiti için
fine-tune edilmiş açık kaynak modeli.

Base: Qwen2.5-7B-Instruct
Method: LoRA fine-tuning on synthetic thermodynamic analysis data
Domain: Industrial exergy analysis, entropy generation, thermoeconomics
Author: Kemal Düzkar / Olivenet Ltd.
License: Apache 2.0
```

Model kartında olması gerekenler:
- [ ] Modelin ne yaptığı, ne yapmadığı
- [ ] Desteklenen ekipman tipleri listesi
- [ ] Örnek kullanım (input/output)
- [ ] Termodinamik varsayımlar (dead state, referans koşullar)
- [ ] Bilinen sınırlamalar
- [ ] Eğitim detayları
- [ ] Benchmark sonuçları (vs base model, vs frontier modeller)
- [ ] Citation bilgisi

### 5.2 Eşlik Eden İçerik

- [ ] Blog post: "Endüstriyel Entropi Avcılığı: İlk Açık Kaynak Exergy Analiz Modeli"
- [ ] LinkedIn duyurusu
- [ ] Örnek Colab notebook (herkes deneyebilsin)
- [ ] YouTube/video walkthrough (opsiyonel ama etkili)

### 5.3 Dataset'i de yayınla

```
OlivenetAI/exergy-analysis-dataset-v1
```

Dataset'i de açık kaynak yap:
- Başkaları üzerine çalışabilsin
- Akademik atıf alsın
- Community katkısı gelsin

---

## Faz 6: İterasyon (Hafta 14+)

### v0.2 Hedefleri
- [ ] Daha fazla ekipman tipi
- [ ] Termoekonomik analiz (SPECO yöntemi)
- [ ] Türkçe destek (dual-language)
- [ ] DPO ile tercih öğrenme
- [ ] Context window genişletme

### v0.3 Hedefleri
- [ ] ExergyLab entegrasyonu (API endpoint)
- [ ] Zaman serisi veriden trend analizi
- [ ] Arıza teşhis yetenekleri
- [ ] IoT sensor verisi → otomatik analiz pipeline

### v1.0 Vizyonu
- [ ] ExergyLab'ın AI motoru olarak production deployment
- [ ] Edge deployment (GGUF, Jetson?)
- [ ] Müşteri-spesifik fine-tune hizmeti
- [ ] Akademik paper

---

## Bütçe Tahmini

| Kalem | Faz | Tahmini Maliyet |
|-------|-----|----------------|
| Claude API (veri üretimi) | Faz 2 | $30-50 |
| GPU kiralama (eğitim) | Faz 3 | $20-50 |
| GPU kiralama (deney/iterasyon) | Faz 3-6 | $50-100 |
| HuggingFace Pro (opsiyonel) | Faz 5 | $9/ay |
| Wandb Pro (opsiyonel) | Faz 3+ | Free tier yeterli |
| **TOPLAM (MVP)** | | **~$100-200** |
| **TOPLAM (v1.0'a kadar)** | | **~$300-500** |

> Not: RTX 4090 alırsan GPU kiralama maliyeti ortadan kalkar
> ama $1600 başlangıç maliyeti var.

---

## Öğrenme Yol Haritası

Bu proje boyunca kazanacağın AI/ML becerileri:

### Faz 1-2'de öğreneceklerin
- Synthetic data generation
- Prompt engineering (sistematik)
- Dataset curation & quality control
- HuggingFace datasets kütüphanesi

### Faz 3'te öğreneceklerin
- LoRA / QLoRA fine-tuning
- Unsloth framework
- Training hyperparameter optimization
- Wandb experiment tracking
- GPU memory management

### Faz 4'te öğreneceklerin
- Model evaluation methodology
- Benchmark design
- Failure analysis
- A/B testing modeller arası

### Faz 5-6'da öğreneceklerin
- Model deployment (vLLM, GGUF)
- HuggingFace ecosystem
- Open source community management
- Technical writing (model card, blog)
- DPO/RLHF (v0.2+)

---

## Zaman Çizelgesi

```
Hafta  1-2   ████ Faz 0: Ortam kurulumu, donanım kararı
Hafta  2-4   ████████ Faz 1: Taxonomy, prompt tasarımı
Hafta  4-8   ████████████████ Faz 2: Veri üretimi + kalite kontrol
Hafta  8-10  ████████ Faz 3: Eğitim + deney
Hafta 10-12  ████████ Faz 4: Değerlendirme
Hafta 12-14  ████████ Faz 5: Yayınlama
Hafta 14+    ████████████████████ Faz 6: İterasyon
              ↑                    ↑
              v0.1 release         v0.2 release
```

Toplam: MVP (v0.1) ~3 ay, production-ready (v1.0) ~6-9 ay

---

*"Entropi üretimi evrensel bir gerçek. Onu ölçen, anlayan ve azaltan araçlar
 inşa etmek mühendisliğin en asil görevidir."*

— EntropyHunter Manifesto
