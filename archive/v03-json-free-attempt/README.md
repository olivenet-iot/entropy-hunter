# v0.3 JSON-Free Attempt (27 Feb 2026)

## Ne denendi
Training data'dan JSON summary bloklarini cikarip retrain ettik.
Amac: JSON'u 7B model ogrenemiyordu (0/120), cikarmak token waste'i azaltacakti.

## Sonuc: BASARISIZ
- v0.2 (JSON'lu): %85.5
- v0.3 (JSON-free): %78.3 (-7.2pp regression)

## Neden basarisiz
JSON blogu kazara "reasoning scaffold" olarak calisiyormus.
Model "once JSON'da hesapla, sonra acikla" kalibini ogrenmisti.
JSON cikinca reasoning chain kirildi, ozellikle:
- crf_calc: %95 -> %62
- crf_value: %67 -> %38
- avoidable_ratio: %60 -> %27

## Ogrenilen ders
Scaffold'u kaldirmak degil, donusturmek gerekiyor.
v0.4'te JSON yerine "## Calculation Summary" formati kullanilacak.
