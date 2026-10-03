# ATVS Lab v3 Raporu — 2026-10-03 07:30 UTC

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

## Finalistler (v3) — çakışmasız backtest + sağlamlık kapıları

Kapılar: **K1** OOS (n ≥ 30, beklenti > 0, alfa > 0, Benjamini–Hochberg yanlış keşif oranı ≤ 0.10 — 72 aday birlikte test edildi) · **K2** tüm dönem (n ≥ 80, beklenti > 0) · **K3** maliyet ×2 · **K4** komşu parametrelerin ≥ %70'i pozitif · **K5** yılların ≥ %60'i pozitif · **K6** veri şüphesi yok. Tümü çakışmasız: her strateji aynı anda tek pozisyon taşır. Not: tohum adaylar önceki raporun OOS sonuçlarından seçildi; onlar için OOS tam bağımsız değildir — asıl bağımsız sınav canlı kâğıt işlemdir.

| ID | Varlık | ZD | Yön | Giriş | Çıkış | Tüm dönem beklenti (n) | İsabet | PF | OOS beklenti (n) | OOS alfa | Maliyet×2 | Komşu + | Yıl + | İşlem/yıl | Maks. düşüş (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F1_XAU_4h_DONCH** | XAU | 4h | iki yön | DONCH · Donchian 20 · filtresiz + günlük trend | TP0.5>BE_3R | +0.317R (434) | %22.4 | 1.92 | +0.384R (144) | +0.365R | +0.274R | %100.0 | %86.7 | 29.4 | 12.5 |
| **F2_ETH_4h_DONCH** | ETH | 4h | iki yön | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.557R (379) | %36.7 | 1.96 | +0.762R (108) | +0.688R | +0.515R | %100.0 | %90.0 | 41.9 | 17.1 |

### Kurallar (TradingView / manuel uygulama için)

- **F1_XAU_4h_DONCH** — **XAU 4h · LONG ve SHORT** — Mum kapanışı önceki 20 mumun en yükseğinin üstündeyse LONG, en düşüğünün altındaysa SHORT (ilk kırılım). Ek filtre: günlük grafikte önceki gün kapanışı EMA50 üstünde (SHORT: altında). Giriş: sinyal mumunun kapanışından sonraki mumun açılışında. Stop: giriş ∓ 1.0 × ATR(14) (sinyal mumundaki ATR). +0.5R'de stop girişe çekilir. Hedef: +3.0R. 48 mum sonra hâlâ açıksa kapanış fiyatından kapatılır.
- **F2_ETH_4h_DONCH** — **ETH 4h · LONG ve SHORT** — Mum kapanışı önceki 20 mumun en yükseğinin üstündeyse LONG, en düşüğünün altındaysa SHORT (ilk kırılım). Filtre: son 2 mumda hacim, son 50 mumun medyanına göre ≥1.5σ (robust) yüksek. Giriş: sinyal mumunun kapanışından sonraki mumun açılışında. Stop: giriş ∓ 1.0 × ATR(14) (sinyal mumundaki ATR). İz süren stop: ulaşılan en uç fiyattan 2.5 × ATR (girişten itibaren). 48 mum sonra hâlâ açıksa kapanış fiyatından kapatılır.

### Finalistlerin yıllık sonuçları (yıl ortalama R · işlem)

| ID | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1_XAU_4h_DONCH | +1.46 (2) | +0.13 (29) | +0.54 (28) | -0.11 (30) | -0.21 (30) | +0.58 (29) | +0.27 (31) | +0.10 (25) | +0.10 (26) | +0.59 (27) | +0.55 (27) | +0.10 (36) | +0.05 (30) | +0.32 (30) | +1.05 (34) | +0.68 (20) |
| F2_ETH_4h_DONCH |  |  |  |  |  |  | -0.63 (10) | +0.51 (36) | +0.33 (42) | +1.07 (49) | +0.50 (36) | +0.28 (40) | +0.39 (57) | +0.73 (38) | +1.26 (39) | +0.13 (32) |

### Komşu parametre testleri

- **F1_XAU_4h_DONCH**: ATR 10: +0.296R · ATR 20: +0.326R · zaman bariyeri 36: +0.317R · zaman bariyeri 72: +0.317R · stop ×0.8: +0.269R · stop ×1.25: +0.294R · hedef −0.5R: +0.251R · hedef +0.5R: +0.332R · Donchian 15: +0.218R · Donchian 25: +0.313R
- **F2_ETH_4h_DONCH**: ATR 10: +0.513R · ATR 20: +0.604R · zaman bariyeri 36: +0.556R · zaman bariyeri 72: +0.545R · stop ×0.8: +0.682R · stop ×1.25: +0.473R · iz −0.5 ATR: +0.423R · iz +0.5 ATR: +0.673R · şok eşiği 1.25σ: +0.450R · şok eşiği 1.75σ: +0.573R · Donchian 15: +0.506R · Donchian 25: +0.607R

### Tüm adaylar ve kapı sonuçları

| Varlık | ZD | Giriş | Çıkış | Yön | Kaynak | K1 | K2 | K3 | K4 | K5 | K6 | Tüm dönem | OOS | Not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAU | 4h | DONCH · Donchian 20 · EMA200 trend | TP1>BE_3R | yalnız LONG | tohum | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | +0.312R (360) | +0.601R (125) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.175R (546) | +0.262R (170) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | iki yön | tohum | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | +0.557R (379) | +0.762R (108) | **FİNALİST** |
| NQ | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.094R (3430) | +0.078R (1356) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | iki yön | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.279R (928) | +0.041R (228) |  |
| NQ | 1h | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.217R (823) | +0.068R (267) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + önceden sıkışma | IZ_SUREN_2.5ATR | iki yön | IS t=3.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.256R (886) | -0.001R (224) |  |
| XAU | 1h | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | yalnız SHORT | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.259R (88) | +0.022R (31) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_4R | iki yön | IS t=2.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.213R (924) | +0.144R (228) |  |
| XAU | 1h | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend | SABIT_1R | yalnız SHORT | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.222R (92) | +0.022R (31) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + günlük trend | IZ_SUREN_2.5ATR | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.337R (487) | +0.221R (123) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + seans | IZ_SUREN_2.5ATR | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.303R (538) | +0.088R (136) |  |
| XAU | 4h | DONCH · Donchian 20 · filtresiz + günlük trend | TP0.5>BE_3R | iki yön | IS t=3.4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | +0.317R (434) | +0.384R (144) | **FİNALİST** |
| XAU | 4h | DONCH · Donchian 20 · EMA200 trend + günlük trend | TP0.5>BE_3R | iki yön | IS t=3.1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | +0.294R (451) | +0.376R (149) |  |
| XAU | 4h | DONCH · Donchian 55 · filtresiz | TP1>BE_3R_ERKEN | iki yön | IS t=3.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.245R (505) | +0.229R (159) |  |
| XAU | 4h | DONCH · Donchian 55 · filtresiz + günlük trend | TP0.5>BE_3R | iki yön | IS t=3.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.274R (347) | +0.293R (114) |  |
| XAU | 4h | DONCH · Donchian 55 · EMA200 trend + günlük trend | TP0.5>BE_3R | iki yön | IS t=3.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.273R (349) | +0.293R (114) |  |
| XAU | 4h | DONCH · Donchian 55 · filtresiz + güçlü mum | TP1>BE_3R_ERKEN | iki yön | IS t=2.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.262R (428) | +0.222R (134) |  |
| XAG | 4h | RSI2 · RSI(2) 5/95 · EMA200 trend + hacim | SABIT_1R | yalnız SHORT | IS t=2.9 | ✗ | ✗ | · | · | ✓ | ✓ | +0.384R (54) | +0.348R (10) |  |
| XAG | 4h | REJIM · anahtar (ikisi) · Stoch · volatilite şoku + güçlü mum | SABIT_4R | yalnız SHORT | IS t=2.6 | ✗ | ✗ | · | · | ✗ | ✓ | +0.511R (66) | -0.301R (24) |  |
| XAG | 4h | REJIM · yatayda dönüş · Stoch · volatilite şoku + önceden sıkışma | SABIT_4R | yalnız SHORT | IS t=2.5 | ✗ | ✗ | · | · | ✓ | ✓ | +0.572R (59) | -0.423R (16) |  |
| XAG | 4h | DONCH · Donchian 55 · EMA200 trend + önceden sıkışma | SABIT_4R | yalnız SHORT | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.537R (115) | +0.270R (33) |  |
| XAG | 4h | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | SABIT_4R | yalnız SHORT | IS t=2.5 | ✗ | ✓ | · | · | ✗ | ✓ | +0.297R (126) | -0.537R (35) |  |
| XAG | 4h | DONCH · Donchian 55 · filtresiz + önceden sıkışma | SABIT_4R | yalnız SHORT | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.535R (130) | +0.402R (36) |  |
| BTC | 1h | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | SABIT_4R | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.308R (392) | -0.103R (129) |  |
| BTC | 1h | RSI2 · RSI(2) 10/90 · EMA200 trend + ADX≥20 | SABIT_2.5R | iki yön | IS t=3.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.098R (1763) | -0.062R (542) |  |
| BTC | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku + güçlü mum | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=3.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.334R (136) | +0.179R (27) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.401R (427) | +0.028R (127) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası + önceden sıkışma | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.401R (427) | +0.028R (127) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | SABIT_4R | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.348R (241) | -0.162R (71) |  |
| BTC | 4h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.292R (953) | +0.121R (377) |  |
| BTC | 4h | DONCH · Donchian 20 · EMA200 trend + önceden sıkışma | %50@1R>BE_4R | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.244R (350) | -0.052R (105) |  |
| BTC | 4h | DONCH · Donchian 20 · EMA200 trend + hacim | GENIS_%50@1R>BE_3R | iki yön | IS t=4.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.281R (216) | -0.007R (68) |  |
| BTC | 4h | DONCH · Donchian 20 · hacim şoku + güçlü mum | TP0.5>BE_3R | iki yön | IS t=4.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.223R (339) | -0.103R (102) |  |
| BTC | 4h | DONCH · Donchian 20 · hacim şoku + önceden sıkışma | GENIS_%50@1R>BE_3R | iki yön | IS t=3.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.222R (245) | -0.056R (74) |  |
| BTC | 4h | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | iki yön | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.421R (412) | -0.026R (128) |  |
| ETH | 1h | DONCH · Donchian 55 · sıkışma sonrası + hacim | GENIS_%50@1R>BE_3R | iki yön | IS t=4.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.211R (547) | +0.082R (154) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku + önceden sıkışma | GENIS_%50@1R>BE_3R | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.194R (664) | +0.087R (199) |  |
| ETH | 1h | DONCH · Donchian 20 · sıkışma sonrası + hacim | SABIT_2R | iki yön | IS t=4.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.209R (817) | +0.097R (207) |  |
| ETH | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.094R (2208) | +0.026R (537) |  |
| ETH | 1h | DONCH · Donchian 55 · EMA200 trend + önceden sıkışma | GENIS_%50@1R>BE_3R | iki yön | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.145R (766) | -0.006R (232) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku | TP0.5>BE_3R | yalnız LONG | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.160R (630) | -0.036R (186) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku + önceden sıkışma | %50@1R>BE_3R | yalnız LONG | IS t=6.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.524R (126) | +0.022R (42) |  |
| ETH | 4h | DONCH · Donchian 20 · sıkışma sonrası + hacim | %50@1R>BE_3R | yalnız LONG | IS t=5.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.453R (99) | -0.206R (32) |  |
| ETH | 4h | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | TP1>BE_3R_ERKEN | iki yön | IS t=5.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.519R (221) | -0.003R (63) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku + güçlü mum | %50@1R>BE_4R | iki yön | IS t=5.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.368R (353) | +0.245R (107) |  |
| ETH | 4h | DONCH · Donchian 55 · sıkışma sonrası + hacim | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=5.0 | ✗ | ✗ | · | · | ✓ | ✓ | +0.549R (74) | +0.091R (28) |  |
| ETH | 4h | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | GENIS_%50@1R>BE_3R | iki yön | IS t=4.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.461R (132) | +0.123R (39) |  |
| NQ | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.075R (3787) | +0.075R (1422) |  |
| NQ | 1h | MA · zaman serisi momentumu 24 bar + seans | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.217R (1233) | -0.076R (380) |  |
| NQ | 1h | MA · zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.221R (1608) | +0.063R (492) |  |
| NQ | 1h | DONCH · Donchian 20 · EMA200 trend + seans | IZ_SUREN_2.5ATR | iki yön | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.205R (1702) | +0.065R (510) |  |
| NQ | 1h | MA · EMA 50/200 kesişimi | SABIT_3R | yalnız LONG | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.461R (212) | +0.186R (68) |  |
| NQ | 1h | DONCH · Donchian 20 · filtresiz + seans | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.232R (1218) | +0.098R (374) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi | TP0.5>BE_3R | yalnız LONG | IS t=4.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.413R (186) | -0.046R (63) |  |
| NQ | 4h | OSC · Stoch · sabit · EMA200 trend | TP0.5>BE_3R | iki yön | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.222R (422) | -0.032R (138) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi + seans | TP0.5>BE_3R | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.518R (107) | +0.043R (27) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi + günlük trend | TP0.5>BE_3R | yalnız LONG | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.361R (118) | -0.219R (43) |  |
| NQ | 4h | MA · zaman serisi momentumu 72 bar + seans | SABIT_2.5R | yalnız LONG | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.383R (158) | -0.106R (46) |  |
| NQ | 4h | DONCH · Donchian 55 · filtresiz + seans | SABIT_4R | yalnız LONG | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.436R (216) | +0.010R (61) |  |
| SPX | 1h | OSC · Stoch · sabit · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.161R (1852) | +0.063R (556) |  |
| SPX | 1h | OSC · Stoch · sabit · onay mumu | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.156R (1548) | +0.044R (464) |  |
| SPX | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + önceden sıkışma | TP1.5>BE_4R | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.339R (300) | +0.240R (105) |  |
| SPX | 1h | OSC · Stoch · sabit · EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.149R (758) | -0.081R (232) |  |
| SPX | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.4 | ✗ | ✗ | · | · | ✓ | ✓ | +0.201R (71) | -0.387R (20) |  |
| SPX | 1h | MA · zaman serisi momentumu 72 bar + hacim | TP1>BE_2R | yalnız LONG | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.172R (236) | -0.017R (79) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | IZ_SUREN_2.5ATR | iki yön | IS t=3.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.341R (520) | +0.226R (159) |  |
| SPX | 4h | OSC · Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | yalnız LONG | IS t=3.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.214R (184) | -0.023R (64) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · filtresiz + seans | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.307R (580) | +0.172R (174) |  |
| SPX | 4h | DONCH · Donchian 55 · sıkışma sonrası + seans | TP0.5>BE_3R | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.264R (201) | +0.051R (60) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.268R (799) | +0.284R (241) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.311R (501) | +0.326R (155) |  |

## Portföy (v3, olay tabanlı)

2 finalist · 2011-12-12 → 2026-09-23 · aynı anda en fazla 4 pozisyon · küme başına en fazla 1 (ABD endeksleri / metaller / kripto) · günlük zarar limiti %3 · stratejiler arası ortalama korelasyon 0.02

### ✅ Önerilen risk: işlem başına kasanın **%1**'i
Bu seviyede Monte Carlo'ya göre 1 yıllık maksimum düşüş %95 olasılıkla **%13.1**'i aşmıyor (hedef ≤ %15.0). Tarihsel: yıllık getiri **%25.0**, maksimum düşüş **%12.4**, en uzun düşüş 650 gün, pozitif ay oranı %53.4, ayda 4.6 işlem.

| Risk/işlem | Yıllık getiri | Toplam | Maks. düşüş | En uzun düşüş (gün) | Sharpe | Pozitif ay | İşlem/ay | Atlanan (açık/küme/gün) | MC %95 maks. düşüş | MC yılı zararla kapama | MC medyan yıllık | MC en kötü %5 | OOS yıllık | OOS maks. düşüş |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %0.25 | %6.0 | %136.1 | %3.2 | 650 | 1.45 | %53.4 | 4.6 | 0/0/0 | %3.4 | %6.6 | %5.6 | %-0.5 | %7.9 | %2.9 |
| %0.5 | %12.1 | %444.4 | %6.3 | 650 | 1.45 | %53.4 | 4.6 | 0/0/0 | %6.7 | %6.7 | %11.4 | %-1.1 | %16.2 | %5.7 |
| %0.75 | %18.5 | %1126.9 | %9.4 | 650 | 1.45 | %53.4 | 4.6 | 0/0/0 | %9.9 | %6.9 | %17.4 | %-1.8 | %24.9 | %8.4 |
| %1 ◀ | %25.0 | %2604.4 | %12.4 | 650 | 1.45 | %53.4 | 4.6 | 0/0/0 | %13.1 | %7.0 | %23.6 | %-2.5 | %34.0 | %11.1 |
| %1.5 | %38.5 | %12225.8 | %18.1 | 650 | 1.45 | %53.4 | 4.6 | 0/0/0 | %19.1 | %7.4 | %36.4 | %-4.2 | %53.3 | %16.5 |
| %2 | %52.6 | %51682.7 | %23.5 | 650 | 1.45 | %52.8 | 4.6 | 0/0/0 | %24.8 | %7.7 | %49.6 | %-6.1 | %74.2 | %21.7 |

### Yıllık getiriler (risk %1)

| 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %2.9 | %3.6 | %15.8 | %-3.6 | %-6.2 | %17.9 | %1.8 | %22.1 | %17.1 | %92.0 | %37.0 | %14.8 | %23.1 | %41.9 | %127.0 | %17.8 |

### Son 24 ay (risk %1)

| 2024-10 | 2024-11 | 2024-12 | 2025-01 | 2025-02 | 2025-03 | 2025-04 | 2025-05 | 2025-06 | 2025-07 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 | 2026-01 | 2026-02 | 2026-03 | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %4.2 | %8.9 | %-1.4 | %2.5 | %10.5 | %-1.4 | %13.6 | %18.8 | %-2.1 | %8.5 | %8.8 | %7.6 | %9.4 | %6.5 | %4.2 | %14.7 | %9.3 | %-1.2 | %-3.2 | %1.6 | %-2.7 | %-1.2 | %4.1 | %-3.5 |

---
# Araştırma ayrıntıları (tüm aileler × çıkışlar; IS'te seçilen, OOS'ta ölçülen; çakışmalı işlemlerle tarama)

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1h | SHORT | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | **+0.022R** (31) | +0.142R | %54.8 | 1.04 | 0.6 | 8.61R | 0.453 | ⚠️ Pozitif, anlamsız |
| **XAG** | 4h | SHORT | REJIM · anahtar (ikisi) · Stoch · volatilite şoku + güçlü mum | SABIT_4R | +0.975R (42) | **-0.301R** (24) | -0.147R | %16.7 | 0.65 | 0.4 | 9.60R | 0.801 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | IZ_SUREN_2.5ATR | +0.944R (166) | **+0.149R** (67) | +0.144R | %26.9 | 1.21 | 2.0 | 22.68R | 0.301 | ⚠️ Pozitif, anlamsız |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · hacim şoku + önceden sıkışma | TP1.5>BE_4R | +1.323R (84) | **+0.118R** (42) | +0.113R | %19.0 | 1.19 | 1.3 | 8.48R | 0.346 | ⚠️ Pozitif, anlamsız |
| **NQ** | 4h | LONG | MA · EMA 20/50 kesişimi + günlük trend | IZ_SUREN_2.5ATR | +1.129R (75) | **-0.304R** (43) | -0.395R | %16.3 | 0.63 | 0.9 | 14.34R | 0.866 | ❌ OOS'ta tutmadı |
| **SPX** | 4h | LONG | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | IZ_SUREN_2.5ATR | +0.491R (286) | **+0.382R** (125) | +0.345R | %32.8 | 1.59 | 2.6 | 11.75R | 0.041 | ⚠️ Pozitif, anlamsız |

## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 1h | 4h |
|---|---|---|
| **XAU** | ⚠ +0.022R (31) | ✅ +0.641R (97) |
| **XAG** | ❌ -0.023R (526) | ❌ -0.301R (24) |
| **BTC** | ⚠ +0.015R (135) | ⚠ +0.149R (67) |
| **ETH** | ❌ -0.343R (23) | ⚠ +0.118R (42) |
| **NQ** | ⚠ +0.172R (68) | ❌ -0.304R (43) |
| **SPX** | ❌ -0.387R (21) | ⚠ +0.382R (125) |

## XAU

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,448 | 2011-10-04 → 2022-03-22 | 2022-03-22 → 2026-10-02 | 0.084R | çalıştı |
| 4h | 24,003 | 2011-10-04 → 2022-04-03 | 2022-04-04 → 2026-10-02 | 0.042R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 4h | LONG | Donchian 20 · filtresiz + günlük trend | TP0.5>BE_3R | +0.375R (150) | +0.641R (97) | +0.577R | %34.0 | 2.75 | <0.001 | ✅ Kanıtlı |
| **MA** | 4h | LONG | zaman serisi momentumu 72 bar + günlük trend | IZ_SUREN_2.5ATR | +0.683R (92) | +0.515R (60) | +0.290R | %31.7 | 1.80 | 0.070 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.215R (642) | +0.391R (388) | +0.167R | %35.6 | 1.64 | <0.001 | ✅ Kanıtlı |
| **RSI2** | 1h | iki yön | RSI(2) 5/95 · EMA200 trend + ADX≥20 | IZ_SUREN_2.5ATR | +0.196R (923) | +0.215R (407) | +0.223R | %28.5 | 1.31 | 0.047 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 1h | SHORT | anahtar (ikisi) · Stoch · filtresiz + hacim | SABIT_1.5R | +0.311R (75) | +0.092R (51) | +0.215R | %47.1 | 1.16 | 0.301 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.349R (713) | +0.070R (232) | +0.102R | %28.9 | 1.10 | 0.297 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | SHORT | RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | +0.022R (31) | +0.142R | %54.8 | 1.04 | 0.453 | ⚠️ Pozitif, anlamsız |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.228R | %90.0 | %30.8 | +0.068R | %28.5 | 473 |
| SABIT_4R | +0.191R | %100.0 | %26.4 | -0.010R | %22.8 | 473 |
| SABIT_2.5R | +0.083R | %65.0 | %33.7 | +0.013R | %31.2 | 473 |
| TP1.5>BE_4R | +0.079R | %75.0 | %18.7 | -0.023R | %16.0 | 473 |
| SABIT_3R | +0.072R | %70.0 | %29.2 | -0.006R | %27.1 | 473 |
| SABIT_2R | +0.064R | %75.0 | %38.1 | +0.003R | %36.0 | 473 |
| GENIS_%50@1R>BE_3R | +0.048R | %80.0 | %51.9 | -0.014R | %51.3 | 473 |
| %50@1R>BE_IZ | +0.033R | %75.0 | %53.1 | -0.063R | %50.7 | 473 |
| %50@1R>BE_4R | +0.028R | %65.0 | %52.4 | -0.048R | %50.7 | 473 |
| TP0.5>BE_3R | +0.012R | %55.0 | %14.8 | -0.004R | %13.8 | 473 |
| %50@1R>BE_3R | +0.002R | %60.0 | %52.9 | -0.056R | %50.7 | 473 |
| TP1>BE_2R | -0.001R | %55.0 | %27.6 | -0.042R | %26.1 | 473 |
| TP1>BE_3R | -0.004R | %45.0 | %18.5 | -0.054R | %17.1 | 473 |
| TP1>BE_3R_ERKEN | -0.005R | %40.0 | %17.8 | -0.070R | %16.1 | 473 |
| SABIT_1.5R | -0.012R | %50.0 | %42.6 | -0.002R | %42.8 | 473 |
| %50@1R>BE_2R | -0.020R | %35.0 | %52.1 | -0.050R | %50.7 | 473 |
| SABIT_1R | -0.021R | %30.0 | %52.8 | -0.058R | %50.7 | 473 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %100.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.206R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu · SABIT_1R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2011-10-21 → 2014-11-10 | 22 | %77.3 | +0.464R |
| 2014-11-11 → 2018-08-10 | 22 | %72.7 | +0.366R |
| 2018-10-10 → 2023-02-28 | 22 | %50.0 | -0.082R |
| 2023-03-09 → 2026-09-30 | 22 | %68.2 | +0.288R |

Maksimum düşüş: IS 2.19R · OOS 8.61R

### İlk 15 ayar (1h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.349R (713) | +0.070R (232) | %28.9 |
| 2 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku + seans | IZ_SUREN_2.5ATR | +0.671R (152) | +0.607R (58) | %37.9 |
| 3 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + önceden sıkışma | IZ_SUREN_2.5ATR | +0.338R (672) | +0.029R (228) | %28.5 |
| 4 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku + önceden sıkışma | IZ_SUREN_2.5ATR | +0.619R (159) | +0.415R (71) | %36.6 |
| 5 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + ADX≥20 | IZ_SUREN_2.5ATR | +0.408R (309) | +0.276R (86) | %32.6 |
| 6 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + günlük trend | IZ_SUREN_2.5ATR | +0.377R (371) | +0.286R (125) | %32.0 |
| 7 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + seans | IZ_SUREN_2.5ATR | +0.371R (408) | +0.074R (138) | %29.0 |
| 8 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | IZ_SUREN_2.5ATR | +0.593R (163) | +0.415R (71) | %36.6 |
| 9 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + güçlü mum | IZ_SUREN_2.5ATR | +0.384R (344) | +0.190R (121) | %28.1 |
| 10 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_4R | +0.239R (713) | +0.144R (232) | %25.4 |
| 11 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + ADX≥20 | SABIT_4R | +0.325R (309) | +0.287R (86) | %29.1 |
| 12 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + hacim | IZ_SUREN_2.5ATR | +0.631R (136) | +0.446R (58) | %36.2 |
| 13 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_3R | +0.197R (713) | +0.037R (232) | %28.4 |
| 14 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + önceden sıkışma | SABIT_4R | +0.215R (672) | +0.121R (228) | %25.0 |
| 15 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz + ADX≥20 | TP0.5>BE_3R | +0.208R (309) | +0.047R (86) | %15.1 |

## XAG

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,233 | 2011-10-04 → 2022-03-25 | 2022-03-25 → 2026-10-02 | 0.108R | çalıştı |
| 4h | 24,001 | 2011-10-04 → 2022-04-03 | 2022-04-04 → 2026-10-02 | 0.055R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 4h | SHORT | Donchian 55 · EMA200 trend + önceden sıkışma | SABIT_4R | +0.623R (86) | +0.231R (34) | +0.385R | %26.5 | 1.30 | 0.267 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | SHORT | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.037R (4641) | -0.035R (2093) | +0.025R | %51.6 | 0.93 | 0.928 | ❌ OOS'ta tutmadı |
| **MA** | 1h | SHORT | EMA 50/200 kesişimi + ADX≥20 | SABIT_1R | +0.102R (155) | -0.057R (70) | +0.028R | %51.4 | 0.89 | 0.683 | ❌ OOS'ta tutmadı |
| **RSI2** | 4h | SHORT | RSI(2) 5/95 · EMA200 trend + hacim | GENIS_%50@1R>BE_3R | +0.476R (44) | -0.135R (10) | -0.069R | %40.0 | 0.78 | 0.632 | ⏳ OOS yetersiz |
| **REJIM** | 4h | SHORT | anahtar (ikisi) · Stoch · volatilite şoku + güçlü mum | SABIT_4R | +0.975R (42) | -0.301R (24) | -0.147R | %16.7 | 0.65 | 0.801 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | SHORT | Stoch+WaveTrend · dinamik · volatilite şoku+EMA200 trend | SABIT_4R | +0.846R (40) | -0.489R (5) | -0.335R | %20.0 | 0.42 | 0.807 | ⏳ OOS yetersiz |
| **SQZ** | 4h | SHORT | BB-Keltner sıkışma çözülmesi · filtresiz + önceden sıkışma | GENIS_%50@1R>BE_3R | +0.229R (101) | -0.492R (25) | -0.426R | %32.0 | 0.30 | 0.998 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_4R | +0.106R | %70.6 | %23.9 | -0.047R | %21.0 | 367 |
| TP1.5>BE_4R | +0.029R | %63.2 | %17.1 | -0.124R | %14.2 | 367 |
| TP0.5>BE_3R | +0.016R | %70.0 | %13.8 | -0.099R | %10.2 | 367 |
| %50@1R>BE_4R | -0.013R | %50.0 | %49.9 | -0.129R | %46.0 | 367 |
| %50@1R>BE_IZ | -0.025R | %35.0 | %50.0 | -0.117R | %46.0 | 367 |
| IZ_SUREN_2.5ATR | -0.046R | %42.1 | %25.1 | -0.102R | %24.9 | 367 |
| SABIT_1R | -0.050R | %20.0 | %49.8 | -0.126R | %46.0 | 367 |
| SABIT_2.5R | -0.053R | %11.1 | %28.4 | -0.105R | %27.0 | 367 |
| %50@1R>BE_3R | -0.062R | %25.0 | %49.5 | -0.152R | %46.0 | 367 |
| SABIT_3R | -0.073R | %23.5 | %24.4 | -0.112R | %23.6 | 367 |
| %50@1R>BE_2R | -0.080R | %10.0 | %49.5 | -0.145R | %46.0 | 367 |
| TP1>BE_3R_ERKEN | -0.087R | %25.0 | %14.9 | -0.154R | %13.2 | 367 |
| TP1>BE_3R | -0.095R | %15.0 | %15.5 | -0.177R | %13.7 | 367 |
| SABIT_1.5R | -0.097R | %10.0 | %38.0 | -0.151R | %35.8 | 367 |
| TP1>BE_2R | -0.097R | %10.0 | %22.3 | -0.164R | %21.1 | 367 |
| GENIS_%50@1R>BE_3R | -0.105R | %15.0 | %45.8 | -0.061R | %48.8 | 367 |
| SABIT_2R | -0.148R | %5.6 | %30.0 | -0.114R | %31.1 | 367 |

**Sağlamlık (4h):** IS'te en iyi 17 ayarın %29.4'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.072R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — REJIM · anahtar (ikisi) · Stoch · volatilite şoku + güçlü mum · SABIT_4R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-02-29 → 2015-07-13 | 16 | %68.8 | +2.381R |
| 2015-10-23 → 2019-04-17 | 17 | %29.4 | +0.145R |
| 2019-04-29 → 2023-01-26 | 16 | %18.8 | -0.120R |
| 2023-02-02 → 2026-08-20 | 17 | %17.6 | -0.289R |

Maksimum düşüş: IS 7.42R · OOS 9.60R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · EMA200 trend + önceden sıkışma | IZ_SUREN_2.5ATR | +0.405R (262) | -0.042R (133) | %26.3 |
| 2 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.297R (433) | -0.112R (216) | %25.0 |
| 3 | DONCH · Donchian 20 · EMA200 trend + seans | IZ_SUREN_2.5ATR | +0.347R (321) | -0.023R (144) | %25.0 |
| 4 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_4R | +0.634R (58) | -1.051R (12) | %0.0 |
| 5 | REJIM · yatayda dönüş · Stoch · volatilite şoku + güçlü mum | SABIT_2.5R | +0.431R (69) | -0.171R (44) | %25.0 |
| 6 | DONCH · Donchian 55 · EMA200 trend + günlük trend | %50@1R>BE_IZ | +0.198R (241) | -0.058R (118) | %47.5 |
| 7 | DONCH · Donchian 55 · sıkışma sonrası + ADX≥20 | TP0.5>BE_3R | +0.286R (115) | +0.018R (61) | %13.1 |
| 8 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.513R (58) | -1.051R (12) | %0.0 |
| 9 | REJIM · anahtar (ikisi) · Stoch · volatilite şoku + güçlü mum | SABIT_2.5R | +0.373R (84) | -0.117R (49) | %26.5 |
| 10 | DONCH · Donchian 55 · EMA200 trend | TP0.5>BE_3R | +0.155R (310) | +0.053R (162) | %14.8 |
| 11 | DONCH · Donchian 55 · filtresiz + günlük trend | %50@1R>BE_IZ | +0.190R (238) | -0.058R (118) | %47.5 |
| 12 | DONCH · Donchian 55 · EMA200 trend + günlük trend | TP0.5>BE_3R | +0.175R (241) | -0.030R (118) | %12.7 |
| 13 | DONCH · Donchian 20 · EMA200 trend + önceden sıkışma | SABIT_4R | +0.269R (262) | +0.180R (133) | %26.3 |
| 14 | DONCH · Donchian 20 · filtresiz + günlük trend | IZ_SUREN_2.5ATR | +0.314R (292) | -0.234R (144) | %20.8 |
| 15 | RSI2 · RSI(2) 5/95 · EMA200 trend + hacim | GENIS_%50@1R>BE_3R | +0.272R (70) | -0.328R (32) | %31.2 |

## BTC

Veri: 5m tabanı `None` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 79,883 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-03 | 0.102R | çalıştı |
| 4h | 19,989 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-03 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 4h | iki yön | Donchian 20 · sıkışma sonrası + günlük trend | IZ_SUREN_2.5ATR | +0.944R (166) | +0.149R (67) | +0.144R | %26.9 | 1.21 | 0.301 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.274R (1618) | +0.011R (974) | +0.019R | %26.1 | 1.02 | 0.437 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 4h | iki yön | yatayda dönüş · WaveTrend · filtresiz + günlük trend | SABIT_3R | +0.763R (58) | -0.096R (29) | -0.090R | %24.1 | 0.88 | 0.617 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz + günlük trend | IZ_SUREN_2.5ATR | +0.842R (95) | -0.156R (32) | -0.170R | %18.8 | 0.80 | 0.678 | ❌ OOS'ta tutmadı |
| **RSI2** | 4h | SHORT | RSI(2) 5/95 · EMA200 trend + önceden sıkışma | TP1.5>BE_4R | +0.601R (86) | -0.247R (34) | -0.191R | %8.8 | 0.58 | 0.848 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | zaman serisi momentumu 72 bar + hacim | IZ_SUREN_2.5ATR | +0.971R (107) | -0.251R (49) | -0.253R | %20.4 | 0.66 | 0.851 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch+WaveTrend · dinamik · EMA200 trend+onay mumu | TP1.5>BE_4R | +0.748R (45) | -0.367R (23) | -0.412R | %8.7 | 0.48 | 0.890 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | -0.066R | %35.0 | %23.3 | -0.130R | %24.2 | 366 |
| GENIS_%50@1R>BE_3R | -0.070R | %25.0 | %48.5 | -0.075R | %46.5 | 366 |
| SABIT_1R | -0.081R | %10.0 | %49.3 | -0.163R | %44.9 | 366 |
| %50@1R>BE_2R | -0.097R | %15.0 | %49.8 | -0.150R | %44.9 | 366 |
| %50@1R>BE_IZ | -0.097R | %10.0 | %48.6 | -0.140R | %44.9 | 366 |
| %50@1R>BE_3R | -0.105R | %10.0 | %49.4 | -0.146R | %44.9 | 366 |
| TP1>BE_2R | -0.112R | %25.0 | %22.7 | -0.138R | %23.7 | 366 |
| %50@1R>BE_4R | -0.115R | %15.0 | %48.5 | -0.144R | %44.9 | 366 |
| SABIT_1.5R | -0.121R | %25.0 | %37.9 | -0.178R | %35.3 | 366 |
| TP1>BE_3R_ERKEN | -0.126R | %5.0 | %14.8 | -0.132R | %15.8 | 366 |
| TP1>BE_3R | -0.128R | %5.0 | %14.8 | -0.129R | %16.3 | 366 |
| TP1.5>BE_4R | -0.145R | %10.0 | %13.5 | -0.147R | %14.8 | 366 |
| TP0.5>BE_3R | -0.167R | %5.0 | %9.8 | -0.110R | %11.2 | 366 |
| SABIT_3R | -0.228R | %5.0 | %21.1 | -0.148R | %23.3 | 366 |
| SABIT_2.5R | -0.237R | %5.0 | %23.8 | -0.144R | %26.3 | 366 |
| SABIT_2R | -0.270R | %0.0 | %26.6 | -0.181R | %29.3 | 366 |
| SABIT_4R | -0.290R | %0.0 | %15.7 | -0.168R | %19.4 | 366 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %35.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.062R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · sıkışma sonrası + günlük trend · IZ_SUREN_2.5ATR · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-10-07 → 2019-10-16 | 58 | %46.6 | +1.007R |
| 2019-11-04 → 2021-12-03 | 58 | %27.6 | +0.464R |
| 2021-12-13 → 2024-04-29 | 58 | %41.4 | +1.410R |
| 2024-05-07 → 2026-07-31 | 59 | %25.4 | -0.009R |

Maksimum düşüş: IS 14.83R · OOS 22.68R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | IZ_SUREN_2.5ATR | +0.944R (166) | +0.149R (67) | %26.9 |
| 2 | DONCH · Donchian 20 · sıkışma sonrası + ADX≥20 | IZ_SUREN_2.5ATR | +0.948R (164) | -0.020R (70) | %22.9 |
| 3 | DONCH · Donchian 20 · EMA200 trend + önceden sıkışma | IZ_SUREN_2.5ATR | +0.749R (248) | +0.062R (106) | %25.5 |
| 4 | MA · zaman serisi momentumu 72 bar + hacim | IZ_SUREN_2.5ATR | +0.971R (107) | -0.251R (49) | %20.4 |
| 5 | DONCH · Donchian 20 · hacim şoku + güçlü mum | IZ_SUREN_2.5ATR | +0.677R (237) | -0.108R (102) | %23.5 |
| 6 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | %25.0 |
| 7 | DONCH · Donchian 20 · sıkışma sonrası + önceden sıkışma | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | %25.0 |
| 8 | MA · zaman serisi momentumu 24 bar + hacim | IZ_SUREN_2.5ATR | +0.937R (119) | +0.035R (55) | %30.9 |
| 9 | DONCH · Donchian 20 · EMA200 trend + hacim | IZ_SUREN_2.5ATR | +0.729R (154) | -0.034R (69) | %23.2 |
| 10 | DONCH · Donchian 20 · EMA200 trend + hacim | TP1.5>BE_4R | +0.625R (154) | -0.066R (69) | %14.5 |
| 11 | DONCH · Donchian 20 · hacim şoku + ADX≥20 | IZ_SUREN_2.5ATR | +0.685R (190) | -0.259R (85) | %20.0 |
| 12 | DONCH · Donchian 20 · filtresiz + hacim | IZ_SUREN_2.5ATR | +0.642R (202) | -0.085R (84) | %21.4 |
| 13 | DONCH · Donchian 20 · sıkışma sonrası + güçlü mum | IZ_SUREN_2.5ATR | +0.616R (260) | +0.123R (104) | %26.9 |
| 14 | DONCH · Donchian 55 · hacim şoku + ADX≥20 | IZ_SUREN_2.5ATR | +0.738R (152) | -0.371R (72) | %16.7 |
| 15 | DONCH · Donchian 55 · hacim şoku + seans | IZ_SUREN_2.5ATR | +0.802R (113) | -0.359R (70) | %15.7 |

## ETH

Veri: 5m tabanı `None` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 79,888 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-03 | 0.077R | çalıştı |
| 4h | 19,989 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-03 | 0.037R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | TP1.5>BE_4R | +0.255R (720) | +0.185R (393) | +0.180R | %20.6 | 1.30 | 0.028 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | LONG | Donchian 20 · hacim şoku + önceden sıkışma | TP1.5>BE_4R | +1.323R (84) | +0.118R (42) | +0.113R | %19.0 | 1.19 | 0.346 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · filtresiz + günlük trend | IZ_SUREN_2.5ATR | +0.346R (626) | +0.022R (296) | -0.043R | %28.4 | 1.03 | 0.424 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi + günlük trend | IZ_SUREN_2.5ATR | +0.650R (250) | -0.153R (127) | -0.217R | %22.8 | 0.79 | 0.801 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku + önceden sıkışma | TP1.5>BE_4R | +0.972R (58) | -0.250R (25) | -0.232R | %12.0 | 0.65 | 0.778 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | iki yön | yatayda dönüş · Stoch · volatilite şoku + önceden sıkışma | IZ_SUREN_2.5ATR | +1.443R (41) | -0.264R (17) | -0.322R | %23.5 | 0.62 | 0.779 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | -0.280R | %23.5 | 0.58 | 0.854 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.285R | %95.0 | %33.3 | -0.031R | %26.0 | 350 |
| TP1.5>BE_4R | +0.237R | %85.0 | %20.7 | +0.004R | %17.2 | 350 |
| SABIT_4R | +0.236R | %80.0 | %25.8 | -0.013R | %22.6 | 350 |
| IZ_SUREN_2.5ATR | +0.222R | %65.0 | %30.1 | +0.068R | %27.0 | 350 |
| SABIT_2.5R | +0.174R | %90.0 | %34.8 | -0.047R | %28.8 | 350 |
| TP0.5>BE_3R | +0.143R | %95.0 | %17.7 | -0.025R | %12.3 | 350 |
| TP1>BE_3R | +0.127R | %75.0 | %21.8 | -0.046R | %17.2 | 350 |
| GENIS_%50@1R>BE_3R | +0.100R | %80.0 | %54.7 | -0.004R | %49.5 | 350 |
| TP1>BE_3R_ERKEN | +0.100R | %80.0 | %21.0 | -0.044R | %16.5 | 350 |
| SABIT_1.5R | +0.080R | %75.0 | %45.0 | -0.059R | %39.3 | 350 |
| TP1>BE_2R | +0.066R | %75.0 | %30.0 | -0.046R | %25.5 | 350 |
| %50@1R>BE_IZ | +0.037R | %70.0 | %49.6 | -0.031R | %48.6 | 350 |
| %50@1R>BE_4R | +0.017R | %55.0 | %50.3 | -0.052R | %48.6 | 350 |
| SABIT_2R | +0.010R | %55.0 | %35.2 | -0.027R | %33.8 | 350 |
| %50@1R>BE_3R | -0.013R | %50.0 | %49.5 | -0.058R | %48.6 | 350 |
| %50@1R>BE_2R | -0.016R | %55.0 | %49.5 | -0.058R | %48.6 | 350 |
| SABIT_1R | -0.068R | %25.0 | %48.9 | -0.070R | %48.6 | 350 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %80.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.120R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · hacim şoku + önceden sıkışma · TP1.5>BE_4R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-10-13 → 2020-04-01 | 31 | %45.2 | +1.476R |
| 2020-04-06 → 2022-08-10 | 32 | %43.8 | +1.429R |
| 2022-09-02 → 2024-07-19 | 31 | %32.3 | +0.843R |
| 2024-08-23 → 2026-09-11 | 32 | %15.6 | -0.048R |

Maksimum düşüş: IS 4.21R · OOS 8.48R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | TP1.5>BE_4R | +1.089R (94) | +0.338R (39) | %23.1 |
| 2 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | TP1>BE_3R_ERKEN | +0.867R (94) | +0.082R (39) | %20.5 |
| 3 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | TP1>BE_3R | +0.865R (94) | +0.082R (39) | %20.5 |
| 4 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | SABIT_4R | +0.982R (94) | +0.364R (39) | %28.2 |
| 5 | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | TP1.5>BE_4R | +0.820R (158) | +0.045R (63) | %17.5 |
| 6 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | SABIT_3R | +0.876R (94) | +0.287R (39) | %33.3 |
| 7 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | SABIT_2.5R | +0.823R (94) | +0.120R (39) | %33.3 |
| 8 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | IZ_SUREN_2.5ATR | +0.931R (94) | +0.356R (39) | %33.3 |
| 9 | REJIM · yatayda dönüş · Stoch · volatilite şoku + önceden sıkışma | IZ_SUREN_2.5ATR | +1.443R (41) | -0.264R (17) | %23.5 |
| 10 | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | TP1>BE_3R_ERKEN | +0.727R (158) | -0.003R (63) | %19.0 |
| 11 | DONCH · Donchian 55 · sıkışma sonrası + günlük trend | TP0.5>BE_3R | +0.759R (94) | +0.056R (39) | %15.4 |
| 12 | DONCH · Donchian 20 · sıkışma sonrası + günlük trend | TP1>BE_3R | +0.718R (158) | -0.003R (63) | %19.0 |
| 13 | DONCH · Donchian 20 · hacim şoku + önceden sıkışma | TP1.5>BE_4R | +0.764R (171) | +0.232R (75) | %21.3 |
| 14 | DONCH · Donchian 55 · sıkışma sonrası + hacim | TP1.5>BE_4R | +0.888R (87) | +0.314R (49) | %22.4 |
| 15 | DONCH · Donchian 20 · sıkışma sonrası + hacim | TP1.5>BE_4R | +0.781R (131) | +0.109R (57) | %19.3 |

## NQ

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 74,920 | 2012-01-19 → 2022-12-08 | 2022-12-08 → 2026-10-02 | 0.072R | çalıştı |
| 4h | 21,254 | 2012-01-19 → 2022-10-06 | 2022-10-06 → 2026-10-02 | 0.038R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 1h | LONG | RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +0.203R (1525) | +0.108R (643) | +0.006R | %28.1 | 1.15 | 0.116 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.146R (4945) | +0.096R (3734) | -0.006R | %28.3 | 1.14 | 0.004 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +1.027R (71) | +0.034R (30) | -0.058R | %26.7 | 1.05 | 0.459 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · filtresiz + güçlü mum | SABIT_2.5R | +0.412R (93) | -0.013R (46) | +0.007R | %30.4 | 0.98 | 0.522 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | LONG | Donchian 55 · sıkışma sonrası + seans | SABIT_4R | +0.768R (101) | -0.069R (36) | -0.144R | %19.4 | 0.92 | 0.582 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | LONG | yatayda dönüş · WaveTrend · volatilite şoku | IZ_SUREN_2.5ATR | +1.006R (56) | -0.105R (25) | -0.197R | %24.0 | 0.84 | 0.626 | ❌ OOS'ta tutmadı |
| **MA** | 4h | LONG | EMA 20/50 kesişimi + günlük trend | IZ_SUREN_2.5ATR | +1.129R (75) | -0.304R (43) | -0.395R | %16.3 | 0.63 | 0.866 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | +0.204R | %100.0 | %59.4 | +0.039R | %52.1 | 342 |
| SABIT_3R | +0.128R | %75.0 | %29.2 | +0.057R | %27.4 | 342 |
| SABIT_4R | +0.059R | %65.0 | %23.5 | +0.063R | %22.8 | 342 |
| IZ_SUREN_2.5ATR | +0.033R | %45.0 | %28.6 | +0.006R | %27.2 | 342 |
| TP1>BE_3R_ERKEN | +0.025R | %45.0 | %18.0 | +0.008R | %17.7 | 342 |
| TP0.5>BE_3R | +0.013R | %40.0 | %15.0 | +0.021R | %14.6 | 342 |
| TP1>BE_3R | +0.008R | %30.0 | %18.7 | +0.007R | %18.6 | 342 |
| SABIT_2R | -0.007R | %50.0 | %34.2 | -0.016R | %33.9 | 342 |
| TP1.5>BE_4R | -0.010R | %45.0 | %15.4 | +0.001R | %16.0 | 342 |
| SABIT_1.5R | -0.012R | %40.0 | %40.8 | -0.026R | %40.3 | 342 |
| TP1>BE_2R | -0.028R | %25.0 | %26.1 | -0.025R | %26.2 | 342 |
| %50@1R>BE_3R | -0.029R | %35.0 | %48.1 | -0.029R | %48.5 | 342 |
| SABIT_2.5R | -0.037R | %40.0 | %28.4 | -0.013R | %29.2 | 342 |
| SABIT_1R | -0.049R | %10.0 | %49.2 | -0.064R | %48.5 | 342 |
| %50@1R>BE_IZ | -0.051R | %20.0 | %48.7 | -0.043R | %48.5 | 342 |
| %50@1R>BE_2R | -0.062R | %10.0 | %48.1 | -0.045R | %48.5 | 342 |
| %50@1R>BE_4R | -0.091R | %0.0 | %47.5 | -0.019R | %48.5 | 342 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %50.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.066R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · EMA 20/50 kesişimi + günlük trend · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-04-30 → 2016-07-01 | 29 | %27.6 | -0.016R |
| 2016-09-05 → 2019-12-06 | 30 | %66.7 | +1.996R |
| 2020-01-31 → 2024-03-20 | 29 | %34.5 | +0.602R |
| 2024-04-12 → 2026-09-18 | 30 | %16.7 | -0.176R |

Maksimum düşüş: IS 8.31R · OOS 14.34R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | +1.223R (46) | -0.122R (22) | %27.3 |
| 2 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_4R | +0.981R (46) | +0.361R (22) | %31.8 |
| 3 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | +0.605R (46) | +0.410R (22) | %68.2 |
| 4 | DONCH · Donchian 55 · EMA200 trend + seans | SABIT_4R | +0.510R (246) | -0.040R (107) | %20.6 |
| 5 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.788R (46) | +0.240R (22) | %31.8 |
| 6 | REJIM · trendde geri çekilme · Stoch · filtresiz + günlük trend | IZ_SUREN_2.5ATR | +0.888R (63) | +0.491R (25) | %40.0 |
| 7 | MA · EMA 20/50 kesişimi + günlük trend | IZ_SUREN_2.5ATR | +0.728R (102) | -0.308R (62) | %17.7 |
| 8 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | TP1.5>BE_4R | +0.593R (108) | -0.093R (49) | %12.2 |
| 9 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend | IZ_SUREN_2.5ATR | +1.017R (48) | -0.166R (27) | %29.6 |
| 10 | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +0.659R (108) | -0.149R (49) | %22.4 |
| 11 | DONCH · Donchian 55 · sıkışma sonrası + seans | SABIT_4R | +0.555R (146) | +0.040R (51) | %21.6 |
| 12 | MA · EMA 20/50 kesişimi + günlük trend | TP0.5>BE_3R | +0.473R (102) | -0.241R (62) | %8.1 |
| 13 | DONCH · Donchian 55 · filtresiz + seans | SABIT_4R | +0.445R (273) | +0.052R (114) | %22.8 |
| 14 | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend | GENIS_%50@1R>BE_3R | +0.537R (48) | +0.312R (27) | %66.7 |
| 15 | OSC · Stoch · sabit · EMA200 trend | TP0.5>BE_3R | +0.346R (284) | -0.032R (138) | %13.0 |

## SPX

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 75,563 | 2012-01-16 → 2022-11-28 | 2022-11-28 → 2026-10-02 | 0.095R | çalıştı |
| 4h | 21,503 | 2012-01-16 → 2022-09-20 | 2022-09-20 → 2026-10-02 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MA** | 4h | LONG | EMA 20/50 kesişimi | TP1>BE_3R | +0.350R (136) | +0.528R (62) | +0.499R | %33.9 | 2.14 | 0.009 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | LONG | RSI(2) 10/90 · EMA200 trend + seans | IZ_SUREN_2.5ATR | +0.491R (286) | +0.382R (125) | +0.345R | %32.8 | 1.59 | 0.041 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.039R (5097) | +0.226R (820) | +0.156R | %27.7 | 1.31 | 0.007 | ✅ Kanıtlı |
| **REJIM** | 4h | LONG | anahtar (ikisi) · RSI · filtresiz | SABIT_3R | +0.420R (106) | +0.135R (44) | +0.125R | %29.5 | 1.18 | 0.314 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 55 · sıkışma sonrası + seans | TP0.5>BE_3R | +0.332R (144) | +0.051R (60) | +0.049R | %13.3 | 1.15 | 0.375 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | +0.341R (120) | -0.023R (64) | +0.019R | %40.6 | 0.96 | 0.560 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku + günlük trend | SABIT_4R | +0.737R (59) | -0.387R (21) | -0.356R | %14.3 | 0.59 | 0.839 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_2.5R | +0.165R | %90.0 | %34.7 | +0.015R | %30.3 | 350 |
| SABIT_3R | +0.123R | %80.0 | %29.5 | +0.028R | %27.0 | 350 |
| TP1>BE_3R | +0.099R | %80.0 | %21.1 | +0.026R | %20.3 | 350 |
| %50@1R>BE_IZ | +0.088R | %75.0 | %53.0 | -0.044R | %46.6 | 350 |
| IZ_SUREN_2.5ATR | +0.082R | %85.0 | %29.8 | +0.019R | %28.6 | 350 |
| %50@1R>BE_4R | +0.078R | %70.0 | %53.0 | -0.030R | %46.6 | 350 |
| SABIT_4R | +0.067R | %70.0 | %23.7 | +0.025R | %22.0 | 350 |
| TP1>BE_2R | +0.058R | %75.0 | %30.0 | -0.038R | %27.2 | 350 |
| %50@1R>BE_3R | +0.057R | %75.0 | %52.8 | -0.045R | %46.6 | 350 |
| SABIT_2R | +0.051R | %75.0 | %36.6 | -0.003R | %34.8 | 350 |
| TP1>BE_3R_ERKEN | +0.045R | %70.0 | %18.3 | +0.026R | %19.6 | 350 |
| TP1.5>BE_4R | +0.029R | %65.0 | %16.8 | +0.039R | %17.6 | 350 |
| %50@1R>BE_2R | +0.027R | %65.0 | %51.7 | -0.077R | %46.6 | 350 |
| GENIS_%50@1R>BE_3R | +0.006R | %60.0 | %52.1 | -0.061R | %47.2 | 350 |
| SABIT_1.5R | +0.003R | %45.0 | %42.0 | -0.074R | %39.0 | 350 |
| TP0.5>BE_3R | -0.000R | %45.0 | %13.5 | +0.045R | %15.5 | 350 |
| SABIT_1R | -0.008R | %40.0 | %52.0 | -0.117R | %46.6 | 350 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %85.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.156R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — RSI2 · RSI(2) 10/90 · EMA200 trend + seans · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-03-28 → 2015-05-22 | 102 | %38.2 | +0.648R |
| 2015-05-29 → 2019-10-31 | 103 | %35.0 | +0.387R |
| 2019-11-05 → 2023-04-17 | 103 | %34.0 | +0.332R |
| 2023-04-19 → 2026-09-04 | 103 | %33.0 | +0.466R |

Maksimum düşüş: IS 22.27R · OOS 11.75R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | IZ_SUREN_2.5ATR | +0.409R (409) | +0.234R (181) | %29.8 |
| 2 | DONCH · Donchian 55 · sıkışma sonrası + seans | TP0.5>BE_3R | +0.332R (144) | +0.051R (60) | %13.3 |
| 3 | DONCH · Donchian 55 · sıkışma sonrası + seans | TP1.5>BE_4R | +0.403R (144) | +0.267R (60) | %20.0 |
| 4 | DONCH · Donchian 55 · sıkışma sonrası + seans | SABIT_4R | +0.429R (144) | +0.185R (60) | %26.7 |
| 5 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | SABIT_2.5R | +0.216R (409) | +0.151R (181) | %34.3 |
| 6 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | SABIT_3R | +0.231R (409) | +0.254R (181) | %32.6 |
| 7 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | TP1>BE_3R_ERKEN | +0.195R (409) | +0.109R (181) | %20.4 |
| 8 | DONCH · Donchian 55 · sıkışma sonrası + seans | SABIT_3R | +0.360R (144) | +0.312R (60) | %35.0 |
| 9 | DONCH · Donchian 55 · sıkışma sonrası + seans | IZ_SUREN_2.5ATR | +0.442R (144) | +0.268R (60) | %33.3 |
| 10 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | TP1>BE_3R | +0.199R (409) | +0.173R (181) | %23.8 |
| 11 | RSI2 · RSI(2) 10/90 · EMA200 trend + seans | TP1>BE_2R | +0.172R (409) | +0.101R (181) | %32.0 |
| 12 | RSI2 · RSI(2) 10/90 · EMA200 trend + günlük trend | IZ_SUREN_2.5ATR | +0.235R (591) | +0.189R (266) | %31.2 |
| 13 | DONCH · Donchian 20 · EMA200 trend + seans | TP1.5>BE_4R | +0.248R (319) | -0.124R (139) | %12.9 |
| 14 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.229R (594) | +0.184R (267) | %31.1 |
| 15 | DONCH · Donchian 55 · sıkışma sonrası + seans | TP1>BE_3R_ERKEN | +0.300R (144) | +0.317R (60) | %25.0 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
