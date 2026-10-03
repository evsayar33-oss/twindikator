# ATVS Lab v3 Raporu — 2026-10-03 06:05 UTC

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

Kapılar: **K1** OOS (n ≥ 30, beklenti > 0, alfa > 0, Benjamini–Hochberg yanlış keşif oranı ≤ 0.10 — 49 aday birlikte test edildi) · **K2** tüm dönem (n ≥ 80, beklenti > 0) · **K3** maliyet ×2 · **K4** komşu parametrelerin ≥ %70'i pozitif · **K5** yılların ≥ %60'i pozitif · **K6** veri şüphesi yok. Tümü çakışmasız: her strateji aynı anda tek pozisyon taşır. Not: tohum adaylar önceki raporun OOS sonuçlarından seçildi; onlar için OOS tam bağımsız değildir — asıl bağımsız sınav canlı kâğıt işlemdir.

| ID | Varlık | ZD | Yön | Giriş | Çıkış | Tüm dönem beklenti (n) | İsabet | PF | OOS beklenti (n) | OOS alfa | Maliyet×2 | Komşu + | Yıl + | İşlem/yıl | Maks. düşüş (R) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **F1_XAU_4h_DONCH** | XAU | 4h | yalnız LONG | DONCH · Donchian 20 · EMA200 trend | TP1>BE_3R | +0.312R (360) | %27.8 | 1.61 | +0.601R (125) | +0.528R | +0.269R | %100.0 | %73.3 | 24.3 | 12.6 |

### Kurallar (TradingView / manuel uygulama için)

- **F1_XAU_4h_DONCH** — **XAU 4h · yalnızca LONG** — Mum kapanışı önceki 20 mumun en yükseğinin üstündeyse LONG, en düşüğünün altındaysa SHORT (ilk kırılım). Filtre: LONG için kapanış EMA200 üstünde, SHORT için altında. Giriş: sinyal mumunun kapanışından sonraki mumun açılışında. Stop: giriş ∓ 1.0 × ATR(14) (sinyal mumundaki ATR). +1.0R'de stop girişe çekilir. Hedef: +3.0R. 48 mum sonra hâlâ açıksa kapanış fiyatından kapatılır.

### Finalistlerin yıllık sonuçları (yıl ortalama R · işlem)

| ID | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1_XAU_4h_DONCH | -1.03 (1) | +0.09 (22) | -0.12 (12) | -0.21 (24) | +0.02 (17) | +0.63 (24) | +0.45 (28) | -0.11 (20) | +0.12 (28) | +0.39 (28) | -0.21 (24) | +0.32 (22) | +0.43 (27) | +0.57 (31) | +1.13 (36) | +0.35 (16) |

### Komşu parametre testleri

- **F1_XAU_4h_DONCH**: ATR 10: +0.258R · ATR 20: +0.268R · zaman bariyeri 36: +0.312R · zaman bariyeri 72: +0.316R · stop ×0.8: +0.231R · stop ×1.25: +0.302R · hedef −0.5R: +0.212R · hedef +0.5R: +0.315R · trend EMA 150: +0.298R · trend EMA 250: +0.335R · Donchian 15: +0.232R · Donchian 25: +0.367R

### Tüm adaylar ve kapı sonuçları

| Varlık | ZD | Giriş | Çıkış | Yön | Kaynak | K1 | K2 | K3 | K4 | K5 | K6 | Tüm dönem | OOS | Not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAU | 4h | DONCH · Donchian 20 · EMA200 trend | TP1>BE_3R | yalnız LONG | tohum | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | +0.312R (360) | +0.601R (125) | **FİNALİST** |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.175R (546) | +0.262R (170) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | iki yön | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.557R (379) | +0.762R (108) |  |
| NQ | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.094R (3430) | +0.078R (1356) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | iki yön | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.279R (928) | +0.041R (228) |  |
| NQ | 1h | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.217R (823) | +0.068R (267) |  |
| XAU | 1h | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | yalnız SHORT | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.259R (88) | +0.022R (31) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | yalnız SHORT | IS t=2.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.230R (495) | -0.308R (123) |  |
| XAU | 1h | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend | SABIT_1R | yalnız SHORT | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.222R (92) | +0.022R (31) |  |
| XAU | 1h | OSC · RSI+Stoch · dinamik · hacim şoku+volatilite şoku+EMA200 trend+onay mumu | SABIT_1R | yalnız SHORT | IS t=2.6 | ✗ | ✗ | · | · | ✓ | ✓ | +0.262R (70) | +0.110R (27) |  |
| XAU | 4h | DONCH · Donchian 55 · filtresiz | TP1>BE_3R | iki yön | IS t=2.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.239R (505) | +0.225R (159) |  |
| XAU | 4h | DONCH · Donchian 55 · EMA200 trend | TP1>BE_3R | iki yön | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.237R (466) | +0.258R (148) |  |
| XAU | 4h | DONCH · Donchian 55 · sıkışma sonrası | %50@1R>BE_IZ | iki yön | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.215R (286) | +0.121R (92) |  |
| XAU | 4h | MA · EMA 50/200 kesişimi | SABIT_1R | yalnız SHORT | IS t=2.4 | ✗ | ✗ | · | · | ✗ | ✓ | +0.134R (73) | -0.378R (18) |  |
| XAG | 4h | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | yalnız SHORT | IS t=2.4 | ✗ | ✓ | · | · | ✗ | ✓ | +0.071R (127) | -0.519R (35) |  |
| XAG | 4h | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | iki yön | IS t=2.3 | ✗ | ✓ | · | · | ✗ | ✓ | +0.175R (607) | -0.081R (200) |  |
| XAG | 4h | REJIM · yatayda dönüş · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | yalnız SHORT | IS t=2.2 | ✗ | ✓ | · | · | ✗ | ✓ | +0.030R (108) | -0.580R (33) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.401R (427) | +0.028R (127) |  |
| BTC | 1h | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.245R (762) | -0.104R (230) |  |
| BTC | 1h | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.099R (1239) | -0.087R (385) |  |
| BTC | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.233R (214) | +0.287R (38) |  |
| BTC | 4h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.292R (953) | +0.121R (377) |  |
| BTC | 4h | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | iki yön | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.421R (412) | -0.026R (128) |  |
| BTC | 4h | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | iki yön | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.437R (488) | -0.042R (148) |  |
| BTC | 4h | DONCH · Donchian 20 · hacim şoku | GENIS_%50@1R>BE_3R | iki yön | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.137R (372) | -0.107R (122) |  |
| ETH | 1h | DONCH · Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | iki yön | IS t=3.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.131R (754) | -0.033R (217) |  |
| ETH | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.079R (2247) | +0.004R (567) |  |
| ETH | 1h | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | iki yön | IS t=3.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.101R (2392) | -0.044R (733) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku | GENIS_%50@1R>BE_3R | iki yön | IS t=3.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.111R (1164) | +0.044R (348) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_2R | yalnız LONG | IS t=4.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.317R (202) | +0.100R (61) |  |
| ETH | 4h | DONCH · Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=3.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.407R (118) | +0.174R (41) |  |
| ETH | 4h | DONCH · Donchian 20 · sıkışma sonrası | TP1>BE_3R | iki yön | IS t=3.9 | ✗ | ✓ | · | · | ✓ | ✓ | +0.283R (420) | +0.096R (130) |  |
| ETH | 4h | META · gradient boosting · tüm adaylar · üst %35 | TP1>BE_3R | yalnız LONG | IS t=3.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.205R (766) | +0.166R (273) |  |
| NQ | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | iki yön | IS t=4.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.075R (3787) | +0.075R (1422) |  |
| NQ | 1h | MA · zaman serisi momentumu 24 bar | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.221R (1608) | +0.063R (492) |  |
| NQ | 1h | MA · EMA 50/200 kesişimi | SABIT_3R | yalnız LONG | IS t=3.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.461R (212) | +0.186R (68) |  |
| NQ | 1h | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | iki yön | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.192R (2056) | +0.141R (637) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi | TP1>BE_3R | yalnız LONG | IS t=4.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.370R (186) | -0.157R (63) |  |
| NQ | 4h | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=3.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.418R (101) | +0.248R (30) |  |
| NQ | 4h | OSC · Stoch · sabit · EMA200 trend | TP1>BE_3R | iki yön | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.187R (422) | -0.090R (138) |  |
| NQ | 4h | OSC · WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | GENIS_%50@1R>BE_3R | iki yön | IS t=3.3 | ✗ | ✗ | · | · | ✓ | ✓ | +0.542R (68) | +0.410R (22) |  |
| SPX | 1h | OSC · Stoch · sabit · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.161R (1852) | +0.063R (556) |  |
| SPX | 1h | OSC · Stoch · sabit · onay mumu | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.156R (1548) | +0.044R (464) |  |
| SPX | 1h | OSC · Stoch · sabit · EMA200 trend+onay mumu | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.149R (758) | -0.081R (232) |  |
| SPX | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.4 | ✗ | ✗ | · | · | ✓ | ✓ | +0.201R (71) | -0.387R (20) |  |
| SPX | 4h | OSC · Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | yalnız LONG | IS t=3.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.214R (184) | -0.023R (64) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.268R (799) | +0.284R (241) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.311R (501) | +0.326R (155) |  |
| SPX | 4h | MA · EMA 20/50 kesişimi | TP1>BE_3R | yalnız LONG | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.406R (198) | +0.528R (62) |  |

## Portföy (v3, olay tabanlı)

1 finalist · 2011-11-30 → 2026-09-21 · aynı anda en fazla 4 pozisyon · küme başına en fazla 1 (ABD endeksleri / metaller / kripto) · günlük zarar limiti %3 · stratejiler arası ortalama korelasyon nan

### ✅ Önerilen risk: işlem başına kasanın **%1.5**'i
Bu seviyede Monte Carlo'ya göre 1 yıllık maksimum düşüş %95 olasılıkla **%14.9**'i aşmıyor (hedef ≤ %15.0). Tarihsel: yıllık getiri **%11.2**, maksimum düşüş **%17.7**, en uzun düşüş 1391 gün, pozitif ay oranı %41.9, ayda 2.0 işlem.

| Risk/işlem | Yıllık getiri | Toplam | Maks. düşüş | En uzun düşüş (gün) | Sharpe | Pozitif ay | İşlem/ay | Atlanan (açık/küme/gün) | MC %95 maks. düşüş | MC yılı zararla kapama | MC medyan yıllık | MC en kötü %5 | OOS yıllık | OOS maks. düşüş |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %0.25 | %1.9 | %32.0 | %3.1 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %2.6 | %19.6 | %1.8 | %-1.5 | %4.3 | %1.9 |
| %0.5 | %3.8 | %73.2 | %6.2 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %5.2 | %20.0 | %3.7 | %-2.9 | %8.7 | %3.7 |
| %0.75 | %5.7 | %125.7 | %9.1 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %7.7 | %20.2 | %5.5 | %-4.3 | %13.2 | %5.5 |
| %1 | %7.5 | %192.2 | %12.0 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %10.2 | %20.4 | %7.3 | %-5.8 | %17.8 | %7.2 |
| %1.5 ◀ | %11.2 | %380.8 | %17.7 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %14.9 | %20.6 | %11.0 | %-8.6 | %27.4 | %10.7 |
| %2 | %14.8 | %671.5 | %23.0 | 1391 | 0.90 | %41.9 | 2.0 | 0/0/0 | %19.4 | %20.7 | %14.6 | %-11.5 | %37.4 | %14.0 |

### Yıllık getiriler (risk %1.5)

| 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %-1.6 | %2.5 | %-2.4 | %-7.8 | %0.1 | %24.2 | %19.6 | %-3.5 | %4.4 | %16.7 | %-7.7 | %10.4 | %18.2 | %28.7 | %80.5 | %8.2 |

### Son 24 ay (risk %1.5)

| 2024-10 | 2024-11 | 2024-12 | 2025-01 | 2025-02 | 2025-03 | 2025-04 | 2025-05 | 2025-06 | 2025-07 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 | 2026-01 | 2026-02 | 2026-03 | 2026-04 | 2026-05 | 2026-06 | 2026-07 | 2026-08 | 2026-09 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| %2.7 | %4.4 | %2.8 | %1.0 | %2.8 | %5.7 | %14.0 | %9.1 | %-3.1 | %-3.2 | %-3.2 | %13.9 | %9.1 | %4.5 | %12.2 | %9.1 | %2.9 | %2.9 | %-1.6 | %-3.1 | %0.0 | %-1.5 | %2.9 | %-3.0 |

---
# Araştırma ayrıntıları (tüm aileler × çıkışlar; IS'te seçilen, OOS'ta ölçülen; çakışmalı işlemlerle tarama)

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1h | SHORT | OSC · RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | **+0.022R** (31) | +0.142R | %54.8 | 1.04 | 0.6 | 8.61R | 0.453 | ⚠️ Pozitif, anlamsız |
| **XAG** | 4h | SHORT | REJIM · anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.295R (92) | **-0.519R** (35) | -0.453R | %28.6 | 0.30 | 0.6 | 19.09R | 1.000 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | iki yön | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | **+0.030R** (132) | +0.031R | %25.0 | 1.04 | 4.0 | 36.38R | 0.439 | ⚠️ Pozitif, anlamsız |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | **+0.329R** (61) | +0.311R | %34.4 | 1.48 | 1.9 | 11.52R | 0.090 | ⚠️ Pozitif, anlamsız |
| **NQ** | 4h | LONG | MA · EMA 20/50 kesişimi | IZ_SUREN_2.5ATR | +0.891R (123) | **-0.125R** (64) | -0.217R | %21.9 | 0.83 | 1.3 | 19.06R | 0.710 | ❌ OOS'ta tutmadı |
| **SPX** | 4h | LONG | OSC · Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | +0.341R (120) | **-0.023R** (64) | +0.019R | %40.6 | 0.96 | 1.3 | 7.75R | 0.560 | ❌ OOS'ta tutmadı |

## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 1h | 4h |
|---|---|---|
| **XAU** | ⚠ +0.022R (31) | ⚠ +0.242R (160) |
| **XAG** | ⚠ +0.021R (442) | ❌ -0.519R (35) |
| **BTC** | ⚠ +0.001R (130) | ⚠ +0.030R (132) |
| **ETH** | ❌ -0.007R (211) | ⚠ +0.329R (61) |
| **NQ** | ⚠ +0.172R (68) | ❌ -0.125R (64) |
| **SPX** | ⚠ +0.042R (573) | ❌ -0.023R (64) |

## XAU

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,450 | 2011-10-04 → 2022-03-22 | 2022-03-22 → 2026-10-02 | 0.084R | çalıştı |
| 4h | 24,004 | 2011-10-04 → 2022-04-01 | 2022-04-03 → 2026-10-02 | 0.042R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.166R (663) | +0.399R (410) | +0.174R | %33.9 | 1.63 | <0.001 | ✅ Kanıtlı |
| **REJIM** | 4h | SHORT | anahtar (ikisi) · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.648R (71) | +0.390R (26) | +0.538R | %42.3 | 1.66 | 0.205 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 55 · filtresiz | TP1>BE_3R | +0.246R (346) | +0.242R (160) | +0.237R | %25.0 | 1.49 | 0.030 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | iki yön | RSI(2) 5/95 · EMA200 trend | IZ_SUREN_2.5ATR | +0.122R (1367) | +0.084R (580) | +0.091R | %26.2 | 1.12 | 0.201 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.349R (713) | +0.070R (232) | +0.102R | %28.9 | 1.10 | 0.297 | ⚠️ Pozitif, anlamsız |
| **OSC** | 1h | SHORT | RSI+Stoch · dinamik · hacim şoku+EMA200 trend+onay mumu | SABIT_1R | +0.388R (57) | +0.022R (31) | +0.142R | %54.8 | 1.04 | 0.453 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | SHORT | EMA 50/200 kesişimi | SABIT_1R | +0.302R (55) | -0.378R (18) | -0.274R | %33.3 | 0.46 | 0.950 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.085R | %75.0 | %28.6 | +0.018R | %26.7 | 235 |
| GENIS_%50@1R>BE_3R | -0.002R | %35.0 | %50.4 | -0.037R | %50.4 | 235 |
| SABIT_3R | -0.003R | %40.0 | %27.1 | -0.063R | %25.7 | 235 |
| %50@1R>BE_IZ | -0.028R | %30.0 | %50.7 | -0.090R | %49.5 | 235 |
| SABIT_2R | -0.034R | %25.0 | %34.7 | -0.045R | %34.2 | 235 |
| TP1>BE_3R | -0.036R | %20.0 | %18.0 | -0.105R | %15.8 | 235 |
| %50@1R>BE_3R | -0.040R | %25.0 | %50.7 | -0.093R | %49.5 | 235 |
| TP1>BE_2R | -0.043R | %15.0 | %26.7 | -0.073R | %25.2 | 235 |
| %50@1R>BE_2R | -0.044R | %20.0 | %50.7 | -0.077R | %49.5 | 235 |
| SABIT_1R | -0.046R | %25.0 | %51.5 | -0.082R | %49.5 | 235 |
| SABIT_1.5R | -0.060R | %15.0 | %40.7 | -0.036R | %41.4 | 235 |

**Sağlamlık (1h):** IS'te en iyi 20 ayarın %90.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.081R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

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
| 2 | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku | IZ_SUREN_2.5ATR | +0.593R (163) | +0.415R (71) | %36.6 |
| 3 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_3R | +0.197R (713) | +0.037R (232) | %28.4 |
| 4 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | TP1>BE_3R | +0.157R (713) | +0.045R (232) | %19.8 |
| 5 | DONCH · Donchian 55 · EMA200 trend | IZ_SUREN_2.5ATR | +0.144R (1218) | +0.124R (547) | %29.3 |
| 6 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | %50@1R>BE_IZ | +0.101R (713) | +0.013R (232) | %53.0 |
| 7 | RSI2 · RSI(2) 5/95 · EMA200 trend | IZ_SUREN_2.5ATR | +0.122R (1367) | +0.084R (580) | %26.2 |
| 8 | DONCH · Donchian 55 · filtresiz | IZ_SUREN_2.5ATR | +0.120R (1317) | +0.093R (581) | %28.2 |
| 9 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | %50@1R>BE_3R | +0.080R (713) | +0.013R (232) | %53.0 |
| 10 | MA · EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.067R (2669) | +0.013R (1183) | %26.5 |
| 11 | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.152R (728) | +0.295R (323) | %30.7 |
| 12 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | TP1>BE_2R | +0.074R (713) | +0.019R (232) | %28.4 |
| 13 | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | SABIT_2R | +0.086R (713) | +0.032R (232) | %37.1 |
| 14 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.081R (1803) | -0.010R (769) | %27.3 |
| 15 | RSI2 · RSI(2) 5/95 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.031R (1367) | +0.007R (580) | %50.3 |

## XAG

Veri: 5m tabanı `None` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 89,235 | 2011-10-04 → 2022-03-25 | 2022-03-25 → 2026-10-02 | 0.108R | çalıştı |
| 4h | 24,002 | 2011-10-04 → 2022-04-03 | 2022-04-04 → 2026-10-02 | 0.055R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 1h | SHORT | RSI(2) 10/90 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.011R (1205) | +0.021R (442) | +0.082R | %52.9 | 1.04 | 0.348 | ⚠️ Pozitif, anlamsız |
| **MA** | 1h | SHORT | EMA 50/200 kesişimi | SABIT_1R | +0.065R (200) | -0.037R (80) | +0.049R | %52.5 | 0.93 | 0.629 | ❌ OOS'ta tutmadı |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.013R (1947) | -0.047R (904) | -0.008R | %49.0 | 0.91 | 0.898 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | iki yön | Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.297R (433) | -0.112R (216) | -0.091R | %25.0 | 0.84 | 0.825 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | SHORT | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | +0.216R (108) | -0.512R (26) | -0.446R | %30.8 | 0.28 | 0.999 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | SHORT | anahtar (ikisi) · Stoch · volatilite şoku | GENIS_%50@1R>BE_3R | +0.295R (92) | -0.519R (35) | -0.453R | %28.6 | 0.30 | 1.000 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | WaveTrend · dinamik · volatilite şoku+EMA200 trend+onay mumu | SABIT_3R | +0.513R (58) | -1.051R (12) | -0.946R | %0.0 | 0.00 | 1.000 | ⏳ OOS yetersiz |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | -0.050R | %42.1 | %24.6 | -0.213R | %22.8 | 197 |
| SABIT_3R | -0.064R | %18.8 | %24.7 | -0.210R | %21.0 | 197 |
| GENIS_%50@1R>BE_3R | -0.090R | %21.1 | %46.5 | -0.120R | %46.7 | 197 |
| %50@1R>BE_IZ | -0.113R | %15.0 | %45.9 | -0.187R | %43.7 | 197 |
| SABIT_1R | -0.118R | %5.0 | %46.4 | -0.172R | %43.7 | 197 |
| %50@1R>BE_3R | -0.119R | %10.5 | %47.0 | -0.219R | %43.7 | 197 |
| TP1>BE_3R | -0.122R | %5.6 | %14.9 | -0.266R | %11.5 | 197 |
| %50@1R>BE_2R | -0.137R | %5.0 | %45.9 | -0.194R | %43.7 | 197 |
| SABIT_2R | -0.138R | %11.1 | %30.3 | -0.172R | %29.2 | 197 |
| TP1>BE_2R | -0.162R | %0.0 | %21.6 | -0.217R | %19.6 | 197 |
| SABIT_1.5R | -0.176R | %0.0 | %34.8 | -0.223R | %32.9 | 197 |

**Sağlamlık (4h):** IS'te en iyi 18 ayarın %38.9'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.049R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

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
| 1h | 79,881 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-03 | 0.102R | çalıştı |
| 4h | 19,989 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-03 | 0.049R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.293R (498) | +0.263R (219) | +0.265R | %28.3 | 1.38 | 0.068 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.639R (306) | +0.030R (132) | +0.031R | %25.0 | 1.04 | 0.439 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | iki yön | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.274R (1618) | +0.011R (974) | +0.019R | %26.1 | 1.02 | 0.437 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.399R (571) | -0.105R (256) | -0.099R | %25.4 | 0.86 | 0.807 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | LONG | yatayda dönüş · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.551R (130) | -0.201R (62) | -0.277R | %22.6 | 0.74 | 0.801 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch · sabit · onay mumu | IZ_SUREN_2.5ATR | +0.415R (281) | -0.304R (150) | -0.380R | %20.7 | 0.62 | 0.981 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | +0.497R (183) | -0.328R (64) | -0.327R | %18.8 | 0.59 | 0.952 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.081R | %25.0 | %47.0 | -0.079R | %45.6 | 205 |
| SABIT_1R | -0.089R | %25.0 | %48.7 | -0.171R | %44.4 | 205 |
| %50@1R>BE_IZ | -0.102R | %15.0 | %48.0 | -0.134R | %44.4 | 205 |
| SABIT_1.5R | -0.123R | %15.0 | %37.7 | -0.184R | %35.0 | 205 |
| %50@1R>BE_2R | -0.125R | %10.0 | %47.9 | -0.141R | %44.4 | 205 |
| %50@1R>BE_3R | -0.126R | %5.0 | %47.9 | -0.129R | %44.4 | 205 |
| IZ_SUREN_2.5ATR | -0.128R | %25.0 | %23.0 | -0.136R | %25.3 | 205 |
| TP1>BE_3R | -0.140R | %10.0 | %14.6 | -0.087R | %18.0 | 205 |
| TP1>BE_2R | -0.142R | %15.0 | %22.2 | -0.112R | %25.2 | 205 |
| SABIT_3R | -0.184R | %10.0 | %22.3 | -0.106R | %24.3 | 205 |
| SABIT_2R | -0.188R | %15.0 | %29.3 | -0.158R | %30.0 | 205 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %15.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.138R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

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
| 11 | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.274R (1618) | +0.011R (974) | %26.1 |
| 12 | DONCH · Donchian 20 · hacim şoku | TP1>BE_3R | +0.342R (266) | -0.145R (125) | %14.4 |
| 13 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +0.407R (369) | -0.065R (160) | %26.9 |
| 14 | DONCH · Donchian 55 · sıkışma sonrası | %50@1R>BE_IZ | +0.379R (162) | -0.113R (74) | %48.6 |
| 15 | DONCH · Donchian 55 · filtresiz | IZ_SUREN_2.5ATR | +0.458R (287) | -0.333R (127) | %16.5 |

## ETH

Veri: 5m tabanı `None` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 1h | 79,886 | 2017-08-17 → 2024-01-08 | 2024-01-08 → 2026-10-03 | 0.077R | çalıştı |
| 4h | 19,989 | 2017-08-17 → 2024-01-07 | 2024-01-07 → 2026-10-03 | 0.037R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.267R (720) | +0.359R (393) | +0.234R | %31.6 | 1.55 | 0.004 | ✅ Kanıtlı |
| **DONCH** | 4h | LONG | Donchian 20 · hacim şoku | SABIT_3R | +0.630R (141) | +0.329R (61) | +0.311R | %34.4 | 1.48 | 0.090 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.291R (531) | +0.141R (243) | +0.073R | %29.6 | 1.21 | 0.178 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi | IZ_SUREN_2.5ATR | +0.234R (582) | -0.104R (296) | -0.177R | %23.0 | 0.86 | 0.806 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | %50@1R>BE_IZ | +0.485R (64) | -0.207R (25) | -0.201R | %40.0 | 0.67 | 0.808 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | Stoch+WaveTrend · sabit · EMA200 trend | SABIT_2R | +0.594R (47) | -0.335R (17) | -0.280R | %23.5 | 0.58 | 0.854 | ❌ OOS'ta tutmadı |
| **REJIM** | 4h | iki yön | yatayda dönüş · Stoch · volatilite şoku | IZ_SUREN_2.5ATR | +0.769R (94) | -0.417R (38) | -0.482R | %18.4 | 0.43 | 0.986 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.253R | %80.0 | %30.3 | -0.021R | %25.4 | 198 |
| SABIT_3R | +0.145R | %70.0 | %30.5 | -0.095R | %24.5 | 198 |
| TP1>BE_3R | +0.042R | %50.0 | %19.1 | -0.073R | %16.7 | 198 |
| GENIS_%50@1R>BE_3R | +0.042R | %70.0 | %51.3 | -0.031R | %47.8 | 198 |
| %50@1R>BE_IZ | +0.032R | %55.0 | %50.1 | -0.061R | %47.1 | 198 |
| SABIT_2R | +0.027R | %50.0 | %35.7 | -0.087R | %31.8 | 198 |
| SABIT_1.5R | +0.024R | %45.0 | %42.7 | -0.119R | %36.9 | 198 |
| %50@1R>BE_3R | +0.009R | %45.0 | %51.1 | -0.086R | %47.1 | 198 |
| TP1>BE_2R | -0.037R | %40.0 | %25.4 | -0.080R | %24.5 | 198 |
| %50@1R>BE_2R | -0.038R | %40.0 | %49.9 | -0.089R | %47.1 | 198 |
| SABIT_1R | -0.041R | %40.0 | %50.1 | -0.099R | %47.1 | 198 |

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
| 1h | 74,920 | 2012-01-19 → 2022-12-08 | 2022-12-08 → 2026-10-02 | 0.072R | çalıştı |
| 4h | 21,254 | 2012-01-19 → 2022-10-06 | 2022-10-06 → 2026-10-02 | 0.038R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **DONCH** | 1h | LONG | Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.419R (284) | +0.329R (161) | +0.227R | %29.8 | 1.46 | 0.051 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_1.5R | +0.212R (100) | +0.127R (56) | +0.210R | %48.2 | 1.23 | 0.225 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1h | LONG | RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | +0.203R (1525) | +0.108R (643) | +0.006R | %28.1 | 1.15 | 0.116 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.146R (4945) | +0.096R (3734) | -0.006R | %28.3 | 1.14 | 0.004 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | WaveTrend · dinamik · volatilite şoku+onay mumu | IZ_SUREN_2.5ATR | +1.027R (71) | +0.034R (30) | -0.058R | %26.7 | 1.05 | 0.459 | ⚠️ Pozitif, anlamsız |
| **REJIM** | 4h | LONG | yatayda dönüş · WaveTrend · volatilite şoku | IZ_SUREN_2.5ATR | +1.006R (56) | -0.105R (25) | -0.197R | %24.0 | 0.84 | 0.626 | ❌ OOS'ta tutmadı |
| **MA** | 4h | LONG | EMA 20/50 kesişimi | IZ_SUREN_2.5ATR | +0.891R (123) | -0.125R (64) | -0.217R | %21.9 | 0.83 | 0.710 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.177R | %75.0 | %30.6 | +0.048R | %27.2 | 177 |
| GENIS_%50@1R>BE_3R | +0.146R | %80.0 | %56.0 | +0.039R | %51.8 | 177 |
| IZ_SUREN_2.5ATR | +0.077R | %60.0 | %28.9 | +0.002R | %26.9 | 177 |
| SABIT_1.5R | +0.029R | %55.0 | %42.5 | -0.035R | %40.0 | 177 |
| TP1>BE_3R | -0.000R | %40.0 | %17.9 | +0.003R | %18.1 | 177 |
| %50@1R>BE_IZ | -0.018R | %30.0 | %50.0 | -0.043R | %49.4 | 177 |
| SABIT_2R | -0.023R | %35.0 | %33.6 | -0.028R | %33.5 | 177 |
| TP1>BE_2R | -0.035R | %15.0 | %25.8 | -0.020R | %26.0 | 177 |
| %50@1R>BE_3R | -0.051R | %15.0 | %48.5 | -0.022R | %49.4 | 177 |
| %50@1R>BE_2R | -0.059R | %5.0 | %48.1 | -0.033R | %49.4 | 177 |
| SABIT_1R | -0.085R | %0.0 | %47.4 | -0.047R | %49.4 | 177 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %60.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.109R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

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
| 14 | REJIM · trendde geri çekilme · Stoch · filtresiz | IZ_SUREN_2.5ATR | +0.749R (71) | +0.491R (25) | %40.0 |
| 15 | OSC · Stoch · sabit · EMA200 trend | SABIT_3R | +0.338R (284) | -0.017R (138) | %25.4 |

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
| **RSI2** | 4h | LONG | RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.235R (684) | +0.291R (293) | +0.254R | %31.4 | 1.44 | 0.022 | ⚠️ Pozitif, anlamsız |
| **META** | 1h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.039R (5097) | +0.226R (820) | +0.156R | %27.7 | 1.31 | 0.007 | ✅ Kanıtlı |
| **REJIM** | 4h | LONG | anahtar (ikisi) · RSI · filtresiz | SABIT_3R | +0.420R (106) | +0.135R (44) | +0.125R | %29.5 | 1.18 | 0.314 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | LONG | Donchian 20 · filtresiz | SABIT_3R | +0.229R (322) | +0.064R (139) | +0.054R | %28.1 | 1.09 | 0.336 | ⚠️ Pozitif, anlamsız |
| **OSC** | 4h | LONG | Stoch+WaveTrend · sabit · filtresiz | SABIT_1.5R | +0.341R (120) | -0.023R (64) | +0.019R | %40.6 | 0.96 | 0.560 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | +0.402R (52) | -0.352R (21) | -0.323R | %33.3 | 0.50 | 0.926 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | +0.101R | %80.0 | %28.8 | -0.068R | %24.6 | 184 |
| IZ_SUREN_2.5ATR | +0.047R | %65.0 | %28.0 | -0.093R | %26.7 | 184 |
| GENIS_%50@1R>BE_3R | -0.006R | %50.0 | %50.0 | -0.114R | %44.4 | 184 |
| SABIT_2R | -0.006R | %40.0 | %34.7 | -0.079R | %32.3 | 184 |
| %50@1R>BE_IZ | -0.020R | %50.0 | %48.7 | -0.120R | %44.0 | 184 |
| TP1>BE_3R | -0.020R | %40.0 | %18.7 | -0.059R | %18.3 | 184 |
| TP1>BE_2R | -0.037R | %45.0 | %26.6 | -0.105R | %25.1 | 184 |
| %50@1R>BE_2R | -0.047R | %30.0 | %49.1 | -0.137R | %44.0 | 184 |
| SABIT_1R | -0.065R | %15.0 | %49.2 | -0.168R | %44.0 | 184 |
| %50@1R>BE_3R | -0.082R | %30.0 | %46.7 | -0.114R | %44.0 | 184 |
| SABIT_1.5R | -0.092R | %30.0 | %38.3 | -0.151R | %35.9 | 184 |

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
| 1 | RSI2 · RSI(2) 10/90 · EMA200 trend | IZ_SUREN_2.5ATR | +0.229R (594) | +0.184R (267) | %31.1 |
| 2 | OSC · WaveTrend · dinamik · hacim şoku+onay mumu | IZ_SUREN_2.5ATR | +0.482R (117) | +0.045R (33) | %30.3 |
| 3 | RSI2 · RSI(2) 10/90 · EMA200 trend | TP1>BE_3R | +0.115R (594) | +0.160R (267) | %23.2 |
| 4 | RSI2 · RSI(2) 10/90 · EMA200 trend | %50@1R>BE_IZ | +0.082R (594) | +0.094R (267) | %51.3 |
| 5 | RSI2 · RSI(2) 10/90 · EMA200 trend | TP1>BE_2R | +0.078R (594) | +0.100R (267) | %31.8 |
| 6 | MA · zaman serisi momentumu 72 bar | TP1>BE_3R | +0.131R (377) | -0.100R (161) | %16.8 |
| 7 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | +0.116R (594) | +0.207R (267) | %31.5 |
| 8 | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | +0.077R (1519) | +0.115R (637) | %28.1 |
| 9 | RSI2 · RSI(2) 10/90 · filtresiz | TP1>BE_2R | +0.029R (1519) | +0.021R (637) | %28.4 |
| 10 | MA · zaman serisi momentumu 72 bar | IZ_SUREN_2.5ATR | +0.195R (377) | -0.124R (161) | %27.3 |
| 11 | MA · zaman serisi momentumu 72 bar | TP1>BE_2R | +0.094R (377) | -0.106R (161) | %24.8 |
| 12 | OSC · WaveTrend · dinamik · hacim şoku | IZ_SUREN_2.5ATR | +0.363R (144) | +0.038R (47) | %31.9 |
| 13 | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_2R | +0.070R (594) | +0.119R (267) | %39.0 |
| 14 | DONCH · Donchian 20 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.057R (437) | -0.028R (190) | %50.0 |
| 15 | MA · EMA 9/21 kesişimi | SABIT_3R | +0.087R (651) | +0.173R (275) | %30.5 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
