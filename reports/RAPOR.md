# ATVS Lab v2 Raporu — 2026-10-02 18:09 UTC

**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).
**Seçim** ilk %70 veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %30 (OOS) verisine göre** verilir. ✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · ⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.
Giriş: sinyalden sonraki bar açılışı · zaman bariyeri 48 bar · aynı barda hedef+stop = stop. TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 15m | iki yön | SEZON · saat etkisi UTC 11↑ 22↑ 23↑ | IZ_SUREN_2.5ATR | +64.983R (700) | **+5.287R** (300) | %23.0 | 5.41 | 78.7 | 92.16R | 0.050 | ⚠️ Pozitif, anlamsız |
| **XAG** | 4h | SHORT | MA · EMA 20/50 kesişimi | GENIS_%50@1R>BE_3R | +0.328R (81) | **-0.067R** (34) | %47.1 | 0.88 | 1.6 | 6.77R | 0.631 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | SHORT | DONCH · Donchian 20 · hacim şoku | SABIT_1.5R | +0.524R (79) | **-0.175R** (45) | %35.6 | 0.75 | 2.1 | 11.44R | 0.834 | ❌ OOS'ta tutmadı |
| **ETH** | 4h | iki yön | REJIM · yatayda dönüş · Stoch · volatilite şoku | TP1>BE_3R | +0.714R (56) | **-0.137R** (31) | %12.9 | 0.74 | 1.4 | 10.14R | 0.720 | ❌ OOS'ta tutmadı |
| **NQ** | 5m | iki yön | VWAP · sapma dönüşü ±2.0σ · filtresiz | IZ_SUREN_2.5ATR | +87320626.004R (1273) | **+35107716.412R** (474) | %19.8 | 464.55 | 153.5 | 35898757.63R | 0.159 | ⚠️ Pozitif, anlamsız |
| **SPX** | 15m | SHORT | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +9.381R (399) | **+2.057R** (180) | %20.0 | 1.79 | 35.6 | 220.79R | 0.275 | ⚠️ Pozitif, anlamsız |

## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 5m | 15m | 30m | 1h | 4h |
|---|---|---|---|---|---|
| **XAU** | ⚠ +0.302R (21) | ⚠ +5.287R (300) | ❌ -0.001R (200) | ⏳ +0.626R (11) | ❌ -0.071R (63) |
| **XAG** | ❌ -0.010R (21) | ⚠ +0.030R (23) | ⏳ -0.105R (11) | ❌ -0.202R (41) | ❌ -0.067R (34) |
| **BTC** | ❌ -0.349R (84) | ❌ -0.205R (47) | ⚠ +0.071R (27) | ⚠ +0.249R (21) | ❌ -0.175R (45) |
| **ETH** | ❌ -0.066R (87) | ❌ -0.237R (175) | ❌ -0.049R (30) | ⚠ +0.100R (239) | ❌ -0.137R (31) |
| **NQ** | ⚠ +35107716.412R (474) | ⚠ +3.532R (211) | ❌ -0.499R (43) | ⚠ +12.482R (189) | ❌ -0.145R (29) |
| **SPX** | ❌ -0.139R (71) | ⚠ +2.057R (180) | ⚠ +0.209R (25) | ⚠ +1.507R (218) | ❌ -0.051R (21) |

## XAU

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 96,192 | 2024-10-11 → 2026-06-07 | 2026-06-07 → 2026-10-01 | çalıştı |
| 15m | 32,064 | 2024-10-11 → 2026-06-07 | 2026-06-07 → 2026-10-01 | çalıştı |
| 30m | 16,032 | 2024-10-11 → 2026-06-07 | 2026-06-07 → 2026-10-01 | çalıştı |
| 1h | 51,822 | 2020-10-02 → 2024-12-23 | 2024-12-23 → 2026-10-01 | çalıştı |
| 4h | 12,956 | 2020-10-02 → 2024-12-23 | 2024-12-23 → 2026-10-01 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **SEZON** | 15m | iki yön | saat etkisi UTC 11↑ 22↑ 23↑ | IZ_SUREN_2.5ATR | +64.983R (700) | +5.287R (300) | %23.0 | 5.41 | 0.050 | ⚠️ Pozitif, anlamsız |
| **OSC** | 30m | LONG | Stoch · dinamik · EMA200 trend | IZ_SUREN_2.5ATR | +1.272R (125) | +0.886R (26) | %42.3 | 2.62 | 0.053 | ⚠️ Pozitif, anlamsız |
| **PAIR** | 1h | iki yön | XAG'e göre göreli değer dönüşü ±2.0σ | IZ_SUREN_2.5ATR | +0.504R (367) | +0.715R (154) | %33.1 | 2.02 | 0.049 | ⚠️ Pozitif, anlamsız |
| **MA** | 30m | LONG | zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +1.502R (152) | +0.419R (66) | %22.7 | 1.45 | 0.294 | ⚠️ Pozitif, anlamsız |
| **LEADLAG** | 15m | LONG | XAG ani hareketini takip | IZ_SUREN_2.5ATR | +1.759R (54) | +0.365R (23) | %39.1 | 1.59 | 0.229 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 30m | LONG | anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.658R (145) | +0.293R (39) | %30.8 | 1.44 | 0.220 | ⚠️ Pozitif, anlamsız |
| **IMOM** | 30m | LONG | sabah getirisi → 15:30 NY yönü | IZ_SUREN_2.5ATR | +1.382R (110) | +0.161R (45) | %31.1 | 1.27 | 0.292 | ⚠️ Pozitif, anlamsız |
| **META** | 30m | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.248R (814) | +0.051R (416) | %29.3 | 1.07 | 0.308 | ⚠️ Pozitif, anlamsız |
| **VWAP** | 1h | iki yön | sapma dönüşü ±2.0σ · yatay rejim | GENIS_%50@1R>BE_3R | +0.015R (306) | -0.072R (128) | %48.4 | 0.86 | 0.777 | ❌ OOS'ta tutmadı |
| **RSI2** | 30m | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.506R (338) | -0.077R (151) | %27.2 | 0.90 | 0.672 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | iki yön | New York açılış 30dk · filtresiz | GENIS_%50@1R>BE_3R | +0.083R (173) | -0.089R (67) | %44.8 | 0.83 | 0.750 | ❌ OOS'ta tutmadı |
| **SQZ** | 15m | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_2R | +0.390R (45) | -0.091R (15) | %33.3 | 0.87 | 0.595 | ❌ OOS'ta tutmadı |
| **DONCH** | 30m | LONG | Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +1.145R (58) | -0.796R (26) | %11.5 | 0.14 | 1.000 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (15m) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.215R | %30.0 | %27.4 | -0.033R | %28.0 | 191 |
| %50@1R>BE_IZ | +0.062R | %30.0 | %49.7 | -0.057R | %51.0 | 191 |
| GENIS_%50@1R>BE_3R | -0.057R | %20.0 | %49.6 | -0.125R | %48.1 | 191 |
| SABIT_1.5R | -0.102R | %10.0 | %40.1 | -0.098R | %40.6 | 191 |
| SABIT_1R | -0.119R | %5.0 | %48.9 | -0.090R | %51.0 | 191 |
| SABIT_2R | -0.123R | %10.0 | %33.3 | -0.125R | %33.4 | 191 |
| %50@1R>BE_2R | -0.131R | %5.0 | %49.2 | -0.100R | %51.0 | 191 |
| %50@1R>BE_3R | -0.146R | %10.0 | %48.7 | -0.097R | %50.9 | 191 |
| TP1>BE_2R | -0.162R | %5.0 | %22.4 | -0.110R | %24.6 | 191 |
| SABIT_3R | -0.223R | %5.0 | %23.5 | -0.123R | %26.4 | 191 |
| TP1>BE_3R | -0.264R | %5.0 | %12.3 | -0.103R | %17.2 | 191 |

**Sağlamlık (15m):** IS'te en iyi 20 ayarın %15.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.303R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — SEZON · saat etkisi UTC 11↑ 22↑ 23↑ · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-10-11 → 2025-11-20 | 250 | %31.2 | +2.502R |
| 2025-11-20 → 2026-03-06 | 250 | %30.4 | +177.091R |
| 2026-03-06 → 2026-06-25 | 250 | %20.8 | +4.776R |
| 2026-06-26 → 2026-10-01 | 250 | %23.2 | +3.928R |

Maksimum düşüş: IS 886.76R · OOS 92.16R

### İlk 15 ayar (15m, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | SEZON · saat etkisi UTC 11↑ 22↑ 23↑ | IZ_SUREN_2.5ATR | +64.983R (700) | +5.287R (300) | %23.0 |
| 2 | SEZON · saat etkisi UTC 11↑ 22↑ 23↑ | %50@1R>BE_IZ | +30.142R (700) | +2.237R (300) | %40.7 |
| 3 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.367R (222) | -0.195R (103) | %29.1 |
| 4 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.230R (696) | -0.073R (313) | %26.8 |
| 5 | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.109R (1767) | -0.089R (772) | %25.4 |
| 6 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_2R | +0.390R (45) | -0.091R (15) | %33.3 |
| 7 | RSI2 · RSI(2) 5/95 · EMA200 trend | IZ_SUREN_2.5ATR | +0.328R (406) | +0.218R (186) | %33.9 |
| 8 | RSI2 · RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +0.097R (1133) | -0.011R (543) | %27.1 |
| 9 | META · gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.051R (2638) | -0.049R (1214) | %50.8 |
| 10 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.002R (2638) | -0.043R (1214) | %26.9 |
| 11 | META · gradient boosting · tüm adaylar · üst %35 | %50@1R>BE_IZ | -0.049R (2638) | -0.061R (1214) | %50.7 |
| 12 | ORB · New York açılış 15dk · filtresiz | SABIT_1R | +0.026R (209) | -0.044R (91) | %51.6 |
| 13 | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.130R (222) | -0.100R (103) | %25.2 |
| 14 | DONCH · Donchian 20 · hacim şoku | TP1>BE_2R | +0.063R (222) | -0.027R (103) | %29.1 |
| 15 | DONCH · Donchian 20 · hacim şoku | GENIS_%50@1R>BE_3R | +0.039R (222) | -0.140R (103) | %47.6 |

## XAG

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 127,080 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | çalıştı |
| 15m | 42,360 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | çalıştı |
| 30m | 21,180 | 2024-10-02 → 2025-10-01 | 2025-10-01 → 2026-10-01 | çalıştı |
| 1h | 52,566 | 2020-10-02 → 2024-12-13 | 2024-12-13 → 2026-10-01 | çalıştı |
| 4h | 13,142 | 2020-10-02 → 2024-12-13 | 2024-12-13 → 2026-10-01 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **REJIM** | 4h | iki yön | yatayda dönüş · RSI · filtresiz | GENIS_%50@1R>BE_3R | +0.170R (69) | +0.264R (29) | %58.6 | 1.61 | 0.129 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 15m | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | -0.046R (43) | +0.084R (13) | %46.2 | 1.15 | 0.414 | ⏳ OOS yetersiz |
| **IMOM** | 30m | SHORT | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.074R (121) | +0.039R (50) | %58.0 | 1.10 | 0.386 | ⚠️ Pozitif, anlamsız |
| **OSC** | 5m | LONG | RSI+WaveTrend · sabit · hacim şoku+volatilite şoku | TP1>BE_3R | +0.487R (62) | -0.010R (21) | %19.0 | 0.98 | 0.513 | ❌ OOS'ta tutmadı |
| **SEZON** | 30m | iki yön | saat etkisi UTC 03↑ | GENIS_%50@1R>BE_3R | -0.187R (309) | -0.041R (131) | %47.3 | 0.93 | 0.654 | ❌ OOS'ta tutmadı |
| **MA** | 4h | SHORT | EMA 20/50 kesişimi | GENIS_%50@1R>BE_3R | +0.328R (81) | -0.067R (34) | %47.1 | 0.88 | 0.631 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | iki yön | Donchian 20 · filtresiz | GENIS_%50@1R>BE_3R | -0.084R (353) | -0.068R (160) | %45.6 | 0.88 | 0.769 | ❌ OOS'ta tutmadı |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.045R (1066) | -0.084R (515) | %47.4 | 0.85 | 0.956 | ❌ OOS'ta tutmadı |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | -0.019R (398) | -0.093R (152) | %45.4 | 0.84 | 0.841 | ❌ OOS'ta tutmadı |
| **PAIR** | 4h | iki yön | XAU'e göre göreli değer dönüşü ±2.0σ | SABIT_3R | +0.181R (96) | -0.095R (52) | %25.0 | 0.88 | 0.657 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | LONG | New York açılış 30dk · hacim şoku | GENIS_%50@1R>BE_3R | +0.317R (47) | -0.105R (11) | %54.5 | 0.77 | 0.640 | ⏳ OOS yetersiz |
| **VWAP** | 1h | SHORT | sapma dönüşü ±2.5σ · filtresiz | GENIS_%50@1R>BE_3R | -0.087R (327) | -0.166R (147) | %46.9 | 0.69 | 0.978 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 4h | iki yön | XAU ani hareketini takip | GENIS_%50@1R>BE_3R | +0.096R (86) | -0.191R (45) | %42.2 | 0.68 | 0.876 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | -0.008R | %47.4 | %26.1 | -0.059R | %24.1 | 85 |
| GENIS_%50@1R>BE_3R | -0.036R | %20.0 | %47.9 | -0.107R | %45.5 | 85 |
| %50@1R>BE_IZ | -0.089R | %10.0 | %48.2 | -0.120R | %47.3 | 85 |
| SABIT_2R | -0.090R | %20.0 | %32.3 | -0.184R | %28.9 | 85 |
| SABIT_1R | -0.097R | %15.8 | %48.0 | -0.110R | %47.3 | 85 |
| SABIT_1.5R | -0.116R | %10.0 | %37.6 | -0.162R | %35.6 | 85 |
| SABIT_3R | -0.120R | %15.0 | %23.8 | -0.160R | %22.7 | 85 |
| %50@1R>BE_3R | -0.121R | %10.0 | %47.5 | -0.153R | %47.3 | 85 |
| %50@1R>BE_2R | -0.134R | %10.0 | %47.0 | -0.150R | %47.3 | 85 |
| TP1>BE_3R | -0.138R | %5.3 | %15.0 | -0.196R | %13.1 | 85 |
| TP1>BE_2R | -0.139R | %5.0 | %22.5 | -0.190R | %19.7 | 85 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.102R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · EMA 20/50 kesişimi · GENIS_%50@1R>BE_3R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2020-10-07 → 2022-03-14 | 28 | %53.6 | +0.032R |
| 2022-03-28 → 2023-07-27 | 29 | %65.5 | +0.403R |
| 2023-09-04 → 2025-04-03 | 29 | %69.0 | +0.508R |
| 2025-04-30 → 2026-09-10 | 29 | %48.3 | -0.104R |

Maksimum düşüş: IS 8.75R · OOS 6.77R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | MA · EMA 20/50 kesişimi | GENIS_%50@1R>BE_3R | +0.188R (162) | -0.039R (69) | %47.8 |
| 2 | MA · EMA 20/50 kesişimi | %50@1R>BE_IZ | +0.153R (162) | -0.114R (69) | %46.4 |
| 3 | MA · EMA 20/50 kesişimi | %50@1R>BE_3R | +0.089R (162) | -0.189R (69) | %46.4 |
| 4 | REJIM · yatayda dönüş · RSI · filtresiz | GENIS_%50@1R>BE_3R | +0.170R (69) | +0.264R (29) | %58.6 |
| 5 | MA · EMA 20/50 kesişimi | TP1>BE_3R | +0.136R (162) | -0.247R (69) | %11.6 |
| 6 | MA · zaman serisi momentumu 72 bar | TP1>BE_3R | +0.098R (233) | -0.108R (106) | %17.9 |
| 7 | MA · zaman serisi momentumu 72 bar | GENIS_%50@1R>BE_3R | +0.042R (233) | -0.073R (106) | %46.2 |
| 8 | MA · EMA 20/50 kesişimi | SABIT_1R | +0.043R (162) | -0.131R (69) | %46.4 |
| 9 | META · gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.045R (1066) | -0.084R (515) | %47.4 |
| 10 | MA · EMA 20/50 kesişimi | %50@1R>BE_2R | +0.049R (162) | -0.160R (69) | %46.4 |
| 11 | MA · zaman serisi momentumu 72 bar | %50@1R>BE_3R | +0.030R (233) | -0.169R (106) | %41.5 |
| 12 | RSI2 · RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | -0.053R (805) | -0.115R (336) | %46.7 |
| 13 | MA · EMA 20/50 kesişimi | SABIT_1.5R | +0.059R (162) | -0.153R (69) | %36.2 |
| 14 | MA · zaman serisi momentumu 72 bar | SABIT_3R | +0.100R (233) | -0.098R (106) | %24.5 |
| 15 | MA · EMA 20/50 kesişimi | TP1>BE_2R | +0.055R (162) | -0.189R (69) | %20.3 |

## BTC

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 210,240 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 15m | 70,081 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 30m | 35,041 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 1h | 52,564 | 2020-10-02 → 2024-12-14 | 2024-12-14 → 2026-10-02 | çalıştı |
| 4h | 13,147 | 2020-10-02 → 2024-12-14 | 2024-12-14 → 2026-10-02 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | +0.300R (99) | +0.249R (21) | %76.2 | 1.90 | 0.116 | ⚠️ Pozitif, anlamsız |
| **PAIR** | 4h | LONG | ETH'e göre göreli değer dönüşü ±1.5σ | SABIT_3R | +0.402R (56) | +0.186R (35) | %31.4 | 1.25 | 0.280 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.559R (184) | +0.144R (63) | %27.0 | 1.20 | 0.335 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.301R (561) | -0.015R (299) | %25.1 | 0.98 | 0.546 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.260R (378) | -0.082R (182) | %24.7 | 0.89 | 0.705 | ❌ OOS'ta tutmadı |
| **SEZON** | 1h | iki yön | saat etkisi UTC 16↑ | IZ_SUREN_2.5ATR | +0.004R (1533) | -0.130R (655) | %25.6 | 0.83 | 0.957 | ❌ OOS'ta tutmadı |
| **VWAP** | 1h | LONG | VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | +0.295R (391) | -0.135R (159) | %22.0 | 0.83 | 0.790 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 4h | iki yön | ETH ani hareketini takip | GENIS_%50@1R>BE_3R | +0.182R (48) | -0.144R (30) | %43.3 | 0.76 | 0.752 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | SHORT | Donchian 20 · hacim şoku | SABIT_1.5R | +0.524R (79) | -0.175R (45) | %35.6 | 0.75 | 0.834 | ❌ OOS'ta tutmadı |
| **ORB** | 15m | SHORT | New York açılış 30dk · hacim şoku | GENIS_%50@1R>BE_3R | +0.129R (128) | -0.205R (47) | %46.8 | 0.66 | 0.897 | ❌ OOS'ta tutmadı |
| **IMOM** | 30m | SHORT | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.111R (177) | -0.216R (86) | %46.5 | 0.62 | 0.974 | ❌ OOS'ta tutmadı |
| **REJIM** | 1h | SHORT | yatayda dönüş · Stoch · volatilite şoku | SABIT_2R | +0.252R (100) | -0.227R (35) | %31.4 | 0.71 | 0.836 | ❌ OOS'ta tutmadı |
| **FUNDING** | 4h | LONG | fonlama uç değeri ±2.0σ (kalabalığa karşı) | SABIT_1.5R | +0.373R (65) | -0.268R (44) | %31.8 | 0.63 | 0.934 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch+WaveTrend · dinamik · EMA200 trend | SABIT_2R | +0.589R (44) | -0.367R (17) | %23.5 | 0.55 | 0.876 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.087R | %10.0 | %47.5 | -0.091R | %46.5 | 183 |
| SABIT_3R | -0.150R | %20.0 | %23.5 | -0.148R | %23.5 | 183 |
| IZ_SUREN_2.5ATR | -0.154R | %25.0 | %22.5 | -0.139R | %25.8 | 183 |
| SABIT_1R | -0.160R | %5.0 | %45.4 | -0.166R | %44.8 | 183 |
| %50@1R>BE_3R | -0.165R | %5.0 | %45.7 | -0.131R | %44.8 | 183 |
| %50@1R>BE_IZ | -0.167R | %5.0 | %45.7 | -0.136R | %44.8 | 183 |
| TP1>BE_3R | -0.187R | %5.0 | %14.5 | -0.096R | %17.8 | 183 |
| %50@1R>BE_2R | -0.191R | %5.0 | %45.1 | -0.143R | %44.8 | 183 |
| SABIT_1.5R | -0.202R | %0.0 | %34.6 | -0.184R | %35.2 | 183 |
| SABIT_2R | -0.212R | %5.0 | %28.6 | -0.160R | %30.1 | 183 |
| TP1>BE_2R | -0.223R | %0.0 | %19.9 | -0.120R | %24.7 | 183 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.175R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · hacim şoku · SABIT_1.5R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2020-11-26 → 2022-02-24 | 31 | %58.1 | +0.420R |
| 2022-03-07 → 2024-01-12 | 31 | %74.2 | +0.766R |
| 2024-03-15 → 2025-07-30 | 31 | %45.2 | +0.072R |
| 2025-08-25 → 2026-09-10 | 31 | %35.5 | -0.177R |

Maksimum düşüş: IS 5.14R · OOS 11.44R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.597R (175) | -0.289R (88) | %18.2 |
| 2 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.610R (191) | -0.120R (89) | %21.3 |
| 3 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_IZ | +0.349R (175) | -0.188R (88) | %42.0 |
| 4 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.506R (234) | -0.054R (106) | %23.6 |
| 5 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.404R (334) | +0.155R (142) | %26.1 |
| 6 | DONCH · Donchian 55 · hacim şoku | %50@1R>BE_IZ | +0.353R (130) | -0.202R (64) | %43.8 |
| 7 | DONCH · Donchian 20 · hacim şoku | SABIT_1R | +0.238R (175) | -0.229R (88) | %42.0 |
| 8 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_3R | +0.258R (175) | -0.217R (88) | %42.0 |
| 9 | DONCH · Donchian 20 · hacim şoku | SABIT_1.5R | +0.271R (175) | -0.274R (88) | %31.8 |
| 10 | DONCH · Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.578R (130) | -0.365R (64) | %15.6 |
| 11 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_2R | +0.230R (175) | -0.223R (88) | %42.0 |
| 12 | DONCH · Donchian 20 · sıkışma sonrası | %50@1R>BE_IZ | +0.256R (191) | -0.125R (89) | %51.7 |
| 13 | DONCH · Donchian 20 · hacim şoku | GENIS_%50@1R>BE_3R | +0.241R (175) | -0.214R (88) | %42.0 |
| 14 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.283R (191) | -0.188R (89) | %12.4 |
| 15 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.278R (175) | -0.206R (88) | %14.8 |

## ETH

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 210,240 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 15m | 70,081 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 30m | 35,041 | 2024-10-02 → 2026-02-25 | 2026-02-25 → 2026-10-02 | çalıştı |
| 1h | 52,564 | 2020-10-02 → 2024-12-14 | 2024-12-14 → 2026-10-02 | çalıştı |
| 4h | 13,147 | 2020-10-02 → 2024-12-14 | 2024-12-14 → 2026-10-02 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.093R (2438) | +0.100R (239) | %26.8 | 1.14 | 0.287 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | LONG | Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.416R (57) | +0.046R (25) | %56.0 | 1.10 | 0.415 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.261R (428) | +0.039R (186) | %26.3 | 1.06 | 0.422 | ⚠️ Pozitif, anlamsız |
| **IMOM** | 30m | iki yön | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | -0.066R (364) | -0.044R (156) | %52.6 | 0.91 | 0.690 | ❌ OOS'ta tutmadı |
| **MA** | 4h | LONG | EMA 9/21 kesişimi | %50@1R>BE_IZ | +0.233R (197) | -0.106R (105) | %43.8 | 0.82 | 0.800 | ❌ OOS'ta tutmadı |
| **VWAP** | 30m | iki yön | VWAP kırılımı · hacim şoku | IZ_SUREN_2.5ATR | +0.247R (461) | -0.127R (211) | %27.0 | 0.84 | 0.836 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | iki yön | yatayda dönüş · Stoch · volatilite şoku | TP1>BE_3R | +0.714R (56) | -0.137R (31) | %12.9 | 0.74 | 0.720 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch · sabit · EMA200 trend | TP1>BE_2R | +0.462R (66) | -0.168R (42) | %19.0 | 0.69 | 0.831 | ❌ OOS'ta tutmadı |
| **LEADLAG** | 1h | LONG | BTC ani hareketini takip | GENIS_%50@1R>BE_3R | +0.194R (96) | -0.171R (44) | %45.5 | 0.70 | 0.852 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | iki yön | New York açılış 30dk · hacim şoku | SABIT_2R | +0.144R (188) | -0.221R (85) | %30.6 | 0.72 | 0.930 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | SHORT | BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_1R | +0.215R (57) | -0.246R (20) | %40.0 | 0.61 | 0.864 | ❌ OOS'ta tutmadı |
| **SEZON** | 15m | iki yön | saat etkisi UTC 21↑ | GENIS_%50@1R>BE_3R | -0.059R (510) | -0.283R (219) | %43.4 | 0.56 | 1.000 | ❌ OOS'ta tutmadı |
| **PAIR** | 4h | LONG | BTC'e göre göreli değer dönüşü ±2.0σ | GENIS_%50@1R>BE_3R | +0.331R (66) | -0.377R (31) | %41.9 | 0.37 | 0.996 | ❌ OOS'ta tutmadı |
| **FUNDING** | 30m | iki yön | fonlama uç değeri ±2.0σ (kalabalığa karşı) | %50@1R>BE_IZ | +0.328R (51) | -0.446R (24) | %37.5 | 0.38 | 0.984 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.090R | %50.0 | %27.6 | +0.014R | %25.1 | 173 |
| SABIT_3R | +0.072R | %50.0 | %28.4 | -0.074R | %25.1 | 173 |
| SABIT_1R | +0.014R | %35.0 | %52.8 | -0.077R | %48.1 | 173 |
| %50@1R>BE_IZ | +0.000R | %50.0 | %49.6 | -0.028R | %48.1 | 173 |
| SABIT_1.5R | -0.017R | %35.0 | %41.1 | -0.159R | %35.2 | 173 |
| GENIS_%50@1R>BE_3R | -0.049R | %30.0 | %48.2 | -0.026R | %47.6 | 173 |
| %50@1R>BE_3R | -0.064R | %25.0 | %48.7 | -0.072R | %48.1 | 173 |
| TP1>BE_3R | -0.081R | %20.0 | %16.4 | -0.067R | %16.8 | 173 |
| SABIT_2R | -0.086R | %25.0 | %31.8 | -0.119R | %30.6 | 173 |
| %50@1R>BE_2R | -0.091R | %10.0 | %49.0 | -0.072R | %48.1 | 173 |
| TP1>BE_2R | -0.139R | %10.0 | %21.2 | -0.067R | %24.6 | 173 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %15.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.090R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — REJIM · yatayda dönüş · Stoch · volatilite şoku · TP1>BE_3R · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2020-11-03 → 2021-11-29 | 21 | %28.6 | +0.402R |
| 2022-02-28 → 2023-02-13 | 22 | %54.5 | +1.369R |
| 2023-03-23 → 2025-06-13 | 22 | %18.2 | +0.278R |
| 2025-06-16 → 2026-09-24 | 22 | %9.1 | -0.406R |

Maksimum düşüş: IS 4.47R · OOS 10.14R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | REJIM · yatayda dönüş · Stoch · volatilite şoku | TP1>BE_3R | +0.714R (56) | -0.137R (31) | %12.9 |
| 2 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | TP1>BE_3R | +0.605R (73) | -0.145R (38) | %13.2 |
| 3 | REJIM · yatayda dönüş · Stoch · volatilite şoku | %50@1R>BE_3R | +0.517R (56) | -0.072R (31) | %51.6 |
| 4 | REJIM · yatayda dönüş · Stoch · volatilite şoku | TP1>BE_2R | +0.535R (56) | -0.201R (31) | %16.1 |
| 5 | REJIM · yatayda dönüş · Stoch · volatilite şoku | SABIT_2R | +0.571R (56) | -0.459R (31) | %19.4 |
| 6 | REJIM · yatayda dönüş · Stoch · volatilite şoku | %50@1R>BE_2R | +0.428R (56) | -0.104R (31) | %51.6 |
| 7 | REJIM · yatayda dönüş · Stoch · volatilite şoku | SABIT_3R | +0.644R (56) | -0.266R (31) | %19.4 |
| 8 | REJIM · yatayda dönüş · Stoch · volatilite şoku | %50@1R>BE_IZ | +0.439R (56) | -0.098R (31) | %51.6 |
| 9 | REJIM · yatayda dönüş · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.410R (56) | -0.287R (31) | %38.7 |
| 10 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.375R (73) | -0.147R (38) | %44.7 |
| 11 | REJIM · yatayda dönüş · Stoch · volatilite şoku | SABIT_1.5R | +0.437R (56) | -0.153R (31) | %35.5 |
| 12 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | %50@1R>BE_3R | +0.400R (73) | -0.092R (38) | %50.0 |
| 13 | OSC · Stoch · sabit · volatilite şoku+EMA200 trend+onay mumu | SABIT_1R | +0.358R (50) | +0.083R (32) | %56.2 |
| 14 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.524R (186) | +0.570R (81) | %35.8 |
| 15 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | TP1>BE_2R | +0.400R (73) | -0.224R (38) | %15.8 |

## NQ

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 78,407 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | çalıştı |
| 15m | 26,136 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | çalıştı |
| 30m | 13,068 | 2024-10-02 → 2026-06-29 | 2026-06-29 → 2026-10-01 | çalıştı |
| 1h | 48,903 | 2020-12-01 → 2024-10-27 | 2024-10-27 → 2026-10-02 | çalıştı |
| 4h | 12,310 | 2020-12-01 → 2024-11-06 | 2024-11-06 → 2026-10-02 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **VWAP** | 5m | iki yön | sapma dönüşü ±2.0σ · filtresiz | IZ_SUREN_2.5ATR | +87320626.004R (1273) | +35107716.412R (474) | %19.8 | 464.55 | 0.159 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 1h | iki yön | Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.144R (883) | +24.452R (352) | %27.8 | 35.60 | 0.046 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +0.217R (266) | +24.370R (101) | %28.7 | 37.13 | 0.091 | ⚠️ Pozitif, anlamsız |
| **MA** | 1h | LONG | zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +2.986R (469) | +12.482R (189) | %28.0 | 16.20 | 0.140 | ⚠️ Pozitif, anlamsız |
| **PAIR** | 1h | iki yön | SPX'e göre göreli değer dönüşü ±1.5σ | IZ_SUREN_2.5ATR | +0.670R (509) | +4.523R (159) | %28.3 | 7.06 | 0.101 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | TP1>BE_3R | +0.502R (59) | +0.304R (29) | %27.6 | 1.59 | 0.170 | ⚠️ Pozitif, anlamsız |
| **LEADLAG** | 1h | iki yön | SPX ani hareketini takip | GENIS_%50@1R>BE_3R | -0.071R (118) | +0.012R (73) | %53.4 | 1.03 | 0.456 | ⚠️ Pozitif, anlamsız |
| **IMOM** | 30m | iki yön | sabah getirisi → 15:30 NY yönü | GENIS_%50@1R>BE_3R | +0.062R (159) | -0.075R (68) | %50.0 | 0.84 | 0.731 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | RSI+Stoch+WaveTrend · dinamik · EMA200 trend | SABIT_3R | +0.773R (44) | -0.145R (29) | %24.1 | 0.82 | 0.682 | ❌ OOS'ta tutmadı |
| **META** | 30m | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.347R (526) | -0.260R (395) | %24.3 | 0.67 | 0.999 | ❌ OOS'ta tutmadı |
| **ORB** | 15m | LONG | New York açılış 30dk · hacim şoku | SABIT_1.5R | +0.245R (81) | -0.491R (29) | %24.1 | 0.41 | 0.993 | ❌ OOS'ta tutmadı |
| **REJIM** | 30m | LONG | anahtar (ikisi) · WaveTrend · filtresiz | SABIT_1.5R | +0.306R (66) | -0.805R (22) | %13.6 | 0.16 | 1.000 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (5m) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +1755385.621R | %5.0 | %24.8 | +376308.966R | %24.2 | 247 |
| SABIT_3R | -0.030R | %30.0 | %29.9 | -10714.684R | %25.1 | 247 |
| SABIT_2R | -0.063R | %30.0 | %38.4 | -10714.678R | %33.0 | 247 |
| TP1>BE_2R | -0.111R | %25.0 | %30.9 | -10714.641R | %27.7 | 247 |
| TP1>BE_3R | -0.118R | %10.0 | %20.5 | -10714.621R | %19.3 | 247 |
| SABIT_1.5R | -0.133R | %15.8 | %42.9 | -10714.696R | %38.9 | 247 |
| %50@1R>BE_3R | -0.150R | %10.0 | %48.4 | -10714.670R | %46.6 | 247 |
| GENIS_%50@1R>BE_3R | -0.172R | %0.0 | %48.5 | -7143.130R | %46.4 | 247 |
| %50@1R>BE_2R | -0.175R | %0.0 | %48.2 | -10714.680R | %47.0 | 247 |
| %50@1R>BE_IZ | -0.177R | %10.0 | %48.1 | +182797.158R | %46.8 | 247 |
| SABIT_1R | -0.252R | %0.0 | %47.8 | -10714.719R | %47.4 | 247 |

**Sağlamlık (5m):** IS'te en iyi 20 ayarın %35.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +1755385.770R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — VWAP · sapma dönüşü ±2.0σ · filtresiz · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-10-03 → 2025-02-18 | 436 | %22.0 | +116214820.022R |
| 2025-02-18 → 2026-04-09 | 437 | %22.0 | +160331223.810R |
| 2026-04-09 → 2026-07-06 | 437 | %23.3 | -21911326.050R |
| 2026-07-06 → 2026-10-01 | 437 | %19.9 | +38080223.412R |

Maksimum düşüş: IS 9838770851.53R · OOS 35898757.63R

### İlk 15 ayar (5m, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | VWAP · sapma dönüşü ±2.0σ · filtresiz | IZ_SUREN_2.5ATR | +87320626.004R (1273) | +35107716.412R (474) | %19.8 |
| 2 | OSC · RSI+WaveTrend · sabit · volatilite şoku+onay mumu | SABIT_2R | +0.123R (108) | +0.091R (32) | %43.8 |
| 3 | OSC · RSI+WaveTrend · sabit · volatilite şoku | SABIT_2R | +0.108R (109) | +0.091R (32) | %43.8 |
| 4 | DONCH · Donchian 55 · hacim şoku | GENIS_%50@1R>BE_3R | -0.079R (398) | -0.127R (140) | %50.7 |
| 5 | META · gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.175R (5909) | -0.177R (5362) | %47.7 |
| 6 | OSC · RSI · sabit · volatilite şoku+onay mumu | SABIT_2R | +0.061R (116) | -0.069R (39) | %38.5 |
| 7 | REJIM · yatayda dönüş · WaveTrend · filtresiz | GENIS_%50@1R>BE_3R | -0.096R (370) | -0.211R (172) | %45.9 |
| 8 | OSC · RSI+Stoch+WaveTrend · sabit · volatilite şoku+onay mumu | SABIT_2R | +0.066R (108) | +0.091R (32) | %43.8 |
| 9 | OSC · RSI+WaveTrend · sabit · volatilite şoku+onay mumu | SABIT_3R | +0.140R (108) | +0.278R (32) | %37.5 |
| 10 | OSC · RSI · sabit · volatilite şoku | SABIT_2R | +0.049R (117) | -0.069R (39) | %38.5 |
| 11 | OSC · RSI+WaveTrend · sabit · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | -0.011R (108) | -0.070R (32) | %53.1 |
| 12 | META · gradient boosting · tüm adaylar · üst %35 | %50@1R>BE_IZ | -0.195R (5909) | -0.252R (5362) | %47.8 |
| 13 | OSC · RSI+Stoch+WaveTrend · sabit · volatilite şoku | SABIT_2R | +0.051R (109) | +0.091R (32) | %43.8 |
| 14 | OSC · RSI+WaveTrend · sabit · volatilite şoku | SABIT_3R | +0.124R (109) | +0.278R (32) | %37.5 |
| 15 | DONCH · Donchian 55 · hacim şoku | SABIT_3R | -0.051R (398) | -0.044R (140) | %30.0 |

## SPX

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Meta-model |
|---|---|---|---|---|
| 5m | 127,584 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | çalıştı |
| 15m | 42,528 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | çalıştı |
| 30m | 21,264 | 2024-10-03 → 2026-04-30 | 2026-04-30 → 2026-10-01 | çalıştı |
| 1h | 52,565 | 2020-10-02 → 2024-12-13 | 2024-12-13 → 2026-10-01 | çalıştı |
| 4h | 13,142 | 2020-10-02 → 2024-12-13 | 2024-12-13 → 2026-10-01 | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|
| **MA** | 15m | SHORT | zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +9.381R (399) | +2.057R (180) | %20.0 | 1.79 | 0.275 | ⚠️ Pozitif, anlamsız |
| **LEADLAG** | 1h | SHORT | NQ ani hareketini takip | TP1>BE_3R | +0.192R (70) | +0.818R (18) | %44.4 | 3.33 | 0.025 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | +0.196R (57) | +0.280R (27) | %59.3 | 1.66 | 0.124 | ⚠️ Pozitif, anlamsız |
| **OSC** | 30m | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +1.017R (56) | +0.209R (25) | %24.0 | 1.25 | 0.367 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.263R (478) | +0.095R (264) | %26.5 | 1.13 | 0.261 | ⚠️ Pozitif, anlamsız |
| **VWAP** | 30m | iki yön | sapma dönüşü ±2.5σ · filtresiz | %50@1R>BE_IZ | +0.011R (230) | +0.076R (94) | %59.6 | 1.17 | 0.249 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.391R (235) | -0.015R (89) | %27.0 | 0.98 | 0.522 | ❌ OOS'ta tutmadı |
| **PAIR** | 1h | LONG | NQ'e göre göreli değer dönüşü ±2.0σ | %50@1R>BE_IZ | +0.206R (175) | -0.172R (67) | %47.8 | 0.73 | 0.849 | ❌ OOS'ta tutmadı |
| **ORB** | 30m | LONG | New York açılış 30dk · hacim şoku | SABIT_3R | +0.305R (97) | -0.264R (42) | %21.4 | 0.70 | 0.850 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | SHORT | Donchian 20 · filtresiz | SABIT_3R | +0.310R (163) | -0.268R (82) | %20.7 | 0.68 | 0.937 | ❌ OOS'ta tutmadı |
| **IMOM** | 30m | LONG | sabah getirisi → 15:30 NY yönü | %50@1R>BE_IZ | +0.100R (141) | -0.317R (58) | %36.2 | 0.51 | 0.988 | ❌ OOS'ta tutmadı |
| **REJIM** | 30m | LONG | yatayda dönüş · RSI+Stoch+WaveTrend · filtresiz | SABIT_3R | +0.660R (43) | -0.390R (14) | %21.4 | 0.57 | 0.829 | ⏳ OOS yetersiz |

### Çıkış yöntemleri (15m) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | -0.105R | %5.0 | %21.4 | -0.303R | %24.4 | 225 |
| SABIT_1.5R | -0.238R | %0.0 | %38.0 | -0.320R | %36.8 | 225 |
| GENIS_%50@1R>BE_3R | -0.246R | %0.0 | %45.9 | -0.263R | %45.7 | 225 |
| %50@1R>BE_2R | -0.285R | %0.0 | %44.9 | -0.301R | %45.7 | 225 |
| SABIT_1R | -0.288R | %0.0 | %45.7 | -0.313R | %46.2 | 225 |
| TP1>BE_2R | -0.295R | %0.0 | %23.2 | -0.289R | %24.5 | 225 |
| SABIT_2R | -0.312R | %0.0 | %29.7 | -0.294R | %31.6 | 225 |
| %50@1R>BE_3R | -0.346R | %0.0 | %43.0 | -0.290R | %45.6 | 225 |
| TP1>BE_3R | -0.367R | %0.0 | %14.6 | -0.268R | %17.3 | 225 |
| SABIT_3R | -0.370R | %0.0 | %21.8 | -0.264R | %25.1 | 225 |
| %50@1R>BE_IZ | -0.413R | %0.0 | %41.6 | -0.302R | %45.6 | 225 |

**Sağlamlık (15m):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.109R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · zaman serisi momentumu 72 bar · IZ_SUREN_2.5ATR · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-10-03 → 2025-04-01 | 144 | %16.0 | +6.481R |
| 2025-04-03 → 2026-01-25 | 145 | %17.9 | +4.415R |
| 2026-01-25 → 2026-05-31 | 145 | %20.0 | +15.766R |
| 2026-06-01 → 2026-10-01 | 145 | %19.3 | +1.751R |

Maksimum düşüş: IS 212.46R · OOS 220.79R

### İlk 15 ayar (15m, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +5.064R (799) | +5.781R (353) | %19.8 |
| 2 | OSC · RSI+Stoch+WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.747R (41) | -0.571R (20) | %20.0 |
| 3 | OSC · RSI+Stoch+WaveTrend · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_2R | +0.343R (40) | -0.940R (20) | %10.0 |
| 4 | OSC · RSI+Stoch+WaveTrend · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.678R (43) | -0.557R (21) | %19.0 |
| 5 | OSC · RSI+Stoch+WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_2R | +0.302R (41) | -0.487R (20) | %25.0 |
| 6 | OSC · RSI+Stoch+WaveTrend · dinamik · hacim şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.496R (40) | -0.892R (20) | %10.0 |
| 7 | DONCH · Donchian 20 · hacim şoku | GENIS_%50@1R>BE_3R | -0.064R (361) | -0.346R (156) | %43.6 |
| 8 | OSC · RSI+Stoch+WaveTrend · dinamik · hacim şoku+onay mumu | SABIT_2R | +0.027R (184) | -0.494R (85) | %23.5 |
| 9 | ORB · New York açılış 15dk · hacim şoku | GENIS_%50@1R>BE_3R | -0.042R (235) | -0.119R (109) | %49.5 |
| 10 | ORB · New York açılış 15dk · filtresiz | GENIS_%50@1R>BE_3R | -0.059R (280) | -0.166R (131) | %47.3 |
| 11 | MA · EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | -0.123R (1009) | -0.229R (479) | %47.8 |
| 12 | OSC · RSI+WaveTrend · dinamik · hacim şoku+EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.102R (59) | -0.613R (26) | %30.8 |
| 13 | META · gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.162R (3286) | -0.147R (1333) | %48.6 |
| 14 | DONCH · Donchian 55 · hacim şoku | GENIS_%50@1R>BE_3R | -0.064R (280) | -0.186R (112) | %50.0 |
| 15 | OSC · RSI+Stoch · dinamik · hacim şoku+onay mumu | SABIT_2R | -0.018R (240) | -0.354R (108) | %27.8 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` (her varlık×ZD için IS'te ilk 150 + her ailenin en iyisi) · `reports/en_iyi.json`
