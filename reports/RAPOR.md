# ATVS Lab v2 Raporu — 2026-10-02 19:17 UTC

**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).
**Seçim** ilk %70 veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %30 (OOS) verisine göre** verilir. ✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · ⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.
Giriş: sinyalden sonraki bar açılışı · zaman bariyeri 48 bar · aynı barda hedef+stop = stop. TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.

**Odak:** zaman dilimleri 1h, 4h · aileler MA, DONCH, SQZ, RSI2, REJIM, OSC, META. **Alfa** = aynı çıkışla aynı dönemde rastgele girişe göre fark (piyasanın kendi yükselişini ayıklar). 🚩 = fiziksel olarak inandırıcı olmayan sonuç (veri hatası belirtisi) — seçimden çıkarılır.

## Veri doğrulama (yfinance günlük kapanışla ay ay karşılaştırma)

| Varlık | Taban | Referans | Durum | Ay | Düzeltilen ay | Atılan ay | Atılan sıçrama | Medyan sapma |
|---|---|---|---|---|---|---|---|---|
| XAU | 1h | GC=F | temiz | 8 | 0 | 0 | 0 | %0.1 |
| XAG | 1h | SI=F | temiz | 6 | 0 | 0 | 0 | %0.6 |
| BTC | 1h | BTC-USD | düzeltildi | 111 | 0 | 0 | 9 | %0.1 |
| ETH | 1h | ETH-USD | düzeltildi | 108 | 0 | 0 | 4 | %0.1 |
| NQ | 1h | NQ=F | düzeltildi | 63 | 37 | 0 | 0 | %0.1 |
| SPX | 1h | ES=F | temiz | 30 | 0 | 0 | 0 | %0.0 |

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1h | iki yön | DONCH · Donchian 55 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.541R (41) | **+0.029R** (25) | -0.004R | %52.0 | 1.06 | 0.4 | 4.67R | 0.448 | ⚠️ Pozitif, anlamsız |
| **XAG** | 1h | SHORT | OSC · Stoch · dinamik · filtresiz | SABIT_1.5R | +0.400R (50) | **+0.030R** (22) | +0.136R | %45.5 | 1.05 | 12.9 | 6.67R | 0.456 | ⚠️ Pozitif, anlamsız |
| **BTC** | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | **+0.030R** (132) | +0.031R | %25.0 | 1.04 | 4.0 | 36.38R | 0.439 | ⚠️ Pozitif, anlamsız |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | **+0.329R** (61) | +0.311R | %34.4 | 1.48 | 1.9 | 11.52R | 0.090 | ⚠️ Pozitif, anlamsız |
| **NQ** | 1h | LONG | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.793R (206) | **+0.842R** (96) | +0.743R | %36.5 | 2.52 | 1.2 | 4.68R | 0.006 | ✅ Kanıtlı |
| **SPX** | 4h | SHORT | MA · EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | +0.401R (46) | **+0.123R** (26) | +0.090R | %57.7 | 1.28 | 3.0 | 3.75R | 0.292 | ⚠️ Pozitif, anlamsız |

## Portföy (IS'te seçilen stratejilerin birlikte çalışması)

Seçim kuralı (yalnızca IS): IS beklentisi > 0, t ≥ 1.5, varlık başına en fazla 3, aynı varlıkta aynı aile bir kez, toplam en fazla 15. OOS penceresi: **2020-01-20 → bugün** (her strateji yalnızca kendi OOS döneminde işlem yapar; 1h/4h stratejileri kısa geçmiş nedeniyle sonradan katılır). Stratejiler arası ortalama günlük korelasyon: **0.03** (0'a yakın = iyi çeşitlendirme).

| # | Varlık | ZD | Yön | Giriş | Çıkış | IS t | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ETH | 4h | LONG | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_2R | 4.65 | +0.410R (141) | +0.100R (61) | %55.7 |
| 2 | NQ | 1h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 4.25 | +0.322R (1152) | +0.236R (803) | %32.4 |
| 3 | BTC | 4h | iki yön | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 4.24 | +0.271R (1618) | +0.053R (965) | %25.8 |
| 4 | BTC | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | 3.82 | +0.639R (306) | +0.030R (132) | %25.0 |
| 5 | ETH | 1h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 3.68 | +0.152R (3290) | +0.005R (920) | %26.7 |
| 6 | NQ | 1h | LONG | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | TP1>BE_2R | 3.51 | +0.478R (96) | +0.305R (44) | %36.4 |
| 7 | NQ | 1h | LONG | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | 3.41 | +0.793R (206) | +0.842R (96) | %36.5 |
| 8 | ETH | 1h | iki yön | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 3.40 | +0.193R (2033) | -0.043R (888) | %26.5 |
| 9 | XAU | 1h | iki yön | DONCH · Donchian 55 · EMA200 trend | GENIS_%50@1R>BE_3R | 2.79 | +0.541R (41) | +0.029R (25) | %52.0 |
| 10 | XAU | 1h | iki yön | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | 2.71 | +0.510R (107) | +0.287R (42) | %33.3 |
| 11 | BTC | 1h | LONG | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 2.49 | +0.183R (1068) | -0.072R (476) | %27.7 |
| 12 | XAG | 1h | SHORT | OSC · Stoch · dinamik · filtresiz | SABIT_1.5R | 2.30 | +0.400R (50) | +0.030R (22) | %45.5 |
| 13 | SPX | 4h | SHORT | MA · EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | 2.30 | +0.401R (46) | +0.123R (26) | %57.7 |
| 14 | SPX | 1h | iki yön | OSC · RSI · dinamik · volatilite şoku+onay mumu | TP1>BE_3R | 2.01 | +0.273R (152) | +0.016R (62) | %19.4 |
| 15 | XAU | 1h | iki yön | MA · zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | 1.98 | +0.589R (115) | -0.207R (47) | %21.3 |

### Portföy performansı — işlem başına sabit risk, günlük zarar limiti %3

| Risk/işlem | Dönem | İşlem/gün | İsabet | Beklenti | Toplam getiri | Yıllık | Maks. düşüş | En uzun düşüş (gün) | Pozitif gün | Pozitif ay |
|---|---|---|---|---|---|---|---|---|---|---|
| %0.25 | IS | 2.05 | %31.3 | +0.248R | %52778.8 | %57.0 | %26.1 | 873 | %40.1 | %55.1 |
| %0.25 | **OOS** | 1.88 | %28.5 | +0.062R | %90.6 | %10.1 | %41.0 | 621 | %36.3 | %26.2 |
| %0.5 | IS | 2.01 | %31.6 | +0.264R | %31826183.7 | %148.8 | %45.4 | 873 | %40.0 | %55.1 |
| %0.5 | **OOS** | 1.85 | %28.6 | +0.070R | %269.0 | %21.5 | %64.2 | 621 | %36.2 | %28.7 |
| %1 | IS | 1.75 | %32.6 | +0.302R | %3101615278793.5 | %468.5 | %78.4 | 873 | %37.8 | %55.7 |
| %1 | **OOS** | 1.60 | %29.9 | +0.119R | %3966.4 | %73.9 | %78.1 | 623 | %34.2 | %25.0 |

### Monte Carlo — OOS günlük getirilerinden 2.000 adet 1 yıllık yol (5 günlük blok bootstrap)

| Risk/işlem | Medyan yıllık getiri | En kötü %5 senaryo | Yılı zararla kapama | Kasa %20 düşer | %30 düşer | %50 düşer | Medyan maks. düşüş | Medyan en uzun düşüş (gün) |
|---|---|---|---|---|---|---|---|---|
| %0.25 | %9.8 | %-22.9 | %34.2 | %34.0 | %5.5 | %0.0 | %16.8 | 196 |
| %0.5 | %21.1 | %-38.5 | %33.4 | %87.1 | %49.9 | %5.5 | %30.0 | 197 |
| %1 | %70.8 | %-48.7 | %24.6 | %99.5 | %87.7 | %32.0 | %43.6 | 178 |

> Okuma: OOS beklentisi eksiyse risk seviyesi ne olursa olsun kasa uzun vadede erir — sabit oranlı risk yalnızca erimeyi yavaşlatır. OOS pozitifse, kasanın %30 düşme olasılığı kabul edilebilir düzeyde olan en yüksek risk seviyesi seçilir.


## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 1h | 4h |
|---|---|---|
| **XAU** | ⚠ +0.029R (25) | ❌ -0.340R (26) |
| **XAG** | ⚠ +0.030R (22) | — |
| **BTC** | ⚠ +0.001R (130) | ⚠ +0.030R (132) |
| **ETH** | ❌ -0.007R (211) | ⚠ +0.329R (61) |
| **NQ** | ⚠ +0.842R (96) | ⚠ +0.685R (16) |
| **SPX** | ⚠ +0.016R (62) | ⚠ +0.123R (26) |

## XAU

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 3,961 | 2013-04-01 → 2020-04-20 | 2020-04-20 → 2025-11-30 | 0.048R | çalıştı |
| 4h | 1,060 | 2013-04-01 → 2020-04-20 | 2020-04-20 → 2025-11-30 | 0.023R | yetersiz aday |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 1h | iki yön | RSI(2) 10/90 · EMA200 trend | SABIT_3R | +0.510R (107) | +0.287R (42) | +0.176R | %33.3 | 1.41 | 0.165 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | TP1>BE_3R | +0.214R (71) | +0.182R (93) | -0.019R | %22.6 | 1.38 | 0.131 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 1h | iki yön | yatayda dönüş · Stoch · filtresiz | SABIT_2R | +0.046R (52) | +0.060R (19) | +0.025R | %36.8 | 1.09 | 0.430 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 1h | iki yön | Donchian 55 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.541R (41) | +0.029R (25) | -0.004R | %52.0 | 1.06 | 0.448 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | SHORT | Stoch · sabit · filtresiz | TP1>BE_3R | +0.208R (90) | -0.074R (43) | +0.008R | %16.3 | 0.87 | 0.633 | ❌ OOS'ta tutmadı |
| **MA** | 1h | iki yön | zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | +0.589R (115) | -0.207R (47) | -0.336R | %21.3 | 0.72 | 0.782 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.054R | %70.0 | %27.5 | +0.031R | %27.1 | 45 |
| GENIS_%50@1R>BE_3R | +0.043R | %65.0 | %52.3 | +0.003R | %51.8 | 45 |
| IZ_SUREN_2.5ATR | +0.041R | %65.0 | %26.4 | -0.113R | %25.4 | 45 |
| SABIT_2R | +0.025R | %75.0 | %35.1 | +0.003R | %34.4 | 45 |
| %50@1R>BE_IZ | -0.014R | %45.0 | %49.7 | -0.064R | %48.7 | 45 |
| %50@1R>BE_2R | -0.014R | %50.0 | %49.6 | -0.037R | %48.7 | 45 |
| SABIT_1.5R | -0.016R | %45.0 | %40.5 | -0.049R | %39.2 | 45 |
| TP1>BE_2R | -0.018R | %35.0 | %26.1 | -0.021R | %26.0 | 45 |
| SABIT_1R | -0.020R | %40.0 | %50.7 | -0.053R | %48.7 | 45 |
| TP1>BE_3R | -0.023R | %45.0 | %17.3 | -0.048R | %16.5 | 45 |
| %50@1R>BE_3R | -0.041R | %45.0 | %49.1 | -0.050R | %48.7 | 45 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %75.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.079R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 55 · EMA200 trend · GENIS_%50@1R>BE_3R · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2013-04-12 → 2013-06-19 | 16 | %75.0 | +0.646R |
| 2013-06-26 → 2020-03-13 | 17 | %64.7 | +0.562R |
| 2020-03-16 → 2025-10-07 | 16 | %62.5 | +0.250R |
| 2025-10-13 → 2025-11-26 | 17 | %47.1 | -0.058R |

Maksimum düşüş: IS 2.04R · OOS 4.67R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 55 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.541R (41) | +0.029R (25) | %52.0 |
| 2 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | +0.510R (107) | +0.287R (42) | %33.3 |
| 3 | DONCH · Donchian 20 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.455R (49) | -0.145R (22) | %45.5 |
| 4 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.580R (107) | +0.383R (42) | %33.3 |
| 5 | DONCH · Donchian 20 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.365R (63) | +0.126R (32) | %53.1 |
| 6 | MA · zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | +0.589R (115) | -0.207R (47) | %21.3 |
| 7 | DONCH · Donchian 20 · filtresiz | GENIS_%50@1R>BE_3R | +0.224R (95) | +0.150R (39) | %53.8 |
| 8 | DONCH · Donchian 55 · EMA200 trend | IZ_SUREN_2.5ATR | +0.823R (41) | +0.041R (25) | %24.0 |
| 9 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_2R | +0.239R (107) | +0.168R (42) | %40.5 |
| 10 | DONCH · Donchian 55 · filtresiz | GENIS_%50@1R>BE_3R | +0.294R (52) | +0.149R (25) | %56.0 |
| 11 | RSI2 · RSI(2) 10/90 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.172R (107) | +0.303R (42) | %59.5 |
| 12 | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.267R (264) | +0.125R (117) | %30.8 |
| 13 | MA · zaman serisi momentumu 24 bar | %50@1R>BE_IZ | +0.336R (115) | -0.114R (47) | %46.8 |
| 14 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.420R (49) | -0.183R (22) | %13.6 |
| 15 | RSI2 · RSI(2) 10/90 · filtresiz | SABIT_3R | +0.150R (264) | +0.144R (117) | %30.8 |

## XAG

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 2,934 | 2018-03-01 → 2025-01-07 | 2025-01-07 → 2025-02-28 | 0.133R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 1h | iki yön | Donchian 20 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.189R (50) | +0.178R (18) | +0.232R | %55.6 | 1.37 | 0.279 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | LONG | RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | +0.014R (97) | +0.034R (34) | +0.112R | %55.9 | 1.07 | 0.430 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | SHORT | Stoch · dinamik · filtresiz | SABIT_1.5R | +0.400R (50) | +0.030R (22) | +0.136R | %45.5 | 1.05 | 0.456 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 1h | iki yön | anahtar (ikisi) · Stoch · filtresiz | SABIT_1.5R | +0.037R (44) | -0.151R (21) | -0.001R | %38.1 | 0.78 | 0.710 | ❌ OOS'ta tutmadı |
| **MA** | 1h | iki yön | EMA 9/21 kesişimi | SABIT_3R | +0.203R (85) | -0.231R (32) | -0.039R | %21.9 | 0.73 | 0.782 | ❌ OOS'ta tutmadı |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | +0.129R (66) | -0.591R (29) | -0.513R | %20.7 | 0.30 | 0.999 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_1R | -0.105R | %25.0 | %49.8 | -0.109R | %49.6 | 29 |
| GENIS_%50@1R>BE_3R | -0.133R | %20.0 | %47.5 | -0.128R | %48.2 | 29 |
| %50@1R>BE_2R | -0.151R | %20.0 | %49.8 | -0.145R | %49.6 | 29 |
| %50@1R>BE_3R | -0.173R | %15.0 | %50.5 | -0.166R | %49.6 | 29 |
| TP1>BE_2R | -0.179R | %20.0 | %20.9 | -0.181R | %21.2 | 29 |
| %50@1R>BE_IZ | -0.197R | %15.0 | %50.1 | -0.192R | %49.6 | 29 |
| SABIT_1.5R | -0.232R | %10.0 | %34.8 | -0.236R | %34.6 | 29 |
| TP1>BE_3R | -0.253R | %10.0 | %11.5 | -0.223R | %12.7 | 29 |
| SABIT_2R | -0.276R | %5.0 | %27.5 | -0.253R | %28.3 | 29 |
| SABIT_3R | -0.386R | %10.0 | %17.9 | -0.320R | %19.5 | 29 |
| IZ_SUREN_2.5ATR | -0.452R | %10.0 | %20.0 | -0.409R | %21.5 | 29 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.180R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · Stoch · dinamik · filtresiz · SABIT_1.5R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2018-03-13 → 2018-04-16 | 18 | %61.1 | +0.354R |
| 2018-04-17 → 2024-12-03 | 18 | %50.0 | +0.092R |
| 2024-12-04 → 2025-01-21 | 18 | %66.7 | +0.559R |
| 2025-01-22 → 2025-02-20 | 18 | %50.0 | +0.145R |

Maksimum düşüş: IS 4.71R · OOS 6.67R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · Stoch · dinamik · filtresiz | SABIT_1.5R | +0.121R (94) | -0.193R (44) | %36.4 |
| 2 | OSC · Stoch · sabit · onay mumu | GENIS_%50@1R>BE_3R | +0.080R (97) | -0.306R (40) | %40.0 |
| 3 | DONCH · Donchian 20 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.189R (50) | +0.178R (18) | %55.6 |
| 4 | DONCH · Donchian 20 · filtresiz | GENIS_%50@1R>BE_3R | +0.103R (81) | -0.070R (30) | %46.7 |
| 5 | OSC · Stoch+WaveTrend · sabit · filtresiz | SABIT_1R | +0.128R (42) | -0.242R (21) | %42.9 |
| 6 | OSC · Stoch · dinamik · filtresiz | GENIS_%50@1R>BE_3R | +0.054R (94) | -0.049R (44) | %56.8 |
| 7 | META · gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.001R (161) | -0.213R (129) | %43.4 |
| 8 | OSC · Stoch+WaveTrend · dinamik · filtresiz | GENIS_%50@1R>BE_3R | +0.177R (42) | -0.282R (20) | %45.0 |
| 9 | OSC · Stoch · sabit · onay mumu | SABIT_1.5R | +0.053R (97) | -0.415R (40) | %27.5 |
| 10 | MA · EMA 9/21 kesişimi | SABIT_3R | +0.203R (85) | -0.231R (32) | %21.9 |
| 11 | OSC · Stoch · sabit · filtresiz | GENIS_%50@1R>BE_3R | -0.003R (124) | -0.293R (49) | %42.9 |
| 12 | RSI2 · RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | -0.038R (184) | -0.084R (70) | %50.0 |
| 13 | DONCH · Donchian 20 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.086R (61) | -0.008R (24) | %50.0 |
| 14 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.279R (161) | -0.495R (129) | %20.9 |
| 15 | RSI2 · RSI(2) 10/90 · filtresiz | SABIT_1R | -0.077R (184) | -0.019R (70) | %54.3 |

## BTC

Veri: 5m tabanı `None` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 79,871 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-02 | 0.102R | çalıştı |
| 4h | 19,986 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-02 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.293R (498) | +0.263R (219) | +0.265R | %28.3 | 1.38 | 0.068 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.271R (1618) | +0.053R (965) | +0.061R | %25.8 | 1.07 | 0.240 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | +0.031R | %25.0 | 1.04 | 0.439 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.399R (571) | -0.105R (256) | -0.099R | %25.4 | 0.86 | 0.807 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | LONG | yatayda dönüş · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.551R (130) | -0.201R (62) | -0.277R | %22.6 | 0.74 | 0.801 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch · sabit · onay mumu | IZ_SUREN_2.5ATR | +0.415R (281) | -0.304R (150) | -0.380R | %20.7 | 0.62 | 0.981 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.497R (183) | -0.328R (64) | -0.327R | %18.8 | 0.59 | 0.952 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.081R | %25.0 | %47.1 | -0.079R | %45.6 | 205 |
| SABIT_1R | -0.089R | %25.0 | %48.7 | -0.171R | %44.4 | 205 |
| %50@1R>BE_IZ | -0.102R | %15.0 | %48.0 | -0.134R | %44.4 | 205 |
| SABIT_1.5R | -0.124R | %15.0 | %37.6 | -0.184R | %35.0 | 205 |
| %50@1R>BE_2R | -0.125R | %10.0 | %47.9 | -0.141R | %44.4 | 205 |
| IZ_SUREN_2.5ATR | -0.126R | %25.0 | %22.9 | -0.135R | %25.3 | 205 |
| %50@1R>BE_3R | -0.126R | %5.0 | %47.9 | -0.129R | %44.4 | 205 |
| TP1>BE_3R | -0.140R | %10.0 | %14.6 | -0.087R | %18.0 | 205 |
| TP1>BE_2R | -0.142R | %15.0 | %22.2 | -0.112R | %25.2 | 205 |
| SABIT_3R | -0.185R | %10.0 | %22.3 | -0.106R | %24.3 | 205 |
| SABIT_2R | -0.188R | %15.0 | %29.3 | -0.158R | %30.0 | 205 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %15.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.135R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · sıkışma sonrası · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-09-13 → 2019-11-04 | 109 | %43.1 | +0.916R |
| 2019-11-08 → 2022-02-15 | 110 | %27.3 | +0.195R |
| 2022-02-28 → 2024-06-30 | 109 | %33.9 | +0.799R |
| 2024-07-23 → 2026-09-08 | 110 | %24.5 | -0.083R |

Maksimum düşüş: IS 21.66R · OOS 36.38R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | %25.0 |
| 2 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.569R (370) | -0.028R (158) | %24.1 |
| 3 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.584R (266) | -0.152R (125) | %21.6 |
| 4 | DONCH · Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.645R (188) | -0.323R (96) | %16.7 |
| 5 | DONCH · Donchian 20 · filtresiz | IZ_SUREN_2.5ATR | +0.434R (495) | -0.038R (210) | %25.7 |
| 6 | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.597R (162) | -0.335R (74) | %14.9 |
| 7 | MA · EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.399R (571) | -0.105R (256) | %25.4 |
| 8 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.341R (306) | -0.049R (132) | %15.9 |
| 9 | DONCH · Donchian 55 · hacim şoku | %50@1R>BE_IZ | +0.378R (188) | -0.166R (96) | %45.8 |
| 10 | DONCH · Donchian 55 · hacim şoku | TP1>BE_3R | +0.393R (188) | -0.198R (96) | %13.5 |
| 11 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.342R (266) | -0.145R (125) | %14.4 |
| 12 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +0.407R (369) | -0.065R (160) | %26.9 |
| 13 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.271R (1618) | +0.053R (965) | %25.8 |
| 14 | DONCH · Donchian 55 · sıkışma sonrası | %50@1R>BE_IZ | +0.379R (162) | -0.113R (74) | %48.6 |
| 15 | DONCH · Donchian 55 · filtresiz | IZ_SUREN_2.5ATR | +0.458R (287) | -0.333R (127) | %16.5 |

## ETH

Veri: 5m tabanı `None` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 79,876 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-02 | 0.077R | çalıştı |
| 4h | 19,986 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-02 | 0.037R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 4h | LONG | Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | +0.329R (61) | +0.311R | %34.4 | 1.48 | 0.090 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.311R (718) | +0.306R (410) | +0.180R | %30.5 | 1.45 | 0.010 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.291R (531) | +0.141R (243) | +0.073R | %29.6 | 1.21 | 0.178 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.234R (582) | -0.097R (294) | -0.171R | %23.1 | 0.87 | 0.789 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_IZ | +0.485R (64) | -0.207R (25) | -0.201R | %40.0 | 0.67 | 0.808 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | -0.281R | %23.5 | 0.58 | 0.854 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | iki yön | yatayda dönüş · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.769R (94) | -0.417R (38) | -0.482R | %18.4 | 0.43 | 0.986 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.252R | %80.0 | %30.3 | -0.021R | %25.4 | 198 |
| SABIT_3R | +0.143R | %70.0 | %30.5 | -0.095R | %24.5 | 198 |
| TP1>BE_3R | +0.041R | %50.0 | %19.1 | -0.074R | %16.7 | 198 |
| GENIS_%50@1R>BE_3R | +0.041R | %70.0 | %51.2 | -0.031R | %47.8 | 198 |
| %50@1R>BE_IZ | +0.031R | %55.0 | %50.1 | -0.061R | %47.1 | 198 |
| SABIT_1.5R | +0.023R | %45.0 | %42.7 | -0.119R | %36.9 | 198 |
| SABIT_2R | +0.021R | %45.0 | %35.5 | -0.087R | %31.8 | 198 |
| %50@1R>BE_3R | +0.007R | %40.0 | %51.0 | -0.086R | %47.1 | 198 |
| TP1>BE_2R | -0.038R | %35.0 | %25.4 | -0.080R | %24.5 | 198 |
| %50@1R>BE_2R | -0.039R | %35.0 | %49.8 | -0.089R | %47.1 | 198 |
| SABIT_1R | -0.042R | %35.0 | %50.1 | -0.099R | %47.1 | 198 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %60.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.065R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · hacim şoku · SABIT_3R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-10-13 → 2020-04-06 | 50 | %48.0 | +0.883R |
| 2020-04-16 → 2022-07-14 | 51 | %45.1 | +0.766R |
| 2022-07-28 → 2024-07-19 | 50 | %34.0 | +0.302R |
| 2024-08-23 → 2026-09-21 | 51 | %31.4 | +0.208R |

Maksimum düşüş: IS 6.20R · OOS 11.52R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 55 · sıkışma sonrası | TP1>BE_3R | +0.514R (139) | +0.338R (70) | %27.1 |
| 2 | REJIM · yatayda dönüş · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.769R (94) | -0.417R (38) | %18.4 |
| 3 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.687R (123) | -0.381R (49) | %18.4 |
| 4 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.490R (284) | +0.677R (118) | %36.4 |
| 5 | DONCH · Donchian 55 · sıkışma sonrası | SABIT_3R | +0.514R (139) | +0.495R (70) | %38.6 |
| 6 | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.411R (284) | +0.345R (118) | %34.7 |
| 7 | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | +0.375R (291) | +0.118R (131) | %22.9 |
| 8 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.358R (284) | +0.218R (118) | %22.9 |
| 9 | OSC · Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | %23.5 |
| 10 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_IZ | +0.485R (64) | -0.207R (25) | %40.0 |
| 11 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_3R | +0.652R (64) | -0.250R (25) | %20.0 |
| 12 | DONCH · Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | +0.360R (139) | +0.189R (70) | %58.6 |
| 13 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_3R | +0.431R (64) | -0.210R (25) | %40.0 |
| 14 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_3R | +0.286R (284) | +0.163R (118) | %57.6 |
| 15 | DONCH · Donchian 20 · hacim şoku | TP1>BE_2R | +0.298R (284) | +0.227R (118) | %34.7 |

## NQ

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 23,645 | 2012-01-19 → 2020-01-20 | 2020-01-20 → 2026-07-31 | 0.075R | çalıştı |
| 4h | 6,822 | 2012-01-19 → 2019-12-19 | 2019-12-19 → 2026-07-31 | 0.038R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **OSC** | 1h | LONG | Stoch · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.801R (96) | +1.233R (44) | +1.135R | %36.4 | 3.06 | 0.027 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 1h | LONG | anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.793R (206) | +0.842R (96) | +0.743R | %36.5 | 2.52 | 0.006 | ✅ Kanıtlı |
| **DONCH** | 1h | LONG | Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.621R (120) | +0.568R (50) | +0.469R | %38.0 | 1.93 | 0.079 | ⚠️ Pozitif, anlamsız |
| **MA** | 1h | LONG | zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | +0.465R (355) | +0.435R (164) | +0.337R | %32.3 | 1.70 | 0.025 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.322R (1152) | +0.236R (803) | +0.138R | %32.4 | 1.37 | 0.002 | ✅ Kanıtlı |
| **RSI2** | 1h | LONG | RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.278R (726) | +0.171R (309) | +0.073R | %31.4 | 1.26 | 0.091 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_1.5R | +0.493R (47) | -0.023R (12) | +0.036R | %41.7 | 0.96 | 0.525 | ⏳ OOS yetersiz |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.512R | %94.7 | %31.0 | +0.115R | %23.4 | 199 |
| %50@1R>BE_IZ | +0.356R | %88.9 | %54.2 | +0.081R | %44.1 | 199 |
| SABIT_2R | +0.320R | %89.5 | %45.8 | -0.081R | %32.5 | 199 |
| SABIT_1.5R | +0.183R | %88.9 | %49.4 | -0.084R | %38.7 | 199 |
| TP1>BE_2R | +0.180R | %83.3 | %33.9 | -0.100R | %25.6 | 199 |
| SABIT_3R | +0.135R | %84.2 | %30.1 | -0.078R | %24.7 | 199 |
| %50@1R>BE_2R | +0.114R | %77.8 | %54.9 | -0.135R | %44.1 | 199 |
| TP1>BE_3R | +0.106R | %75.0 | %21.0 | -0.148R | %15.6 | 199 |
| GENIS_%50@1R>BE_3R | +0.105R | %89.5 | %53.9 | -0.087R | %46.4 | 199 |
| SABIT_1R | +0.059R | %76.5 | %55.5 | -0.170R | %44.1 | 199 |
| %50@1R>BE_3R | +0.045R | %66.7 | %52.8 | -0.159R | %44.1 | 199 |

**Sağlamlık (1h):** IS'te en iyi 17 ayarın %100.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.362R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — REJIM · anahtar (ikisi) · Stoch · filtresiz · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-02-23 → 2013-12-17 | 75 | %33.3 | +0.987R |
| 2013-12-18 → 2015-04-08 | 76 | %38.2 | +0.431R |
| 2015-04-13 → 2020-05-14 | 75 | %38.7 | +0.890R |
| 2020-05-15 → 2026-07-22 | 76 | %35.5 | +0.929R |

Maksimum düşüş: IS 15.67R · OOS 4.68R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | TP1>BE_2R | +0.431R (105) | +0.220R (47) | %34.0 |
| 2 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.687R (105) | +1.089R (47) | %34.0 |
| 3 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | TP1>BE_3R | +0.488R (105) | +0.369R (47) | %27.7 |
| 4 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | %50@1R>BE_IZ | +0.430R (105) | +0.627R (47) | %59.6 |
| 5 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_1.5R | +0.493R (47) | -0.023R (12) | %41.7 |
| 6 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | SABIT_2R | +0.429R (105) | +0.220R (47) | %42.6 |
| 7 | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.458R (333) | +0.521R (162) | %30.9 |
| 8 | OSC · Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend | TP1>BE_3R | +0.533R (68) | +0.066R (32) | %18.8 |
| 9 | OSC · Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend | %50@1R>BE_3R | +0.408R (68) | +0.066R (32) | %56.2 |
| 10 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | %50@1R>BE_3R | +0.355R (105) | +0.252R (47) | %59.6 |
| 11 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_2R | +0.557R (47) | -0.065R (12) | %33.3 |
| 12 | OSC · Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend | TP1>BE_2R | +0.430R (68) | +0.066R (32) | %28.1 |
| 13 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | %50@1R>BE_2R | +0.326R (105) | +0.177R (47) | %59.6 |
| 14 | OSC · Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend | %50@1R>BE_IZ | +0.427R (68) | +0.660R (32) | %56.2 |
| 15 | OSC · Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend | %50@1R>BE_2R | +0.357R (68) | +0.066R (32) | %56.2 |

## SPX

Veri: 5m tabanı `None` · 1h tabanı `yfinance:ES=F (yedek, kısa geçmiş)`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 13,677 | 2024-05-12 → 2026-01-15 | 2026-01-15 → 2026-10-02 | 0.097R | çalıştı |
| 4h | 3,706 | 2024-05-12 → 2026-01-13 | 2026-01-14 → 2026-10-02 | 0.047R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **REJIM** | 1h | LONG | anahtar (ikisi) · RSI · volatilite şoku | TP1>BE_3R | +0.516R (45) | +0.158R (17) | +0.216R | %23.5 | 1.30 | 0.345 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | SHORT | EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | +0.401R (46) | +0.123R (26) | +0.090R | %57.7 | 1.28 | 0.292 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | +0.206R (122) | +0.034R (47) | +0.130R | %51.1 | 1.07 | 0.421 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | iki yön | RSI · dinamik · volatilite şoku+onay mumu | TP1>BE_3R | +0.273R (152) | +0.016R (62) | +0.102R | %19.4 | 1.03 | 0.466 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | SABIT_1R | +0.074R (102) | -0.178R (79) | -0.113R | %43.0 | 0.70 | 0.944 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_3R | +0.303R (58) | -0.256R (19) | -0.156R | %21.1 | 0.70 | 0.748 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | SHORT | Donchian 20 · filtresiz | SABIT_2R | +0.455R (40) | -0.392R (23) | -0.408R | %21.7 | 0.52 | 0.932 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_1.5R | +0.012R | %47.4 | %42.2 | -0.035R | %40.4 | 47 |
| TP1>BE_2R | -0.037R | %40.0 | %25.9 | +0.002R | %27.8 | 47 |
| %50@1R>BE_3R | -0.043R | %31.6 | %50.8 | -0.048R | %49.0 | 47 |
| %50@1R>BE_2R | -0.047R | %21.1 | %49.2 | -0.031R | %49.0 | 47 |
| SABIT_1R | -0.049R | %26.3 | %49.7 | -0.064R | %49.0 | 47 |
| %50@1R>BE_IZ | -0.054R | %31.6 | %50.2 | -0.046R | %49.0 | 47 |
| SABIT_2R | -0.060R | %45.0 | %32.8 | -0.001R | %34.8 | 47 |
| GENIS_%50@1R>BE_3R | -0.074R | %27.8 | %51.7 | -0.042R | %50.0 | 47 |
| TP1>BE_3R | -0.077R | %36.8 | %15.7 | -0.031R | %17.5 | 47 |
| SABIT_3R | -0.080R | %45.0 | %24.3 | -0.127R | %23.0 | 47 |
| IZ_SUREN_2.5ATR | -0.124R | %35.0 | %24.8 | -0.157R | %27.4 | 47 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %30.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.130R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · EMA 9/21 kesişimi · GENIS_%50@1R>BE_3R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2024-05-23 → 2025-01-27 | 18 | %66.7 | +0.546R |
| 2025-02-02 → 2025-09-02 | 18 | %61.1 | +0.219R |
| 2025-09-24 → 2026-02-23 | 18 | %61.1 | +0.052R |
| 2026-02-27 → 2026-09-08 | 18 | %66.7 | +0.385R |

Maksimum düşüş: IS 4.24R · OOS 3.75R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | MA · EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | +0.206R (92) | -0.163R (52) | %44.2 |
| 2 | DONCH · Donchian 20 · filtresiz | GENIS_%50@1R>BE_3R | +0.208R (91) | -0.253R (45) | %46.7 |
| 3 | DONCH · Donchian 20 · hacim şoku | GENIS_%50@1R>BE_3R | +0.304R (49) | -0.130R (25) | %48.0 |
| 4 | MA · EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.442R (92) | -0.431R (52) | %19.2 |
| 5 | RSI2 · RSI(2) 10/90 · filtresiz | GENIS_%50@1R>BE_3R | +0.065R (273) | +0.044R (101) | %52.5 |
| 6 | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.204R (273) | +0.115R (101) | %27.7 |
| 7 | MA · EMA 9/21 kesişimi | %50@1R>BE_3R | +0.160R (92) | -0.235R (52) | %40.4 |
| 8 | MA · EMA 9/21 kesişimi | %50@1R>BE_IZ | +0.175R (92) | -0.274R (52) | %40.4 |
| 9 | MA · EMA 9/21 kesişimi | %50@1R>BE_2R | +0.132R (92) | -0.244R (52) | %40.4 |
| 10 | RSI2 · RSI(2) 10/90 · filtresiz | TP1>BE_2R | +0.064R (273) | -0.056R (101) | %25.7 |
| 11 | DONCH · Donchian 55 · filtresiz | SABIT_1R | +0.162R (58) | +0.124R (24) | %58.3 |
| 12 | RSI2 · RSI(2) 10/90 · filtresiz | SABIT_2R | +0.080R (273) | +0.053R (101) | %36.6 |
| 13 | MA · EMA 9/21 kesişimi | SABIT_1R | +0.105R (92) | -0.235R (52) | %40.4 |
| 14 | DONCH · Donchian 20 · filtresiz | SABIT_2R | +0.207R (91) | -0.244R (45) | %26.7 |
| 15 | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_3R | +0.239R (49) | -0.146R (25) | %48.0 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
