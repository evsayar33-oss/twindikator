# ATVS Lab v2 Raporu — 2026-10-02 19:51 UTC

**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).
**Seçim** ilk %70 veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %30 (OOS) verisine göre** verilir. ✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · ⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.
Giriş: sinyalden sonraki bar açılışı · zaman bariyeri 48 bar · aynı barda hedef+stop = stop. TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.

**Odak:** zaman dilimleri 1h, 4h · aileler MA, DONCH, SQZ, RSI2, REJIM, OSC, META. **Alfa** = aynı çıkışla aynı dönemde rastgele girişe göre fark (piyasanın kendi yükselişini ayıklar). 🚩 = fiziksel olarak inandırıcı olmayan sonuç (veri hatası belirtisi) — seçimden çıkarılır.

## Veri doğrulama (yfinance günlük kapanışla ay ay karşılaştırma)

| Varlık | Taban | Dönem | Referans | Durum | Ay | **Eksik ay** | Düzeltilen ay | Atılan ay | Atılan sıçrama | Medyan sapma |
|---|---|---|---|---|---|---|---|---|---|---|
| XAU | 1h | 2011-10 → 2026-10 | GC=F | temiz | 181 | 1 | 0 | 0 | 0 | %0.1 |
| XAG | 1h | 2011-10 → 2026-10 | SI=F | düzeltildi | 181 | 1 | 0 | 0 | 1 | %0.2 |
| BTC | 1h | 2017-08 → 2026-10 | BTC-USD | düzeltildi | 111 | 1 | 0 | 0 | 9 | %0.1 |
| ETH | 1h | 2017-08 → 2026-10 | ETH-USD | düzeltildi | 108 | 1 | 0 | 0 | 4 | %0.1 |
| NQ | 1h | 2012-01 → 2026-10 | NQ=F | düzeltildi | 178 | 2 | 42 | 0 | 0 | %0.1 |
| SPX | 1h | 2012-01 → 2026-10 | ES=F | düzeltildi | 178 | 1 | 0 | 0 | 1 | %0.2 |

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1h | SHORT | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | **-0.009R** (30) | +0.111R | %53.3 | 0.98 | 0.6 | 8.61R | 0.520 | ❌ OOS'ta tutmadı |
| **XAG** | 4h | SHORT | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.295R (92) | **-0.519R** (35) | -0.453R | %28.6 | 0.30 | 0.6 | 19.09R | 1.000 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | **+0.030R** (132) | +0.031R | %25.0 | 1.04 | 4.0 | 36.38R | 0.439 | ⚠️ Pozitif, anlamsız |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | **+0.329R** (61) | +0.311R | %34.4 | 1.48 | 1.9 | 11.52R | 0.090 | ⚠️ Pozitif, anlamsız |
| **NQ** | 4h | LONG | MA · EMA 20/50 kesişimi | IZ_SUREN_2.5ATR | +0.906R (122) | **-0.139R** (65) | -0.231R | %21.5 | 0.81 | 1.4 | 19.06R | 0.734 | ❌ OOS'ta tutmadı |
| **SPX** | 4h | LONG | OSC · Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | +0.341R (120) | **-0.023R** (64) | +0.015R | %40.6 | 0.96 | 1.3 | 7.75R | 0.560 | ❌ OOS'ta tutmadı |

## Portföy (IS'te seçilen stratejilerin birlikte çalışması)

Seçim kuralı (yalnızca IS): IS beklentisi > 0, t ≥ 1.5, varlık başına en fazla 3, aynı varlıkta aynı aile bir kez, toplam en fazla 15. OOS penceresi: **2022-03-21 → bugün** (her strateji yalnızca kendi OOS döneminde işlem yapar; 1h/4h stratejileri kısa geçmiş nedeniyle sonradan katılır). Stratejiler arası ortalama günlük korelasyon: **0.02** (0'a yakın = iyi çeşitlendirme).

| # | Varlık | ZD | Yön | Giriş | Çıkış | IS t | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NQ | 1h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 5.01 | +0.161R (5284) | +0.089R (3551) | %27.9 |
| 2 | ETH | 4h | LONG | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_2R | 4.65 | +0.410R (141) | +0.100R (61) | %55.7 |
| 3 | BTC | 4h | iki yön | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 4.24 | +0.271R (1618) | +0.053R (965) | %25.8 |
| 4 | NQ | 4h | LONG | MA · EMA 20/50 kesişimi | TP1>BE_3R | 4.18 | +0.654R (122) | -0.184R (65) | %12.3 |
| 5 | BTC | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | 3.82 | +0.639R (306) | +0.030R (132) | %25.0 |
| 6 | ETH | 1h | LONG | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | 3.68 | +0.152R (3290) | +0.005R (920) | %26.7 |
| 7 | XAU | 1h | iki yön | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | 3.55 | +0.349R (713) | +0.070R (232) | %28.9 |
| 8 | NQ | 4h | LONG | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | 3.46 | +0.491R (71) | +0.248R (30) | %60.0 |
| 9 | SPX | 1h | LONG | OSC · Stoch · sabit · filtresiz | IZ_SUREN_2.5ATR | 3.46 | +0.227R (1332) | +0.051R (577) | %28.9 |
| 10 | ETH | 1h | iki yön | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 3.40 | +0.193R (2033) | -0.043R (888) | %26.5 |
| 11 | XAU | 1h | SHORT | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | 3.31 | +0.388R (57) | -0.009R (30) | %53.3 |
| 12 | XAU | 4h | iki yön | DONCH · Donchian 55 · filtresiz | TP1>BE_3R | 2.89 | +0.246R (346) | +0.242R (160) | %25.0 |
| 13 | SPX | 4h | LONG | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | 2.59 | +0.235R (684) | +0.281R (292) | %32.2 |
| 14 | BTC | 1h | LONG | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | 2.49 | +0.183R (1068) | -0.072R (476) | %27.7 |
| 15 | SPX | 1h | LONG | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | 2.43 | +0.402R (52) | -0.274R (22) | %36.4 |

### Yıllık kararlılık — strateji başına yıl yıl ortalama R (boş hücre = o yıl işlem veya veri yok)

| # | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  | +0.11 | +0.13 | +0.22 | +0.04 | +0.40 | +0.26 | +0.20 | +0.07 | +0.17 | +0.03 | +0.05 | +0.05 |
| 2 |  |  |  |  |  |  | -0.03 | +0.74 | +0.53 | +0.68 | +0.04 | +0.31 | +0.29 | +0.12 | +0.29 | -0.13 |
| 3 |  |  |  |  |  |  |  |  | +0.60 | +0.45 | +0.21 | +0.05 | +0.15 | +0.14 | -0.13 | +0.19 |
| 4 |  | +0.97 | +0.29 | +0.57 | +0.05 | +1.07 | +1.04 | +0.03 | +1.57 | +0.42 | +0.84 | +0.25 | +0.20 | -0.03 | -0.03 | -0.56 |
| 5 |  |  |  |  |  |  | +1.29 | +0.90 | +0.82 | +0.23 | -0.00 | +0.38 | +1.34 | +0.32 | -0.34 | +0.22 |
| 6 |  |  |  |  |  |  |  |  | +0.10 | +0.35 | +0.12 | -0.09 | +0.22 | -0.01 | +0.09 | -0.08 |
| 7 | +0.81 | +0.48 | +0.02 | +0.19 | +0.49 | +0.23 | +0.74 | +0.44 | -0.01 | +0.44 | +0.50 | +0.01 | +0.07 | -0.11 | -0.11 | +0.68 |
| 8 |  | +1.98 | +0.64 | +0.24 | +0.78 | -1.03 | +0.72 | +0.86 | +0.69 | +0.86 | +0.21 | +0.11 | +0.10 | +0.05 | +0.53 | -0.01 |
| 9 |  | +0.57 | +0.55 | +0.30 | +0.05 | -0.07 | +0.48 | +0.18 | +0.12 | +0.26 | +0.27 | +0.15 | -0.11 | +0.20 | -0.00 | +0.07 |
| 10 |  |  |  |  |  |  | +0.20 | +0.26 | +0.59 | +0.07 | +0.20 | +0.09 | -0.03 | -0.02 | -0.20 | +0.16 |
| 11 | -0.05 | +0.49 | +0.49 | +0.64 | +0.42 | +0.26 | +0.22 | +0.23 | +0.86 |  | +0.25 | -0.32 | -0.10 | +0.34 | -0.06 | +0.29 |
| 12 | +1.54 | +0.20 | +0.44 | -0.29 | -0.19 | +0.80 | +0.35 | -0.09 | -0.02 | +0.59 | +0.49 | +0.23 | +0.00 | -0.10 | +0.74 | +0.45 |
| 13 |  | +0.58 | +1.03 | -0.08 | -0.16 | +0.23 | +0.64 | +0.10 | +0.34 | +0.14 | +0.06 | +0.07 | +0.45 | +0.40 | -0.08 | +0.40 |
| 14 |  |  |  |  |  |  | +0.23 | +0.03 | +0.13 | +0.37 | +0.18 | +0.27 | +0.06 | +0.00 | -0.10 | -0.16 |
| 15 |  |  | +0.54 | +0.61 | +0.07 | -1.09 | +1.85 | -1.05 | +0.69 | -0.32 | +0.22 | -0.54 | -1.05 | +0.21 | -0.41 | -1.05 |

### Portföy performansı — işlem başına sabit risk, günlük zarar limiti %3

| Risk/işlem | Dönem | İşlem/gün | İsabet | Beklenti | Toplam getiri | Yıllık | Maks. düşüş | En uzun düşüş (gün) | Pozitif gün | Pozitif ay |
|---|---|---|---|---|---|---|---|---|---|---|
| %0.25 | IS | 3.81 | %30.2 | +0.208R | %536387.1 | %101.4 | %39.0 | 366 | %40.2 | %70.1 |
| %0.25 | **OOS** | 5.08 | %27.8 | +0.056R | %185.7 | %26.2 | %34.3 | 495 | %39.3 | %55.6 |
| %0.5 | IS | 3.60 | %30.8 | +0.231R | %3796205634.3 | %315.0 | %53.4 | 210 | %39.7 | %70.7 |
| %0.5 | **OOS** | 4.70 | %28.2 | +0.076R | %1095.5 | %73.3 | %64.7 | 450 | %38.0 | %59.3 |
| %1 | IS | 2.93 | %32.2 | +0.291R | %78706265546208800.0 | %1539.5 | %78.4 | 201 | %36.1 | %72.8 |
| %1 | **OOS** | 3.57 | %29.8 | +0.132R | %56200.8 | %307.0 | %74.6 | 450 | %32.3 | %59.3 |

### Monte Carlo — OOS günlük getirilerinden 2.000 adet 1 yıllık yol (5 günlük blok bootstrap)

| Risk/işlem | Medyan yıllık getiri | En kötü %5 senaryo | Yılı zararla kapama | Kasa %20 düşer | %30 düşer | %50 düşer | Medyan maks. düşüş | Medyan en uzun düşüş (gün) |
|---|---|---|---|---|---|---|---|---|
| %0.25 | %24.7 | %-32.7 | %29.4 | %81.2 | %40.0 | %3.0 | %27.3 | 174 |
| %0.5 | %66.9 | %-48.3 | %24.3 | %99.7 | %89.1 | %32.0 | %43.3 | 168 |
| %1 | %270.3 | %-48.3 | %13.8 | %100.0 | %99.6 | %65.0 | %55.2 | 142 |

> Okuma: OOS beklentisi eksiyse risk seviyesi ne olursa olsun kasa uzun vadede erir — sabit oranlı risk yalnızca erimeyi yavaşlatır. OOS pozitifse, kasanın %30 düşme olasılığı kabul edilebilir düzeyde olan en yüksek risk seviyesi seçilir.


## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 1h | 4h |
|---|---|---|
| **XAU** | ❌ -0.009R (30) | ⚠ +0.242R (160) |
| **XAG** | ⚠ +0.019R (443) | ❌ -0.519R (35) |
| **BTC** | ⚠ +0.001R (130) | ⚠ +0.030R (132) |
| **ETH** | ❌ -0.007R (211) | ⚠ +0.329R (61) |
| **NQ** | ⚠ +0.172R (68) | ❌ -0.139R (65) |
| **SPX** | ⚠ +0.051R (577) | ❌ -0.023R (64) |

## XAU

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,439 | 2011-10-03 → 2022-03-21 | 2022-03-21 → 2026-10-01 | 0.084R | çalıştı |
| 4h | 24,000 | 2011-10-03 → 2022-04-01 | 2022-04-01 → 2026-10-01 | 0.042R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **REJIM** | 4h | SHORT | anahtar (ikisi) · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.648R (71) | +0.390R (26) | +0.540R | %42.3 | 1.66 | 0.205 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 55 · filtresiz | TP1>BE_3R | +0.246R (346) | +0.242R (160) | +0.238R | %25.0 | 1.49 | 0.030 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | iki yön | RSI(2) 5/95 · EMA200 trend | IZ_SUREN_2.5ATR | +0.123R (1366) | +0.082R (581) | +0.089R | %26.2 | 1.11 | 0.207 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.097R (1985) | +0.077R (991) | +0.078R | %27.9 | 1.11 | 0.122 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.349R (713) | +0.070R (232) | +0.102R | %28.9 | 1.10 | 0.297 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | SHORT | RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | -0.009R (30) | +0.111R | %53.3 | 0.98 | 0.520 | ❌ OOS'ta tutmadı |
| **MA** | 4h | SHORT | EMA 50/200 kesişimi | SABIT_1R | +0.302R (55) | -0.378R (18) | -0.274R | %33.3 | 0.46 | 0.950 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.086R | %75.0 | %28.7 | +0.021R | %26.9 | 235 |
| SABIT_3R | +0.000R | %40.0 | %27.2 | -0.058R | %25.8 | 235 |
| GENIS_%50@1R>BE_3R | -0.001R | %40.0 | %50.4 | -0.039R | %50.2 | 235 |
| %50@1R>BE_IZ | -0.027R | %35.0 | %50.7 | -0.093R | %49.2 | 235 |
| SABIT_2R | -0.033R | %25.0 | %34.8 | -0.051R | %34.1 | 235 |
| TP1>BE_3R | -0.035R | %20.0 | %18.1 | -0.105R | %15.9 | 235 |
| %50@1R>BE_3R | -0.039R | %25.0 | %50.7 | -0.096R | %49.2 | 235 |
| TP1>BE_2R | -0.043R | %20.0 | %26.7 | -0.080R | %24.9 | 235 |
| %50@1R>BE_2R | -0.044R | %20.0 | %50.7 | -0.083R | %49.2 | 235 |
| SABIT_1R | -0.047R | %25.0 | %51.4 | -0.086R | %49.2 | 235 |
| SABIT_1.5R | -0.059R | %15.0 | %40.7 | -0.042R | %41.2 | 235 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %85.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.073R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu · SABIT_1R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2011-10-21 → 2014-10-08 | 21 | %76.2 | +0.441R |
| 2014-11-10 → 2018-08-03 | 22 | %72.7 | +0.368R |
| 2018-08-10 → 2023-02-17 | 22 | %54.5 | +0.009R |
| 2023-02-28 → 2026-07-01 | 22 | %63.6 | +0.194R |

Maksimum düşüş: IS 2.19R · OOS 8.61R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.349R (713) | +0.070R (232) | %28.9 |
| 2 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | IZ_SUREN_2.5ATR | +0.593R (163) | +0.415R (71) | %36.6 |
| 3 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_3R | +0.197R (713) | +0.037R (232) | %28.4 |
| 4 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | TP1>BE_3R | +0.157R (713) | +0.045R (232) | %19.8 |
| 5 | DONCH · Donchian 55 · EMA200 trend | IZ_SUREN_2.5ATR | +0.144R (1218) | +0.124R (547) | %29.3 |
| 6 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | %50@1R>BE_IZ | +0.101R (713) | +0.013R (232) | %53.0 |
| 7 | RSI2 · RSI(2) 5/95 · EMA200 trend | IZ_SUREN_2.5ATR | +0.123R (1366) | +0.082R (581) | %26.2 |
| 8 | DONCH · Donchian 55 · filtresiz | IZ_SUREN_2.5ATR | +0.120R (1317) | +0.095R (580) | %28.3 |
| 9 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | %50@1R>BE_3R | +0.080R (713) | +0.013R (232) | %53.0 |
| 10 | MA · EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.069R (2669) | +0.013R (1183) | %26.5 |
| 11 | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.152R (728) | +0.295R (323) | %30.7 |
| 12 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | TP1>BE_2R | +0.074R (713) | +0.019R (232) | %28.4 |
| 13 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_2R | +0.086R (713) | +0.032R (232) | %37.1 |
| 14 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.081R (1804) | -0.010R (769) | %27.3 |
| 15 | RSI2 · RSI(2) 5/95 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.030R (1366) | +0.007R (581) | %50.4 |

## XAG

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,224 | 2011-10-03 → 2022-03-24 | 2022-03-24 → 2026-10-01 | 0.108R | çalıştı |
| 4h | 23,998 | 2011-10-03 → 2022-04-01 | 2022-04-01 → 2026-10-01 | 0.055R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 1h | SHORT | RSI(2) 10/90 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.012R (1204) | +0.019R (443) | +0.079R | %52.8 | 1.04 | 0.365 | ⚠️ Pozitif, anlamsız |
| **MA** | 1h | SHORT | EMA 50/200 kesişimi | SABIT_1R | +0.064R (202) | -0.037R (80) | +0.049R | %52.5 | 0.93 | 0.629 | ❌ OOS'ta tutmadı |
| **META** | 4h | SHORT | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.010R (1199) | -0.058R (554) | +0.008R | %48.4 | 0.89 | 0.890 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | iki yön | Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.297R (433) | -0.112R (216) | -0.090R | %25.0 | 0.84 | 0.825 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | SHORT | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | +0.216R (108) | -0.512R (26) | -0.446R | %30.8 | 0.28 | 0.999 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | SHORT | anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.295R (92) | -0.519R (35) | -0.453R | %28.6 | 0.30 | 1.000 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.513R (58) | -1.051R (12) | -0.945R | %0.0 | 0.00 | 1.000 | ⏳ OOS yetersiz |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | -0.051R | %36.8 | %24.6 | -0.213R | %22.8 | 197 |
| SABIT_3R | -0.065R | %18.8 | %24.6 | -0.210R | %21.0 | 197 |
| GENIS_%50@1R>BE_3R | -0.090R | %21.1 | %46.5 | -0.120R | %46.7 | 197 |
| %50@1R>BE_IZ | -0.114R | %15.0 | %45.8 | -0.187R | %43.7 | 197 |
| %50@1R>BE_3R | -0.119R | %10.5 | %47.0 | -0.219R | %43.7 | 197 |
| SABIT_1R | -0.119R | %5.0 | %46.3 | -0.172R | %43.7 | 197 |
| TP1>BE_3R | -0.123R | %5.6 | %14.9 | -0.266R | %11.5 | 197 |
| %50@1R>BE_2R | -0.138R | %5.0 | %45.8 | -0.194R | %43.7 | 197 |
| SABIT_2R | -0.138R | %11.1 | %30.3 | -0.172R | %29.2 | 197 |
| TP1>BE_2R | -0.163R | %0.0 | %21.6 | -0.217R | %19.6 | 197 |
| SABIT_1.5R | -0.177R | %0.0 | %34.8 | -0.223R | %32.9 | 197 |

**Sağlamlık (4h):** IS'te en iyi 18 ayarın %38.9'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.047R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — REJIM · anahtar (ikisi) · Stoch · volatilite şoku · GENIS_%50@1R>BE_3R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-02-29 → 2014-12-26 | 31 | %67.7 | +0.513R |
| 2015-04-02 → 2018-05-22 | 32 | %62.5 | +0.349R |
| 2018-05-31 → 2022-06-03 | 32 | %59.4 | -0.001R |
| 2022-09-06 → 2026-08-20 | 32 | %25.0 | -0.564R |

Maksimum düşüş: IS 6.86R · OOS 19.09R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.297R (433) | -0.112R (216) | %25.0 |
| 2 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.513R (58) | -1.051R (12) | %0.0 |
| 3 | OSC · Stoch+WaveTrend · dinamik · EMA200 trend+onay mumu | SABIT_3R | +0.385R (95) | +0.554R (30) | %40.0 |
| 4 | DONCH · Donchian 55 · EMA200 trend | %50@1R>BE_IZ | +0.152R (310) | +0.004R (162) | %50.6 |
| 5 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend | SABIT_3R | +0.466R (65) | -0.801R (16) | %6.2 |
| 6 | DONCH · Donchian 55 · EMA200 trend | IZ_SUREN_2.5ATR | +0.278R (310) | +0.026R (162) | %28.4 |
| 7 | DONCH · Donchian 55 · EMA200 trend | TP1>BE_3R | +0.132R (310) | -0.021R (162) | %17.3 |
| 8 | DONCH · Donchian 20 · EMA200 trend | %50@1R>BE_IZ | +0.087R (433) | -0.064R (216) | %49.1 |
| 9 | DONCH · Donchian 55 · filtresiz | IZ_SUREN_2.5ATR | +0.223R (348) | +0.060R (177) | %28.2 |
| 10 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.789R (58) | -0.926R (12) | %8.3 |
| 11 | DONCH · Donchian 55 · EMA200 trend | %50@1R>BE_3R | +0.084R (310) | -0.027R (162) | %50.6 |
| 12 | DONCH · Donchian 55 · filtresiz | %50@1R>BE_IZ | +0.096R (348) | +0.004R (177) | %49.7 |
| 13 | DONCH · Donchian 20 · EMA200 trend | TP1>BE_3R | +0.092R (433) | -0.097R (216) | %15.3 |
| 14 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.236R (332) | +0.073R (165) | %24.8 |
| 15 | DONCH · Donchian 55 · EMA200 trend | TP1>BE_2R | +0.087R (310) | -0.071R (162) | %23.5 |

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
| 1h | 74,899 | 2012-01-19 → 2022-12-08 | 2022-12-08 → 2026-10-01 | 0.072R | çalıştı |
| 4h | 21,248 | 2012-01-19 → 2022-10-05 | 2022-10-05 → 2026-10-01 | 0.038R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 1h | LONG | Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.419R (284) | +0.338R (160) | +0.236R | %30.0 | 1.48 | 0.047 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_1.5R | +0.212R (100) | +0.149R (55) | +0.232R | %49.1 | 1.27 | 0.190 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | LONG | RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +0.203R (1525) | +0.108R (643) | +0.006R | %28.1 | 1.15 | 0.116 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.161R (5284) | +0.089R (3551) | -0.013R | %27.9 | 1.13 | 0.008 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +1.027R (71) | +0.034R (30) | -0.058R | %26.7 | 1.05 | 0.459 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 4h | LONG | yatayda dönüş · WaveTrend · volatilite şoku | IZ_SUREN_2.5ATR | +1.006R (56) | -0.105R (25) | -0.197R | %24.0 | 0.84 | 0.626 | ❌ OOS'ta tutmadı |
| **MA** | 4h | LONG | EMA 20/50 kesişimi | IZ_SUREN_2.5ATR | +0.906R (122) | -0.139R (65) | -0.231R | %21.5 | 0.81 | 0.734 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.154R | %70.0 | %29.9 | +0.050R | %27.2 | 177 |
| GENIS_%50@1R>BE_3R | +0.150R | %80.0 | %56.1 | +0.041R | %51.9 | 177 |
| IZ_SUREN_2.5ATR | +0.085R | %60.0 | %29.0 | +0.004R | %27.0 | 177 |
| SABIT_1.5R | +0.032R | %60.0 | %42.6 | -0.033R | %40.1 | 177 |
| TP1>BE_3R | +0.005R | %45.0 | %18.0 | +0.005R | %18.2 | 177 |
| %50@1R>BE_IZ | -0.014R | %30.0 | %50.3 | -0.040R | %49.5 | 177 |
| SABIT_2R | -0.024R | %30.0 | %33.6 | -0.026R | %33.6 | 177 |
| TP1>BE_2R | -0.035R | %15.0 | %25.8 | -0.017R | %26.1 | 177 |
| %50@1R>BE_3R | -0.046R | %15.0 | %48.7 | -0.019R | %49.5 | 177 |
| %50@1R>BE_2R | -0.058R | %5.0 | %48.2 | -0.031R | %49.5 | 177 |
| SABIT_1R | -0.083R | %0.0 | %47.5 | -0.044R | %49.5 | 177 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %60.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.091R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · EMA 20/50 kesişimi · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-01-25 → 2016-02-17 | 46 | %32.6 | +0.064R |
| 2016-05-24 → 2020-06-16 | 47 | %59.6 | +1.607R |
| 2020-06-30 → 2023-11-02 | 47 | %34.0 | +0.636R |
| 2023-12-08 → 2026-09-18 | 47 | %21.3 | -0.146R |

Maksimum düşüş: IS 7.79R · OOS 19.06R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +1.223R (46) | -0.122R (22) | %27.3 |
| 2 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.605R (46) | +0.410R (22) | %68.2 |
| 3 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.788R (46) | +0.240R (22) | %31.8 |
| 4 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +1.017R (48) | -0.166R (27) | %29.6 |
| 5 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +0.659R (108) | -0.149R (49) | %22.4 |
| 6 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend | GENIS_%50@1R>BE_3R | +0.537R (48) | +0.312R (27) | %66.7 |
| 7 | REJIM · anahtar (ikisi) · WaveTrend · volatilite şoku | GENIS_%50@1R>BE_3R | +0.429R (74) | +0.184R (39) | %59.0 |
| 8 | REJIM · yatayda dönüş · WaveTrend · volatilite şoku | GENIS_%50@1R>BE_3R | +0.427R (72) | +0.184R (39) | %59.0 |
| 9 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | +0.365R (108) | +0.183R (49) | %59.2 |
| 10 | OSC · Stoch · sabit · EMA200 trend | IZ_SUREN_2.5ATR | +0.413R (284) | +0.065R (138) | %23.9 |
| 11 | OSC · Stoch · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +0.619R (117) | -0.108R (60) | %26.7 |
| 12 | OSC · Stoch · sabit · EMA200 trend | TP1>BE_3R | +0.321R (284) | -0.090R (138) | %15.2 |
| 13 | OSC · Stoch · dinamik · EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +0.445R (226) | +0.248R (96) | %31.2 |
| 14 | MA · EMA 20/50 kesişimi | TP1>BE_3R | +0.324R (245) | -0.085R (129) | %15.5 |
| 15 | OSC · Stoch · sabit · EMA200 trend | SABIT_3R | +0.338R (284) | -0.017R (138) | %25.4 |

## SPX

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 75,598 | 2012-01-16 → 2022-11-29 | 2022-11-29 → 2026-10-02 | 0.094R | çalıştı |
| 4h | 21,503 | 2012-01-16 → 2022-09-20 | 2022-09-20 → 2026-10-02 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MA** | 4h | LONG | EMA 20/50 kesişimi | TP1>BE_3R | +0.350R (136) | +0.512R (62) | +0.473R | %33.9 | 2.07 | 0.012 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.235R (684) | +0.281R (292) | +0.240R | %32.2 | 1.43 | 0.023 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 4h | LONG | anahtar (ikisi) · RSI · filtresiz | SABIT_3R | +0.420R (106) | +0.198R (45) | +0.177R | %31.1 | 1.27 | 0.240 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | LONG | Donchian 20 · filtresiz | SABIT_3R | +0.229R (322) | +0.056R (140) | +0.035R | %27.9 | 1.07 | 0.355 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.062R (5255) | +0.031R (3530) | -0.050R | %26.7 | 1.04 | 0.209 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | +0.341R (120) | -0.023R (64) | +0.015R | %40.6 | 0.96 | 0.560 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | +0.402R (52) | -0.274R (22) | -0.247R | %36.4 | 0.59 | 0.868 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.101R | %75.0 | %28.8 | -0.077R | %24.3 | 184 |
| IZ_SUREN_2.5ATR | +0.033R | %65.0 | %27.8 | -0.101R | %26.2 | 184 |
| SABIT_2R | -0.010R | %45.0 | %34.6 | -0.067R | %32.7 | 184 |
| TP1>BE_3R | -0.015R | %40.0 | %18.8 | -0.054R | %18.5 | 184 |
| GENIS_%50@1R>BE_3R | -0.017R | %45.0 | %49.4 | -0.112R | %44.4 | 184 |
| %50@1R>BE_IZ | -0.032R | %50.0 | %48.4 | -0.121R | %44.0 | 184 |
| TP1>BE_2R | -0.038R | %40.0 | %26.6 | -0.091R | %25.8 | 184 |
| %50@1R>BE_2R | -0.047R | %30.0 | %49.0 | -0.129R | %44.0 | 184 |
| SABIT_1R | -0.069R | %15.0 | %48.9 | -0.167R | %44.0 | 184 |
| SABIT_1.5R | -0.077R | %35.0 | %38.8 | -0.143R | %36.2 | 184 |
| %50@1R>BE_3R | -0.077R | %25.0 | %47.0 | -0.110R | %44.0 | 184 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %65.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.031R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · Stoch+WaveTrend · sabit · filtresiz · SABIT_1.5R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-04-11 → 2016-01-20 | 46 | %56.5 | +0.374R |
| 2016-02-09 → 2020-03-23 | 46 | %52.2 | +0.272R |
| 2020-06-15 → 2023-09-27 | 46 | %47.8 | +0.163R |
| 2023-10-04 → 2026-09-11 | 46 | %43.5 | +0.048R |

Maksimum düşüş: IS 5.98R · OOS 7.75R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.229R (594) | +0.169R (267) | %31.5 |
| 2 | OSC · WaveTrend · dinamik · hacim şoku+onay mumu | IZ_SUREN_2.5ATR | +0.482R (117) | +0.044R (34) | %32.4 |
| 3 | RSI2 · RSI(2) 10/90 · EMA200 trend | TP1>BE_3R | +0.115R (594) | +0.179R (267) | %23.6 |
| 4 | RSI2 · RSI(2) 10/90 · EMA200 trend | %50@1R>BE_IZ | +0.082R (594) | +0.100R (267) | %52.1 |
| 5 | RSI2 · RSI(2) 10/90 · EMA200 trend | TP1>BE_2R | +0.078R (594) | +0.131R (267) | %33.0 |
| 6 | MA · zaman serisi momentumu 72 bar | TP1>BE_3R | +0.131R (377) | -0.124R (163) | %16.6 |
| 7 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | +0.116R (594) | +0.223R (267) | %31.8 |
| 8 | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.077R (1519) | +0.105R (639) | %28.3 |
| 9 | RSI2 · RSI(2) 10/90 · filtresiz | TP1>BE_2R | +0.029R (1519) | +0.034R (639) | %28.8 |
| 10 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +0.195R (377) | -0.123R (163) | %27.6 |
| 11 | MA · zaman serisi momentumu 72 bar | TP1>BE_2R | +0.094R (377) | -0.142R (163) | %23.9 |
| 12 | OSC · WaveTrend · dinamik · hacim şoku | IZ_SUREN_2.5ATR | +0.363R (144) | +0.023R (51) | %33.3 |
| 13 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_2R | +0.070R (594) | +0.142R (267) | %39.7 |
| 14 | DONCH · Donchian 20 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.057R (437) | -0.020R (191) | %50.3 |
| 15 | MA · EMA 9/21 kesişimi | SABIT_3R | +0.087R (651) | +0.187R (275) | %30.9 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
