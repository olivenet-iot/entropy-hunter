# EntropyHunter-7B — Faz 1: Taxonomy & Veri Seti Tasarımı

> ExergyLab PROJECT_ANALYSIS.md'den türetilmiştir.
> ExergyLab'ın 7 motoru, 7 ekipman tipi ve 46 alt tipi doğrudan
> eğitim verisi kategorilerine dönüştürülmüştür.

---

## 1. Ekipman Taxonomy'si (ExergyLab'dan Doğrudan)

ExergyLab'da zaten 7 ekipman ve 46 alt tip var. Bunların HER BİRİ
eğitim verisinde temsil edilecek.

### 1.1 Ekipman × Alt Tip Matrisi

```
COMPRESSOR (4 alt tip)
├── screw
├── piston (reciprocating)
├── scroll
└── centrifugal

BOILER (7 alt tip)
├── steam_firetube
├── steam_watertube
├── hotwater
├── condensing
├── waste_heat
├── electric
└── biomass

CHILLER (7 alt tip)
├── screw
├── centrifugal
├── scroll
├── reciprocating
├── absorption
├── air_cooled
└── water_cooled

PUMP (6 alt tip)
├── centrifugal
├── positive_displacement
├── submersible
├── vertical_turbine
├── booster
└── vacuum

HEAT_EXCHANGER (8 alt tip)
├── shell_tube
├── plate
├── air_cooled
├── double_pipe
├── spiral
├── economizer
├── recuperator
└── finned_tube

STEAM_TURBINE (5 alt tip)
├── back_pressure
├── condensing
├── extraction
├── orc
└── micro_turbine

DRYER (11 alt tip)
├── convective
├── rotary
├── fluidized_bed
├── spray
├── belt
├── heat_pump
├── infrared
├── drum
├── conveyor
├── tray
└── microwave
```

**Toplam: 7 ekipman × 48 alt tip = veri setinin ekipman ekseni**

---

## 2. Analiz Türleri Taxonomy'si (ExergyLab'ın 7 Motorundan)

ExergyLab'ın her motoru bir analiz türüne karşılık geliyor.
EntropyHunter bunların HEPSİNİ yapabilmeli.

### 2.1 Ana Analiz Türleri

| # | Analiz Türü | ExergyLab Karşılığı | Kaynak Dosya | Zorluk |
|---|------------|---------------------|-------------|--------|
| A | **Temel Exergy Analizi** | `analyze_{equipment}()` | core.py + 7 ekipman.py | ⭐ Kolay |
| B | **Exergoekonomik Analiz** | `analyze_exergoeconomic()` | exergoeconomic.py | ⭐⭐ Orta |
| C | **Pinch Analizi** | `analyze_pinch()` | pinch.py | ⭐⭐ Orta |
| D | **İleri Exergy (Tsatsaronis)** | `analyze_advanced_exergy()` | advanced_exergy.py | ⭐⭐⭐ Zor |
| E | **Entropi Üretim Min. (EGM)** | `analyze_entropy_generation()` | entropy_generation.py | ⭐⭐⭐ Zor |
| F | **Termoekonomik Optimizasyon** | `analyze_thermoeconomic_optimization()` | thermoeconomic_optimization.py | ⭐⭐⭐ Zor |
| G | **Enerji Yönetimi (ISO 50001)** | `analyze_energy_management()` | energy_management.py | ⭐⭐ Orta |
| H | **Gap Analizi** | `analyze_gap()` | gap_analysis.py + process_exergy.py | ⭐⭐ Orta |

### 2.2 Tamamlayıcı Analiz Türleri (ExergyLab'dan türetilmiş)

| # | Analiz Türü | ExergyLab Karşılığı | Zorluk |
|---|------------|---------------------|--------|
| I | **AV/UN Ayrışımı** | `compute_avoidable_split()` | ⭐ Kolay |
| J | **What-if Karşılaştırma** | `compute_comparison()` | ⭐⭐ Orta |
| K | **Hotspot Tespiti** | `_identify_hotspots()` | ⭐ Kolay |
| L | **Entegrasyon Fırsatları** | `_detect_integration_opportunities()` | ⭐⭐ Orta |
| M | **Arıza Teşhisi** | (ExergyLab'da yok — yeni yetenek) | ⭐⭐⭐ Zor |
| N | **Sankey Yorumlama** | `generate_factory_sankey_v2()` | ⭐⭐ Orta |

**Toplam: 14 analiz türü**

---

## 3. Prompt Şablon Aileleri

Her şablon ailesi, farklı bir kullanıcı senaryosunu temsil eder.

### Aile A — Temel Exergy Analizi (Tek Ekipman)

```
Senaryo: Mühendis tek bir ekipmanın exergy performansını bilmek istiyor.
Input: Ekipman tipi, alt tipi, çalışma parametreleri, dead state
Output: Exergy dengesi, yıkım, verimlilik, AV/UN ayrışımı, öneriler
```

**Parametrik değişkenler (ExergyLab'ın input dataclass'larından):**

COMPRESSOR:
- inlet_temp_C: [15, 20, 25, 30, 35, 40]
- discharge_pressure_bar: [6, 7, 8, 10, 12, 14]
- power_input_kW: [15, 37, 55, 75, 110, 160, 250]
- isentropic_efficiency_pct: [55, 60, 65, 70, 75, 80, 85]
- flow_rate_m3_min: [1, 2, 5, 10, 20, 50]

BOILER:
- fuel_type: [natural_gas, fuel_oil, lpg, biomass_wood, biomass_pellet]
- thermal_capacity_kW: [100, 250, 500, 1000, 2000, 5000]
- operating_pressure_bar: [4, 6, 8, 10, 15, 20, 25]
- stack_temperature_C: [120, 150, 180, 200, 250, 300]
- feedwater_temperature_C: [15, 40, 60, 80, 100]
- thermal_efficiency_pct: [75, 80, 85, 88, 90, 92, 95]

CHILLER:
- cooling_capacity_kW: [50, 100, 200, 500, 1000, 2000]
- evaporator_temp_C: [-5, 0, 2, 5, 7, 10, 12]
- condenser_temp_C: [30, 35, 38, 40, 45]
- cop: [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
- refrigerant: [R134a, R410A, R407C, R744, LiBr]

PUMP:
- flow_rate_m3_h: [5, 10, 20, 50, 100, 200, 500]
- head_m: [10, 20, 30, 50, 80, 100, 150]
- motor_power_kW: [1.5, 3, 5.5, 11, 22, 37, 55, 75]
- pump_efficiency_pct: [50, 55, 60, 65, 70, 75, 80, 85]
- motor_efficiency_pct: [85, 88, 90, 92, 94]

HEAT_EXCHANGER:
- hot_inlet_temp_C: [80, 120, 150, 200, 300, 400, 500]
- hot_outlet_temp_C: [40, 60, 80, 100, 150, 200]
- cold_inlet_temp_C: [10, 15, 20, 30, 50, 80]
- cold_outlet_temp_C: [40, 60, 80, 100, 120, 150]
- heat_duty_kW: [50, 100, 250, 500, 1000, 2000]
- pressure_drop_bar: [0.1, 0.2, 0.5, 1.0, 2.0]
- fluid_hot: [water, steam, flue_gas, therminol, air]
- fluid_cold: [water, glycol, air, refrigerant]

STEAM_TURBINE:
- inlet_pressure_bar: [10, 15, 20, 30, 40, 60, 80, 100]
- inlet_temp_C: [180, 200, 250, 300, 350, 400, 450, 500, 540]
- outlet_pressure_bar: [0.05, 0.1, 0.5, 1.0, 2.0, 4.0, 6.0]
- mass_flow_kg_s: [1, 2, 5, 10, 20, 50, 100]
- isentropic_efficiency_pct: [60, 65, 70, 75, 80, 85]
- generator_efficiency_pct: [92, 94, 95, 96, 97]

DRYER:
- inlet_air_temp_C: [60, 80, 100, 120, 150, 180, 200]
- outlet_air_temp_C: [40, 50, 60, 70, 80]
- product_flow_kg_h: [50, 100, 200, 500, 1000, 2000]
- initial_moisture_pct: [20, 30, 40, 50, 60, 70, 80]
- final_moisture_pct: [2, 5, 8, 10, 12, 15]
- thermal_input_kW: [50, 100, 200, 500, 1000]


### Aile B — Exergoekonomik Analiz (SPECO)

```
Senaryo: Mühendis ekipmanın exergy yıkımının ekonomik maliyetini bilmek istiyor.
Input: Ekipman + temel analiz sonuçları + ekonomik parametreler
Output: Z_dot, C_dot_D, f-faktör, r-faktör, c_product, strateji önerisi
```

**Ek parametreler (exergoeconomic.py'den):**
- equipment_cost_eur: [5000, 10000, 25000, 50000, 100000, 250000, 500000]
- installation_factor: [1.2, 1.4, 1.65, 2.0]
- interest_rate: [0.05, 0.08, 0.10, 0.12]
- equipment_life_years: [10, 15, 20, 25, 30]
- maintenance_factor: [0.01, 0.02, 0.03, 0.05]
- annual_operating_hours: [4000, 6000, 8000, 8760]
- c_fuel_eur_kwh: [0.03, 0.05, 0.08, 0.10, 0.12]


### Aile C — Pinch Analizi (Çoklu Ekipman)

```
Senaryo: Mühendis fabrikadaki ısı entegrasyon potansiyelini bilmek istiyor.
Input: Sıcak ve soğuk akış listesi (birden fazla ekipmandan)
Output: Pinch noktası, QH_min, QC_min, tasarruf potansiyeli, HEN önerileri
```

**Parametrik değişkenler (pinch.py'den):**
- stream_count: [3, 4, 5, 6, 8, 10]  (sıcak + soğuk toplam)
- delta_T_min_C: [5, 10, 15, 20]
- endüstri tipi: [kimya, gıda, kağıt, çelik, çimento, tekstil, ilaç]


### Aile D — İleri Exergy Dekompozisyonu (Tsatsaronis)

```
Senaryo: Mühendis her ekipmanın exergy yıkımının endojen/eksojen kaynağını bilmek istiyor.
Input: Fabrika ekipman listesi + analiz sonuçları (min 3 ekipman)
Output: EN/EX ayrışımı, AV/UN 4-quadrant, etkileşim ağı, öncelik sıralaması
```

**Anahtar sabitler (advanced_exergy.py'den):**
- BASE_ISOLATION_FACTORS: {compressor: 0.75, boiler: 0.80, ...}
- INTERACTION_COEFFICIENTS: seyrek matris
- REFERENCE_EFFICIENCIES: ekipman/alt tip bazlı


### Aile E — Entropi Üretim Minimizasyonu (EGM / Bejan)

```
Senaryo: Mühendis her ekipmanın entropi üretim mekanizmalarını anlamak istiyor.
Input: Fabrika ekipman listesi + analiz sonuçları
Output: S_gen, N_s (Bejan sayısı), mekanizma dekompozisyonu
         (ısı transferi / basınç düşümü / karışım), iyileştirme potansiyeli
```

**Anahtar sabitler (entropy_generation.py'den):**
- ENTROPY_DECOMPOSITION_FRACTIONS (ekipman/alt tip bazlı)
- BEJAN_GRADES: A (0-0.15), B (0.15-0.30), C (0.30-0.50), D (0.50-0.70), F (0.70-1.01)
- Gouy-Stodola: Ex_destroyed = T₀ × S_gen


### Aile F — Termoekonomik Optimizasyon

```
Senaryo: Mühendis hangi ekipmana yatırım yapması gerektiğine karar vermek istiyor.
Input: Fabrika analiz sonuçları (exergoekonomik dahil)
Output: f/r karar matrisi, strateji (invest/parametric/structural/downsize/maintain),
         maliyet-fayda analizi, basit geri ödeme süresi
```

**Karar mantığı (thermoeconomic_optimization.py'den):**
- f < 0.25 & r > 0.5 → invest
- f > 0.65 → downsize
- 0.25 ≤ f ≤ 0.65 & avoidable > 0.5 → parametric
- 0.25 ≤ f ≤ 0.65 & avoidable ≤ 0.5 → maintain
- diğer → structural


### Aile G — ISO 50001 Enerji Yönetimi Denetimi

```
Senaryo: Enerji yöneticisi ISO 50001 uyumu değerlendirmek istiyor.
Input: Fabrika analiz sonuçları (tüm motorlardan)
Output: EnPI metrikleri, 7 boyutlu olgunluk skoru, aksiyon planı, timeline
```

**7 EnPI metriği (energy_management.py'den):**
- eta_ex, SEC, EDR, ALR, ECI, HRP, EGI


### Aile H — 3-Katmanlı Gap Analizi

```
Senaryo: Mühendis tesisin termodinamik ideal ile BAT arasındaki konumunu bilmek istiyor.
Input: Proses tanımı + fabrika agregat sonuçları
Output: Minimum / BAT / Aktüel exergy karşılaştırması, ESI grade (A-F)
```

**8 proses tipi (process_exergy.py'den):**
- drying, heating, cooling, steam_generation
- compressed_air, chp, cold_storage, general_manufacturing


### Aile I — What-if Senaryo Karşılaştırma

```
Senaryo: Mühendis bir iyileştirmenin etkisini görmek istiyor.
Input: Baseline parametreler + değiştirilmiş senaryo parametreleri
Output: Delta analizi, tasarruf hesabı, iyileşen/kötüleşen metrikler
```


### Aile J — Arıza Teşhisi (YENİ — ExergyLab'da yok)

```
Senaryo: Mühendis exergy verimlilik düşüşünden arıza tahmini istiyor.
Input: Zaman serisi exergy verimlilik verileri + ekipman bilgisi
Output: Olası arıza mekanizması, kök neden analizi, bakım önerileri
```

**Arıza pattern'ları (domain bilgisi gerekli):**
- Kademeli düşüş → fouling, scaling, korozyon
- Ani düşüş → mekanik arıza, kontrol sistemi hatası
- Periyodik dalgalanma → yük değişimi, çevresel etki
- Aşamalı kötüleşme → aşınma, sızdırma

---

## 4. Ekipman × Analiz Matrisi (Veri Seti Kapsam Planı)

Her hücre = üretilecek eğitim örneği sayısı hedefi

### v0.1 (MVP) — Toplam ~800-1000 örnek

|  | A:Temel | B:SPECO | E:EGM | I:AV/UN | J:What-if |
|--|---------|---------|-------|---------|-----------|
| **Compressor** (4) | 30 | 15 | 10 | 10 | 10 |
| **Boiler** (7) | 35 | 15 | 10 | 10 | 10 |
| **Chiller** (7) | 35 | 15 | 10 | 10 | 10 |
| **Pump** (6) | 30 | 15 | 10 | 10 | 10 |
| **HX** (8) | 40 | 15 | 15 | 10 | 10 |
| **Steam Turbine** (5) | 30 | 15 | 10 | 10 | 10 |
| **Dryer** (11) | 40 | 15 | 10 | 10 | 10 |
| **Multi-equip** | — | — | 20 | — | 20 |
| **TOPLAM** | **240** | **105** | **95** | **70** | **90** |

**Grand total v0.1: ~600 + ~200 edge case/error handling = ~800**

### v0.2 — Toplam ~3000 örnek (v0.1 + aşağıdakiler)

|  | C:Pinch | D:Tsatsaronis | F:Termoekon | G:ISO50001 | H:Gap |
|--|---------|--------------|-------------|------------|-------|
| **3-equip fabrika** | 40 | 40 | 30 | 20 | 30 |
| **5-equip fabrika** | 40 | 40 | 30 | 20 | 30 |
| **7+ equip fabrika** | 30 | 30 | 20 | 15 | 20 |
| **Sektör varyasyonları** | 60 | 40 | 40 | 40 | 50 |
| **TOPLAM ek** | **170** | **150** | **120** | **95** | **130** |

### v0.3 — Toplam ~5000+ (v0.2 + arıza teşhisi + Türkçe)

- Aile J: Arıza teşhisi örnekleri (~300)
- Türkçe duplikasyonlar (~800)
- Edge case'ler ve hata düzeltmeleri (~500)

---

## 5. Veri Kalite Gereksinimleri

### 5.1 Termodinamik Tutarlılık Kontrolleri

Her üretilen örnek şu kontrollerden geçmeli:

```python
QUALITY_CHECKS = {
    "energy_balance": {
        "rule": "abs(exergy_in - exergy_out - exergy_destroyed) < 0.01 * exergy_in",
        "description": "Exergy dengesi (%1 tolerans)"
    },
    "efficiency_range": {
        "rule": "0 < exergy_efficiency < 100",
        "description": "Verimlilik fiziksel aralıkta"
    },
    "second_law": {
        "rule": "exergy_destroyed >= 0",
        "description": "İkinci yasa ihlali yok (S_gen ≥ 0)"
    },
    "gouy_stodola": {
        "rule": "abs(exergy_destroyed - T0 * S_gen) < 0.01 * exergy_destroyed",
        "description": "Gouy-Stodola tutarlılığı"
    },
    "dead_state_consistency": {
        "rule": "T0 == 298.15 AND P0 == 101.325 (aksi belirtilmedikçe)",
        "description": "Dead state tutarlılığı"
    },
    "unit_consistency": {
        "rule": "all_temperatures_in_K_for_calc AND display_in_C",
        "description": "Birim tutarlılığı (hesap K, gösterim °C)"
    },
    "avoidable_split": {
        "rule": "avoidable + unavoidable == total_destroyed",
        "description": "AV/UN toplam tutarlılığı"
    },
    "bejan_number": {
        "rule": "0 <= N_s <= 1",
        "description": "Bejan sayısı aralığı"
    },
    "speco_factors": {
        "rule": "0 <= f_factor <= 1 AND r_factor >= 0",
        "description": "SPECO faktör aralıkları"
    },
    "realistic_values": {
        "rule": "check_against_BAT_and_industry_ranges",
        "description": "Değerler endüstriyel aralıklarda"
    }
}
```

### 5.2 Endüstriyel Gerçekçilik Kontrolleri

ExergyLab'ın mevcut verileri referans:

| Ekipman | Tipik Verimlilik | Tipik Exergy Yıkım |
|---------|------------------|---------------------|
| Kompresör | %50-85 | 5-50 kW |
| Kazan | %25-95 (exergy) | 50-2000 kW |
| Chiller | COP 2.5-6.0 | 10-500 kW |
| Pompa | %50-85 | 0.5-20 kW |
| Isı eşanjörü | %40-85 | 5-200 kW |
| Buhar türbini | %60-85 | 50-5000 kW |
| Kurutma fırını | %15-55 | 20-500 kW |

### 5.3 Red Kriterleri (Bu örnekleri veri setinden çıkar)

- [ ] Exergy dengesi %5'ten fazla sapıyor
- [ ] Negatif entropi üretimi (ikinci yasa ihlali)
- [ ] Verimlilik %100'ü aşıyor
- [ ] Bejan sayısı [0, 1] aralığı dışında
- [ ] COP, Carnot COP'u aşıyor
- [ ] Değerler endüstriyel aralıkların 10x dışında
- [ ] Formül açıklaması hesap sonucuyla tutarsız
- [ ] Dead state referansı tutarsız

---

## 6. ExergyLab Bilgi Tabanından Yararlanma

### 6.1 Knowledge Base (317 dosya)

ExergyLab'ın knowledge/ dizini doğrudan prompt zenginleştirme için kullanılabilir:

```
knowledge/
├── compressor/ (19 dosya) → kompresör domain bilgisi
├── boiler/ (23 dosya) → kazan domain bilgisi
├── chiller/ (25 dosya) → chiller domain bilgisi
├── pump/ (23 dosya) → pompa domain bilgisi
├── heat_exchanger/ (21 dosya) → HX domain bilgisi
├── steam_turbine/ (23 dosya) → buhar türbini domain bilgisi
├── dryer/ (26 dosya) → kurutma fırını domain bilgisi
└── factory/ (156 dosya)
    ├── pinch/ (18) → pinch analizi domain bilgisi
    ├── advanced_exergy/ (18) → Tsatsaronis domain bilgisi
    ├── exergoeconomic/ (18) → SPECO domain bilgisi
    ├── thermoeconomic_optimization/ (16)
    ├── entropy_generation/ (19) → EGM/Bejan domain bilgisi
    ├── energy_management/ (21) → ISO 50001 domain bilgisi
    └── process/ (12) → proses exergy domain bilgisi
```

**Kullanım stratejisi:** Bu dosyaları teacher model'e (Claude) prompt ile birlikte
context olarak vererek, üretilen cevapların domain doğruluğunu artırabiliriz.

### 6.2 Skill Dosyaları (18 dosya)

ExergyLab'ın skill sistemi, modelin "nasıl davranması gerektiğini" tanımlar:

```
skills/
├── core/ (3 dosya) → temel analiz yaklaşımı
├── equipment/ (7 dosya) → ekipman uzmanı persona
├── factory/ (4 dosya) → fabrika analisti persona
└── output/ (1 dosya) → çıktı formatı
```

Bu skill dosyaları, teacher model'e system prompt olarak verilebilir —
böylece Claude, ExergyLab'ın beklentilerine uygun formatta cevap üretir.

### 6.3 Engine Sabitleri (Doğrudan Veri Kaynağı)

ExergyLab'ın engine'lerinde gömülü sabitler, eğitim verisinde
tutarlılık sağlamak için referans olarak kullanılacak:

| Sabit | Kaynak | Kullanım |
|-------|--------|----------|
| UNAVOIDABLE_REF_* | 7 ekipman.py | AV/UN ayrışım referansları |
| BASE_ISOLATION_FACTORS | advanced_exergy.py | EN/EX izolasyon katsayıları |
| INTERACTION_COEFFICIENTS | advanced_exergy.py | Ekipman etkileşim matrisi |
| ENTROPY_DECOMPOSITION_FRACTIONS | entropy_generation.py | S_gen mekanizma dağılımı |
| BEJAN_GRADES | entropy_generation.py | N_s not sınıfları |
| COST_CORRELATIONS | exergoeconomic.py | PEC maliyet katsayıları |
| BAT_REFERENCES | bat_references.py | BAT verimlilik referansları |
| MATURITY_LEVELS | energy_management.py | ISO 50001 olgunluk seviyeleri |

---

## 7. Prompt Üretim Stratejisi

### 7.1 Aşamalı Yaklaşım

```
AŞAMA 1 (v0.1): Temel — "tek ekipman, doğrudan analiz"
├── Teacher: Claude Sonnet (maliyet/kalite dengesi)
├── System prompt: ExergyLab skill dosyaları + knowledge
├── Her alt tip için 5-8 parametre kombinasyonu
├── Çıktı formatı: yapılandırılmış (heading + hesap + sonuç + öneri)
└── Kalite kontrol: termodinamik tutarlılık + Kemal manual review

AŞAMA 2 (v0.2): İleri — "çoklu ekipman, fabrika analizi"
├── Teacher: Claude Sonnet
├── Fabrika senaryoları: 3-7 ekipman kombinasyonları
├── Endüstri varyasyonları: kimya, gıda, metal, tekstil, vb.
├── Çıktı: pinch + EN/EX + EGM + termoekonomik sentez
└── Kalite kontrol: fabrika düzeyinde exergy dengesi

AŞAMA 3 (v0.3): Uzman — "teşhis, optimizasyon, raporlama"
├── Teacher: Claude Opus (en yüksek kalite)
├── Zaman serisi arıza senaryoları
├── Türkçe teknik rapor formatı
└── Kalite kontrol: endüstri profesyoneli review
```

### 7.2 Örnek Prompt (Aile A — Temel Exergy)

```
[SYSTEM]
Sen ExergyLab platformunun exergy analiz motorusun.
Termodinamiğin ikinci yasasına dayalı exergy analizi yapıyorsun.
Dead state: T₀ = 25°C (298.15 K), P₀ = 101.325 kPa.

Kurallar:
- Tüm hesapları Kelvin'de yap, sonuçları °C olarak göster
- Exergy dengesi: Ex_in = Ex_out + Ex_destroyed
- Gouy-Stodola: Ex_destroyed = T₀ × S_gen
- AV/UN ayrışımını Tsatsaronis referanslarına göre yap
- Endüstriyel gerçekçiliği koru

[USER]
Shell & tube ısı eşanjörü exergy analizi yap.

Çalışma koşulları:
- Sıcak akışkan: Baca gazı, giriş 320°C, çıkış 180°C, debi 2.5 kg/s
- Soğuk akışkan: Su, giriş 25°C, çıkış 85°C, debi 4.0 kg/s
- Basınç düşümü (sıcak taraf): 0.5 bar
- Basınç düşümü (soğuk taraf): 0.3 bar

Şu formatta cevap ver:
1. Exergy Dengesi (kW cinsinden giriş, çıkış, yıkım)
2. Exergy Verimi (%)
3. Entropi Üretimi (kW/K) — Gouy-Stodola ile doğrula
4. AV/UN Ayrışımı (kW ve %)
5. Bejan Sayısı (N_s) ve Notu (A-F)
6. Entropi üretim mekanizmaları dağılımı (%)
7. İyileştirme Önerileri (pratik, uygulanabilir)
```

---

## 8. Sonraki Adımlar (Faz 1 → Faz 2 Geçişi)

### Bu Dökümanla Tamamlanan
- [x] Ekipman taxonomy'si (7 tip, 48 alt tip)
- [x] Analiz türleri taxonomy'si (14 tür)
- [x] Prompt şablon aileleri (A-J, 10 aile)
- [x] Parametrik değişken aralıkları
- [x] Veri kalite gereksinimleri
- [x] ExergyLab bilgi tabanı kullanım stratejisi
- [x] Kapsam planı (v0.1: ~800, v0.2: ~3000, v0.3: ~5000+)

### Faz 2'ye Geçiş İçin Yapılacaklar
- [ ] Prompt şablonlarını Python'a kodla (parametre varyasyonu ile)
- [ ] ExergyLab knowledge dosyalarını okuyup context olarak hazırla
- [ ] Claude API test çağrıları (10-20 örnek) → kalite değerlendirmesi
- [ ] Kalite kontrol script'i yaz (termodinamik tutarlılık)
- [ ] İlk batch: 50 örnek üret → manual review → kalibrasyon
- [ ] GitHub repo oluştur: `OlivenetAI/entropy-hunter`

---

*"Evrende hiçbir süreç tersinir değildir.
 Entropi her zaman üretilir.
 Bunu ölçen, anlayan ve minimize eden araçlar
 inşa etmek — işte bu gerçek mühendisliktir."*
