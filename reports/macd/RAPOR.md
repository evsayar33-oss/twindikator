# ATVS Lab v3 Raporu — 2026-10-07 19:28 UTC

**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).
**Seçim** ilk %70 veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %30 (OOS) verisine göre** verilir. ✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · ⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.
Giriş: sinyalden sonraki bar açılışı · zaman bariyeri 48 bar · aynı barda hedef+stop = stop. TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.

**Odak:** zaman dilimleri 15m, 30m, 1h, 4h, 1d · aileler MACDYON, DONCH, MA, RSI2, SQZ, OSC. **Alfa** = aynı çıkışla aynı dönemde rastgele girişe göre fark (piyasanın kendi yükselişini ayıklar). 🚩 = fiziksel olarak inandırıcı olmayan sonuç (veri hatası belirtisi) — seçimden çıkarılır.

## Veri doğrulama (yfinance günlük kapanışla ay ay karşılaştırma)

| Varlık | Taban | Dönem | Referans | Durum | Ay | **Eksik ay** | Düzeltilen ay | Atılan ay | Atılan sıçrama | Medyan sapma |
|---|---|---|---|---|---|---|---|---|---|---|
| XAU | 1h | 2011-10 → 2026-10 | GC=F | temiz | 181 | 0 | 0 | 0 | 0 | %0.1 |
| XAU | 5m | 2024-10 → 2026-10 | GC=F | temiz | 25 | 0 | 0 | 0 | 0 | %0.3 |
| ETH | 1h | 2017-08 → 2026-10 | ETH-USD | düzeltildi | 108 | 0 | 0 | 0 | 4 | %0.1 |
| ETH | 5m | 2024-10 → 2026-10 | ETH-USD | düzeltildi | 25 | 0 | 0 | 0 | 4 | %0.0 |
| BTC | 1h | 2017-08 → 2026-10 | BTC-USD | düzeltildi | 111 | 0 | 0 | 0 | 9 | %0.1 |
| BTC | 5m | 2024-10 → 2026-10 | BTC-USD | düzeltildi | 25 | 0 | 0 | 0 | 1 | %0.0 |
| XAG | 1h | 2011-10 → 2026-10 | SI=F | düzeltildi | 181 | 0 | 0 | 0 | 1 | %0.2 |
| XAG | 5m | 2024-10 → 2026-10 | SI=F | temiz | 25 | 0 | 0 | 0 | 0 | %0.2 |
| NQ | 1h | 2012-01 → 2026-10 | NQ=F | düzeltildi | 178 | 1 | 42 | 0 | 0 | %0.1 |
| NQ | 5m | 2024-10 → 2026-10 | NQ=F | temiz | 25 | 0 | 0 | 0 | 0 | %0.3 |
| SPX | 1h | 2012-01 → 2026-10 | ES=F | düzeltildi | 178 | 0 | 0 | 0 | 1 | %0.2 |
| SPX | 5m | 2024-10 → 2026-10 | ES=F | temiz | 25 | 0 | 0 | 0 | 0 | %0.3 |

## Finalistler (v3) — çakışmasız backtest + sağlamlık kapıları

Kapılar: **K1** OOS (n ≥ 30, beklenti > 0, alfa > 0, Benjamini–Hochberg yanlış keşif oranı ≤ 0.10 — 54 aday birlikte test edildi) · **K2** tüm dönem (n ≥ 80, beklenti > 0) · **K3** maliyet ×2 · **K4** komşu parametrelerin ≥ %70'i pozitif · **K5** yılların ≥ %60'i pozitif · **K6** veri şüphesi yok. Tümü çakışmasız: her strateji aynı anda tek pozisyon taşır. Not: tohum adaylar önceki raporun OOS sonuçlarından seçildi; onlar için OOS tam bağımsız değildir — asıl bağımsız sınav canlı kâğıt işlemdir.

> **Hiçbir aday tüm kapıları geçemedi.** Canlı kâğıt işlem motoru sinyal üretmeyecek. Aşağıdaki aday tablosu hangi kapıda elendiklerini gösterir.


### Tüm adaylar ve kapı sonuçları

| Varlık | ZD | Giriş | Çıkış | Yön | Kaynak | K1 | K2 | K3 | K4 | K5 | K6 | Tüm dönem | OOS | Not |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XAU | 4h | DONCH · Donchian 20 · EMA200 trend | TP1>BE_3R | yalnız LONG | tohum | ✗ | ✗ | · | · | ✗ | ✓ | -0.008R (360) | +0.309R (125) |  |
| SPX | 4h | RSI2 · RSI(2) 10/90 · EMA200 trend | SABIT_3R | yalnız LONG | tohum | ✗ | ✗ | · | · | ✗ | ✓ | -0.303R (547) | -0.206R (171) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | iki yön | tohum | ✗ | ✓ | · | · | ✓ | ✓ | +0.508R (379) | +0.725R (107) |  |
| NQ | 1h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✗ | · | · | ✗ | ✓ | -0.315R (3062) | -0.358R (1277) |  |
| XAU | 1h | SQZ · BB-Keltner sıkışma çözülmesi · filtresiz | IZ_SUREN_2.5ATR | iki yön | tohum | ✗ | ✗ | · | · | ✗ | ✓ | -0.319R (926) | -0.488R (229) |  |
| NQ | 1h | REJIM · anahtar (ikisi) · Stoch · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | tohum | ✗ | ✗ | · | · | ✗ | ✓ | -0.362R (824) | -0.469R (268) |  |
| ETH | 30m | OSC · Stoch · dinamik · volatilite şoku+onay mumu + MACD yön 1s | IZ_SUREN_2.5ATR | iki yön | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.387R (271) | -0.226R (81) |  |
| ETH | 30m | OSC · Stoch · dinamik · volatilite şoku + MACD yön 1s | IZ_SUREN_2.5ATR | iki yön | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.299R (336) | -0.299R (106) |  |
| ETH | 30m | OSC · Stoch · dinamik · hacim şoku+volatilite şoku + MACD yön 1s | IZ_SUREN_2.5ATR | iki yön | IS t=2.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.384R (275) | -0.172R (82) |  |
| ETH | 30m | OSC · Stoch · dinamik · hacim şoku + MACD yön 1s | IZ_SUREN_2.5ATR | yalnız SHORT | IS t=2.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.549R (146) | -0.108R (34) |  |
| ETH | 30m | OSC · RSI+Stoch+WaveTrend · dinamik · onay mumu + MACD yön | SABIT_4R | yalnız SHORT | IS t=2.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.414R (170) | +0.223R (51) |  |
| ETH | 30m | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu + MACD yön | GENIS_%50@1R>BE_3R | yalnız SHORT | IS t=2.3 | ✗ | ✗ | · | · | ✓ | ✓ | +0.346R (71) | +0.224R (28) |  |
| ETH | 1h | DONCH · Donchian 55 · sıkışma sonrası | GENIS_%50@1R>BE_3R | iki yön | IS t=2.8 | ✗ | ✓ | · | · | ✗ | ✓ | +0.082R (756) | -0.096R (219) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku | TP0.5>BE_3R | yalnız LONG | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.098R (632) | -0.101R (186) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku + MACD yön | GENIS_%50@1R>BE_3R | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.134R (624) | +0.068R (185) |  |
| ETH | 1h | DONCH · Donchian 55 · hacim şoku + MACD yön 1s | GENIS_%50@1R>BE_3R | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.134R (624) | +0.068R (185) |  |
| ETH | 1h | RSI2 · RSI(2) 10/90 · EMA200 trend + MACD yön | IZ_SUREN_2.5ATR | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.058R (1650) | -0.085R (517) |  |
| ETH | 1h | RSI2 · RSI(2) 10/90 · EMA200 trend + MACD yön 1s | IZ_SUREN_2.5ATR | iki yön | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.058R (1650) | -0.085R (517) |  |
| ETH | 4h | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1.5>BE_4R | yalnız LONG | IS t=4.4 | ✗ | ✓ | · | · | ✓ | ✓ | +0.639R (124) | -0.189R (48) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku | %50@1R>BE_4R | yalnız LONG | IS t=4.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.374R (200) | +0.177R (59) |  |
| ETH | 4h | DONCH · Donchian 20 · hacim şoku + MACD yön | %50@1R>BE_4R | iki yön | IS t=4.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.377R (197) | +0.130R (60) |  |
| ETH | 4h | DONCH · Donchian 55 · sıkışma sonrası + MACD yön 1s | SABIT_2.5R | yalnız LONG | IS t=4.1 | ✗ | ✗ | · | · | ✓ | ✓ | +0.802R (76) | +0.388R (26) |  |
| ETH | 4h | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1>BE_3R_ERKEN | iki yön | IS t=4.0 | ✗ | ✓ | · | · | ✓ | ✓ | +0.461R (200) | +0.161R (64) |  |
| ETH | 4h | DONCH · Donchian 55 · sıkışma sonrası | TP1.5>BE_4R | yalnız LONG | IS t=3.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.847R (118) | +0.573R (41) |  |
| ETH | 1d | MACDYON · yön + histogram dönüşü (1s eşdeğeri) | SABIT_4R | iki yön | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.505R (94) | +0.257R (26) |  |
| ETH | 1d | DONCH · Donchian 20 · filtresiz | SABIT_2.5R | yalnız LONG | IS t=2.5 | ✗ | ✗ | · | · | ✓ | ✓ | +0.445R (63) | -0.091R (18) |  |
| ETH | 1d | MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri) | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.3 | ✗ | ✗ | · | · | ✓ | ✓ | +0.322R (75) | +0.284R (20) |  |
| ETH | 1d | MACDYON · yön + hızlı MACD(12,26,9) kesişimi (1s eşdeğeri) | TP0.5>BE_3R | iki yön | IS t=2.0 | ✗ | ✗ | · | · | ✓ | ✓ | +0.329R (77) | +0.258R (26) |  |
| BTC | 30m | OSC · Stoch · sabit · volatilite şoku+EMA200 trend + MACD yön 1s | GENIS_%50@1R>BE_3R | yalnız SHORT | IS t=2.1 | ✗ | ✗ | · | · | ✓ | ✓ | +0.282R (55) | +0.030R (12) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası + MACD yön | SABIT_4R | yalnız LONG | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.150R (205) | -0.821R (58) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası + MACD yön 1s | SABIT_4R | yalnız LONG | IS t=2.8 | ✗ | ✓ | · | · | ✓ | ✓ | +0.150R (205) | -0.821R (58) |  |
| BTC | 1h | DONCH · Donchian 55 · sıkışma sonrası | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.7 | ✗ | ✓ | · | · | ✓ | ✓ | +0.308R (427) | -0.091R (127) |  |
| BTC | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku + MACD yön | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.260R (122) | -0.102R (18) |  |
| BTC | 1h | SQZ · BB-Keltner sıkışma çözülmesi · hacim şoku + MACD yön 1s | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.260R (122) | -0.102R (18) |  |
| BTC | 1h | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.149R (764) | -0.218R (232) |  |
| BTC | 4h | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | iki yön | IS t=3.5 | ✗ | ✓ | · | · | ✓ | ✓ | +0.347R (413) | -0.123R (128) |  |
| BTC | 4h | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | iki yön | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.373R (488) | -0.126R (147) |  |
| BTC | 4h | DONCH · Donchian 55 · hacim şoku + MACD yön 1s | %50@1R>BE_4R | yalnız SHORT | IS t=3.3 | ✗ | ✗ | · | · | ✓ | ✓ | +0.343R (77) | -0.150R (29) |  |
| BTC | 4h | DONCH · Donchian 55 · hacim şoku | TP0.5>BE_3R | yalnız SHORT | IS t=3.3 | ✗ | ✓ | · | · | ✓ | ✓ | +0.304R (129) | -0.077R (45) |  |
| BTC | 4h | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | iki yön | IS t=3.2 | ✗ | ✓ | · | · | ✓ | ✓ | +0.289R (372) | -0.193R (120) |  |
| BTC | 4h | META · gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | yalnız LONG | IS t=3.1 | ✗ | ✓ | · | · | ✓ | ✓ | +0.213R (643) | +0.166R (228) |  |
| BTC | 1d | MACDYON · yön + hızlı MACD(12,26,9) kesişimi (1s eşdeğeri) | SABIT_2.5R | iki yön | IS t=3.0 | ✗ | ✗ | · | · | ✓ | ✓ | +0.676R (66) | +0.632R (22) |  |
| BTC | 1d | MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | SABIT_4R | yalnız LONG | IS t=2.8 | ✗ | ✗ | · | · | ✓ | ✓ | +0.722R (62) | +0.405R (20) |  |
| BTC | 1d | RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.8 | ✗ | ✓ | · | · | ✗ | ✓ | +0.334R (113) | +0.227R (34) |  |
| BTC | 1d | RSI2 · RSI(2) 10/90 · filtresiz + MACD yön 1s | SABIT_4R | yalnız LONG | IS t=2.7 | ✗ | ✗ | · | · | ✓ | ✓ | +0.728R (59) | +0.484R (19) |  |
| BTC | 1d | META · gradient boosting · tüm adaylar · üst %35 | TP0.5>BE_3R | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.151R (138) | +0.059R (76) |  |
| BTC | 1d | MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri) | IZ_SUREN_2.5ATR | iki yön | IS t=2.4 | ✗ | ✓ | · | · | ✗ | ✓ | +0.496R (126) | +0.408R (42) |  |
| XAG | 4h | OSC · WaveTrend · dinamik · volatilite şoku+onay mumu + MACD yön 1s | SABIT_4R | iki yön | IS t=2.1 | ✗ | ✗ | · | · | ✗ | ✓ | +0.368R (75) | -0.369R (24) |  |
| XAG | 1d | MA · zaman serisi momentumu 24 bar | TP1>BE_2R | yalnız SHORT | IS t=2.4 | ✗ | ✓ | · | · | ✗ | ✓ | +0.189R (104) | -0.318R (29) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi + MACD yön | IZ_SUREN_2.5ATR | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✗ | ✓ | +0.415R (97) | -0.628R (36) |  |
| NQ | 4h | MA · EMA 20/50 kesişimi | TP0.5>BE_3R | yalnız LONG | IS t=2.6 | ✗ | ✓ | · | · | ✓ | ✓ | +0.143R (186) | -0.287R (63) |  |
| NQ | 4h | OSC · Stoch · sabit · volatilite şoku + MACD yön 1s | TP0.5>BE_3R | yalnız SHORT | IS t=2.0 | ✗ | ✓ | · | · | ✗ | ✓ | +0.065R (84) | -0.583R (33) |  |
| NQ | 1d | MACDYON · yön + EMA20'ye geri çekilme (bar) | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.4 | ✗ | ✗ | · | · | ✓ | ✓ | +0.189R (79) | +0.122R (30) |  |
| NQ | 1d | RSI2 · RSI(2) 10/90 · EMA200 trend | GENIS_%50@1R>BE_3R | yalnız LONG | IS t=2.0 | ✗ | ✓ | · | · | ✗ | ✓ | +0.047R (111) | -0.216R (35) |  |

## Portföy (v3, olay tabanlı)

> Portföy kurulamadı: finalist yok

---
# Araştırma ayrıntıları (tüm aileler × çıkışlar; IS'te seçilen, OOS'ta ölçülen; çakışmalı işlemlerle tarama)

## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)

| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 1d | SHORT | MACDYON · yön dönüşü (1s eşdeğeri) | SABIT_2R | +0.297R (60) | **-0.073R** (28) | +0.385R | %39.3 | 0.90 | 0.5 | 10.28R | 0.608 | ❌ OOS'ta tutmadı |
| **ETH** | 4h | LONG | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1.5>BE_4R | +1.145R (77) | **-0.189R** (48) | -0.136R | %12.5 | 0.72 | 1.5 | 23.46R | 0.790 | ❌ OOS'ta tutmadı |
| **BTC** | 4h | SHORT | DONCH · Donchian 20 · hacim şoku + MACD yön | IZ_SUREN_2.5ATR | +1.168R (58) | **+0.185R** (32) | +0.351R | %37.5 | 1.30 | 1.0 | 7.13R | 0.310 | ⚠️ Pozitif, anlamsız |
| **XAG** | 1d | SHORT | MA · zaman serisi momentumu 24 bar | TP1>BE_2R | +0.384R (75) | **-0.242R** (30) | -0.060R | %20.0 | 0.61 | 0.6 | 12.29R | 0.872 | ❌ OOS'ta tutmadı |
| **NQ** | 4h | LONG | MA · EMA 20/50 kesişimi + MACD yön | IZ_SUREN_2.5ATR | +1.030R (61) | **-0.628R** (36) | -0.403R | %16.7 | 0.37 | 0.8 | 22.69R | 0.996 | ❌ OOS'ta tutmadı |
| **SPX** | 1d | iki yön | DONCH · Donchian 55 · filtresiz + MACD yön 1s | SABIT_1.5R | +0.177R (57) | **-0.211R** (20) | +0.022R | %45.0 | 0.70 | 0.4 | 5.75R | 0.775 | ❌ OOS'ta tutmadı |

## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi

| Varlık | 15m | 30m | 1h | 4h | 1d |
|---|---|---|---|---|---|
| **XAU** | ❌ -0.967R (16) | ❌ -0.375R (24) | ❌ -0.644R (83) | ⚠ +0.133R (89) | ❌ -0.073R (28) |
| **ETH** | ❌ -0.122R (90) | ❌ -0.071R (30) | ❌ -0.086R (631) | ❌ -0.189R (48) | ⚠ +0.592R (39) |
| **BTC** | ❌ -0.332R (21) | ⏳ +0.030R (12) | ❌ -0.466R (59) | ⚠ +0.185R (32) | ⚠ +0.568R (21) |
| **XAG** | ❌ -0.168R (348) | ❌ -0.107R (15) | ❌ -0.181R (1256) | ❌ -0.404R (25) | ❌ -0.242R (30) |
| **NQ** | ❌ -0.816R (18) | ❌ -1.112R (37) | ❌ -0.325R (68) | ❌ -0.628R (36) | ⚠ +0.171R (40) |
| **SPX** | ❌ -0.441R (34) | ❌ -0.655R (62) | ❌ -0.504R (42) | ❌ -0.469R (27) | ❌ -0.211R (20) |

## XAU

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 47,263 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 0.836R | çalıştı |
| 30m | 23,634 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 0.578R | çalıştı |
| 1h | 89,429 | 2011-10-09 → 2022-03-25 | 2022-03-25 → 2026-10-07 | 0.586R | çalıştı |
| 4h | 23,999 | 2011-10-09 → 2022-04-07 | 2022-04-07 → 2026-10-07 | 0.294R | çalıştı |
| 1d | 4,666 | 2011-10-09 → 2022-04-07 | 2022-04-08 → 2026-10-07 | 0.120R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MA** | 1d | LONG | zaman serisi momentumu 72 bar | GENIS_%50@1R>BE_3R | +0.119R (45) | +0.490R (14) | +0.405R | %71.4 | 2.41 | 0.071 | ⏳ OOS yetersiz |
| **OSC** | 1d | LONG | Stoch · dinamik · filtresiz + MACD yön | SABIT_1R | +0.120R (42) | +0.276R (21) | +0.366R | %71.4 | 1.86 | 0.082 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | iki yön | Donchian 55 · filtresiz + MACD yön | TP0.5>BE_3R | +0.071R (157) | +0.133R (89) | +0.383R | %24.7 | 1.25 | 0.208 | ⚠️ Pozitif, anlamsız |
| **MACDYON** | 1d | SHORT | yön dönüşü (1s eşdeğeri) | SABIT_2R | +0.297R (60) | -0.073R (28) | +0.385R | %39.3 | 0.90 | 0.608 | ❌ OOS'ta tutmadı |
| **META** | 4h | SHORT | gradient boosting · tüm adaylar · üst %35 | GENIS_%50@1R>BE_3R | -0.253R (1715) | -0.208R (409) | +0.092R | %49.9 | 0.66 | 1.000 | ❌ OOS'ta tutmadı |
| **RSI2** | 1d | SHORT | RSI(2) 10/90 · filtresiz + MACD yön 1s | TP1>BE_3R_ERKEN | +0.036R (80) | -0.489R (39) | -0.089R | %7.7 | 0.30 | 0.999 | ❌ OOS'ta tutmadı |
| **SQZ** | 15m | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku | SABIT_4R | +0.439R (40) | -0.967R (16) | -0.128R | %12.5 | 0.30 | 0.990 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1d) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| IZ_SUREN_2.5ATR | +0.458R | %75.0 | %30.9 | +0.420R | %27.9 | 42 |
| SABIT_4R | +0.090R | %50.0 | %28.2 | +0.025R | %27.3 | 42 |
| TP1.5>BE_4R | +0.034R | %55.0 | %22.8 | +0.023R | %22.5 | 42 |
| GENIS_%50@1R>BE_3R | -0.051R | %50.0 | %53.2 | -0.013R | %54.0 | 42 |
| SABIT_3R | -0.098R | %25.0 | %29.7 | -0.079R | %30.6 | 42 |
| SABIT_2.5R | -0.100R | %25.0 | %33.2 | -0.107R | %33.2 | 42 |
| TP0.5>BE_3R | -0.123R | %35.0 | %14.0 | -0.083R | %15.4 | 42 |
| %50@1R>BE_IZ | -0.127R | %25.0 | %47.2 | -0.097R | %47.5 | 42 |
| SABIT_1.5R | -0.153R | %25.0 | %42.2 | -0.137R | %42.9 | 42 |
| TP1>BE_3R | -0.166R | %20.0 | %19.9 | -0.143R | %20.7 | 42 |
| TP1>BE_3R_ERKEN | -0.180R | %15.0 | %17.6 | -0.151R | %19.0 | 42 |
| SABIT_2R | -0.186R | %20.0 | %35.1 | -0.148R | %36.5 | 42 |
| %50@1R>BE_3R | -0.211R | %10.0 | %46.0 | -0.211R | %45.4 | 42 |
| %50@1R>BE_4R | -0.218R | %15.0 | %42.4 | -0.195R | %43.5 | 42 |
| SABIT_1R | -0.222R | %5.0 | %47.8 | -0.215R | %48.4 | 42 |
| %50@1R>BE_2R | -0.223R | %5.0 | %47.8 | -0.220R | %47.7 | 42 |
| TP1>BE_2R | -0.227R | %0.0 | %25.7 | -0.192R | %27.0 | 42 |

**Sağlamlık (1d):** IS'te en iyi 20 ayarın %30.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.080R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MACDYON · yön dönüşü (1s eşdeğeri) · SABIT_2R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2011-12-11 → 2015-05-07 | 22 | %59.1 | +0.548R |
| 2015-05-29 → 2019-07-22 | 22 | %54.5 | +0.332R |
| 2019-09-05 → 2023-08-08 | 22 | %45.5 | +0.113R |
| 2023-09-27 → 2026-05-18 | 22 | %31.8 | -0.275R |

Maksimum düşüş: IS 6.54R · OOS 10.28R

### İlk 15 ayar (1d, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | OSC · Stoch · dinamik · filtresiz + MACD yön | SABIT_1R | +0.068R (47) | +0.021R (35) | %60.0 |
| 2 | DONCH · Donchian 55 · EMA200 trend | TP0.5>BE_3R | +0.099R (57) | +0.181R (26) | %19.2 |
| 3 | MACDYON · yön dönüşü (1s eşdeğeri) | TP0.5>BE_3R | -0.007R (119) | -0.176R (57) | %14.0 |
| 4 | DONCH · Donchian 55 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.038R (57) | +0.242R (26) | %65.4 |
| 5 | MACDYON · yön dönüşü (1s eşdeğeri) | SABIT_2R | -0.011R (119) | -0.038R (57) | %40.4 |
| 6 | DONCH · Donchian 55 · filtresiz | TP0.5>BE_3R | +0.013R (66) | +0.131R (27) | %18.5 |
| 7 | OSC · Stoch · sabit · filtresiz + MACD yön | SABIT_1R | -0.018R (54) | -0.145R (35) | %51.4 |
| 8 | MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | SABIT_4R | +0.044R (152) | -0.378R (70) | %18.6 |
| 9 | DONCH · Donchian 20 · filtresiz | SABIT_1R | -0.113R (126) | -0.193R (49) | %49.0 |
| 10 | MACDYON · yön dönüşü (1s eşdeğeri) | SABIT_1R | -0.108R (119) | -0.197R (57) | %49.1 |
| 11 | MACDYON · yön + histogram dönüşü (bar) | SABIT_1R | -0.111R (119) | -0.033R (81) | %56.8 |
| 12 | RSI2 · RSI(2) 10/90 · filtresiz | SABIT_1R | -0.181R (312) | -0.361R (122) | %41.0 |
| 13 | DONCH · Donchian 55 · filtresiz | SABIT_1.5R | +0.007R (66) | +0.093R (27) | %51.9 |
| 14 | DONCH · Donchian 55 · filtresiz | GENIS_%50@1R>BE_3R | -0.026R (66) | +0.181R (27) | %63.0 |
| 15 | MACDYON · yön dönüşü (1s eşdeğeri) | SABIT_2.5R | -0.003R (119) | -0.046R (57) | %35.1 |

## ETH

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 70,081 | 2024-10-07 → 2026-03-02 | 2026-03-02 → 2026-10-07 | 0.311R | çalıştı |
| 30m | 35,041 | 2024-10-07 → 2026-03-02 | 2026-03-02 → 2026-10-07 | 0.212R | çalıştı |
| 1h | 79,995 | 2017-08-17 → 2024-01-11 | 2024-01-11 → 2026-10-07 | 0.125R | çalıştı |
| 4h | 20,016 | 2017-08-17 → 2024-01-10 | 2024-01-11 → 2026-10-07 | 0.059R | çalıştı |
| 1d | 3,339 | 2017-08-17 → 2024-01-09 | 2024-01-10 → 2026-10-07 | 0.021R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MACDYON** | 1d | iki yön | yön + histogram dönüşü (1s eşdeğeri) | SABIT_4R | +0.643R (90) | +0.592R (39) | +0.538R | %33.3 | 1.84 | 0.059 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.253R (962) | +0.071R (419) | +0.011R | %27.0 | 1.10 | 0.272 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 4h | iki yön | RSI(2) 10/90 · EMA200 trend + MACD yön | IZ_SUREN_2.5ATR | +0.401R (352) | +0.012R (178) | +0.005R | %28.7 | 1.02 | 0.470 | ⚠️ Pozitif, anlamsız |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi + MACD yön 1s | IZ_SUREN_2.5ATR | +0.571R (253) | -0.048R (138) | -0.061R | %23.2 | 0.94 | 0.594 | ❌ OOS'ta tutmadı |
| **OSC** | 30m | SHORT | Stoch · dinamik · hacim şoku+volatilite şoku + MACD yön 1s | IZ_SUREN_2.5ATR | +0.921R (90) | -0.071R (30) | +0.226R | %26.7 | 0.92 | 0.570 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | LONG | Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1.5>BE_4R | +1.145R (77) | -0.189R (48) | -0.136R | %12.5 | 0.72 | 0.790 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · hacim şoku | TP1.5>BE_4R | +0.781R (65) | -0.267R (24) | -0.194R | %12.5 | 0.65 | 0.786 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_4R | +0.220R | %75.0 | %26.6 | -0.035R | %23.3 | 263 |
| SABIT_3R | +0.210R | %80.0 | %32.6 | -0.059R | %26.5 | 263 |
| TP1.5>BE_4R | +0.205R | %80.0 | %20.8 | -0.004R | %18.2 | 263 |
| IZ_SUREN_2.5ATR | +0.177R | %65.0 | %31.0 | +0.076R | %28.0 | 263 |
| SABIT_2.5R | +0.135R | %80.0 | %35.1 | -0.068R | %29.4 | 263 |
| SABIT_1.5R | +0.098R | %73.7 | %47.3 | -0.074R | %40.4 | 263 |
| %50@1R>BE_IZ | +0.081R | %65.0 | %52.3 | -0.065R | %48.2 | 263 |
| GENIS_%50@1R>BE_3R | +0.080R | %70.0 | %55.5 | -0.054R | %48.1 | 263 |
| SABIT_2R | +0.059R | %60.0 | %38.2 | -0.054R | %34.4 | 263 |
| %50@1R>BE_4R | +0.053R | %75.0 | %52.9 | -0.100R | %48.2 | 263 |
| TP1>BE_3R | +0.042R | %60.0 | %20.5 | -0.087R | %17.4 | 263 |
| TP1>BE_3R_ERKEN | +0.026R | %55.0 | %19.2 | -0.086R | %16.7 | 263 |
| TP0.5>BE_3R | +0.020R | %55.0 | %15.2 | -0.081R | %11.8 | 263 |
| %50@1R>BE_3R | +0.009R | %55.0 | %52.1 | -0.105R | %48.2 | 263 |
| %50@1R>BE_2R | +0.005R | %55.0 | %52.1 | -0.107R | %48.2 | 263 |
| TP1>BE_2R | -0.021R | %45.0 | %28.1 | -0.094R | %25.4 | 263 |
| SABIT_1R | -0.022R | %55.0 | %53.0 | -0.116R | %48.2 | 263 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %75.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi +0.208R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s · TP1.5>BE_4R · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2017-10-13 → 2020-05-13 | 31 | %48.4 | +1.536R |
| 2020-05-17 → 2022-08-08 | 31 | %25.8 | +0.504R |
| 2022-08-10 → 2024-12-16 | 31 | %38.7 | +1.042R |
| 2025-03-24 → 2026-09-29 | 32 | %6.2 | -0.512R |

Maksimum düşüş: IS 4.50R · OOS 23.46R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1.5>BE_4R | +0.814R (141) | -0.086R (69) | %14.5 |
| 2 | DONCH · Donchian 55 · sıkışma sonrası + MACD yön 1s | TP1.5>BE_4R | +0.867R (82) | +0.372R (39) | %23.1 |
| 3 | DONCH · Donchian 20 · hacim şoku + MACD yön | TP1.5>BE_4R | +0.738R (139) | +0.354R (61) | %23.0 |
| 4 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | SABIT_4R | +0.753R (141) | -0.084R (69) | %20.3 |
| 5 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1>BE_3R_ERKEN | +0.611R (141) | -0.053R (69) | %17.4 |
| 6 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | TP1>BE_3R | +0.607R (141) | -0.053R (69) | %17.4 |
| 7 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1.5>BE_4R | +0.684R (136) | +0.228R (64) | %23.4 |
| 8 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1>BE_3R_ERKEN | +0.602R (136) | +0.161R (64) | %26.6 |
| 9 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1>BE_3R | +0.599R (136) | +0.155R (64) | %26.6 |
| 10 | DONCH · Donchian 55 · sıkışma sonrası + MACD yön 1s | TP1>BE_3R_ERKEN | +0.680R (82) | +0.094R (39) | %20.5 |
| 11 | DONCH · Donchian 55 · sıkışma sonrası + MACD yön 1s | TP1>BE_3R | +0.678R (82) | +0.094R (39) | %20.5 |
| 12 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön 1s | IZ_SUREN_2.5ATR | +0.756R (141) | -0.188R (69) | %26.1 |
| 13 | DONCH · Donchian 55 · sıkışma sonrası | TP1.5>BE_4R | +0.652R (139) | +0.485R (70) | %27.1 |
| 14 | DONCH · Donchian 20 · hacim şoku + MACD yön 1s | SABIT_4R | +0.647R (158) | +0.495R (73) | %31.5 |
| 15 | DONCH · Donchian 20 · hacim şoku + MACD yön | SABIT_4R | +0.667R (139) | +0.705R (61) | %36.1 |

## BTC

Veri: 5m tabanı `binance` · 1h tabanı `binance`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 70,081 | 2024-10-07 → 2026-03-02 | 2026-03-02 → 2026-10-07 | 0.484R | çalıştı |
| 30m | 35,041 | 2024-10-07 → 2026-03-02 | 2026-03-02 → 2026-10-07 | 0.326R | çalıştı |
| 1h | 79,991 | 2017-08-17 → 2024-01-11 | 2024-01-11 → 2026-10-07 | 0.166R | çalıştı |
| 4h | 20,016 | 2017-08-17 → 2024-01-10 | 2024-01-11 → 2026-10-07 | 0.080R | çalıştı |
| 1d | 3,339 | 2017-08-17 → 2024-01-09 | 2024-01-10 → 2026-10-07 | 0.028R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MACDYON** | 1d | LONG | yön + RSI(2) aşırı (1s eşdeğeri) | SABIT_4R | +0.924R (54) | +0.568R (21) | +0.600R | %33.3 | 1.80 | 0.137 | ⚠️ Pozitif, anlamsız |
| **RSI2** | 1d | LONG | RSI(2) 10/90 · filtresiz + MACD yön 1s | SABIT_4R | +0.904R (52) | +0.484R (19) | +0.516R | %31.6 | 1.66 | 0.185 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 4h | SHORT | Donchian 20 · hacim şoku + MACD yön | IZ_SUREN_2.5ATR | +1.168R (58) | +0.185R (32) | +0.351R | %37.5 | 1.30 | 0.310 | ⚠️ Pozitif, anlamsız |
| **META** | 4h | LONG | gradient boosting · tüm adaylar · üst %35 | IZ_SUREN_2.5ATR | +0.269R (991) | +0.134R (502) | +0.141R | %26.9 | 1.18 | 0.110 | ⚠️ Pozitif, anlamsız |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku + MACD yön | GENIS_%50@1R>BE_3R | +0.308R (108) | -0.102R (18) | +0.030R | %66.7 | 0.75 | 0.688 | ❌ OOS'ta tutmadı |
| **MA** | 4h | iki yön | EMA 9/21 kesişimi + MACD yön 1s | IZ_SUREN_2.5ATR | +0.542R (250) | -0.173R (117) | -0.087R | %22.2 | 0.78 | 0.823 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | LONG | Stoch · sabit · onay mumu + MACD yön | TP1.5>BE_4R | +0.445R (115) | -0.461R (71) | -0.430R | %9.9 | 0.45 | 0.996 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.103R | %10.0 | %48.3 | -0.086R | %49.0 | 276 |
| IZ_SUREN_2.5ATR | -0.123R | %20.0 | %23.4 | -0.077R | %25.6 | 276 |
| %50@1R>BE_4R | -0.155R | %10.0 | %48.1 | -0.194R | %45.3 | 276 |
| %50@1R>BE_IZ | -0.157R | %15.0 | %47.9 | -0.167R | %45.3 | 276 |
| TP1>BE_3R_ERKEN | -0.160R | %10.0 | %15.9 | -0.168R | %16.1 | 276 |
| TP1>BE_3R | -0.162R | %10.0 | %15.9 | -0.171R | %16.8 | 276 |
| %50@1R>BE_3R | -0.165R | %10.0 | %48.5 | -0.195R | %45.3 | 276 |
| TP1.5>BE_4R | -0.172R | %15.0 | %14.7 | -0.174R | %15.0 | 276 |
| TP0.5>BE_3R | -0.174R | %5.0 | %10.9 | -0.165R | %11.1 | 276 |
| SABIT_1R | -0.175R | %5.0 | %47.2 | -0.212R | %45.3 | 276 |
| %50@1R>BE_2R | -0.180R | %10.0 | %47.6 | -0.199R | %45.3 | 276 |
| TP1>BE_2R | -0.182R | %10.0 | %23.2 | -0.183R | %24.3 | 276 |
| SABIT_1.5R | -0.187R | %15.0 | %37.5 | -0.191R | %37.2 | 276 |
| SABIT_2R | -0.193R | %15.0 | %31.3 | -0.182R | %31.5 | 276 |
| SABIT_2.5R | -0.199R | %10.0 | %26.8 | -0.164R | %27.7 | 276 |
| SABIT_3R | -0.229R | %20.0 | %22.9 | -0.213R | %23.3 | 276 |
| SABIT_4R | -0.257R | %20.0 | %18.0 | -0.248R | %18.8 | 276 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %30.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.093R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 20 · hacim şoku + MACD yön · IZ_SUREN_2.5ATR · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2018-05-12 → 2019-09-23 | 22 | %40.9 | +0.970R |
| 2019-09-30 → 2022-02-17 | 23 | %39.1 | +0.613R |
| 2022-02-24 → 2024-09-30 | 22 | %45.5 | +1.460R |
| 2024-10-10 → 2026-06-30 | 23 | %39.1 | +0.266R |

Maksimum düşüş: IS 4.89R · OOS 7.13R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | IZ_SUREN_2.5ATR | +0.809R (149) | +0.358R (58) | %32.8 |
| 2 | DONCH · Donchian 20 · sıkışma sonrası | IZ_SUREN_2.5ATR | +0.576R (307) | -0.067R (132) | %24.2 |
| 3 | DONCH · Donchian 20 · EMA200 trend | IZ_SUREN_2.5ATR | +0.513R (371) | -0.111R (157) | %23.6 |
| 4 | DONCH · Donchian 20 · hacim şoku | IZ_SUREN_2.5ATR | +0.522R (266) | -0.223R (125) | %21.6 |
| 5 | DONCH · Donchian 20 · hacim şoku + MACD yön 1s | TP1.5>BE_4R | +0.542R (143) | -0.254R (70) | %12.9 |
| 6 | DONCH · Donchian 20 · hacim şoku + MACD yön 1s | IZ_SUREN_2.5ATR | +0.646R (143) | -0.309R (70) | %21.4 |
| 7 | DONCH · Donchian 55 · hacim şoku | IZ_SUREN_2.5ATR | +0.578R (189) | -0.381R (95) | %16.8 |
| 8 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1.5>BE_4R | +0.511R (149) | +0.215R (58) | %20.7 |
| 9 | MA · EMA 9/21 kesişimi + MACD yön 1s | IZ_SUREN_2.5ATR | +0.542R (250) | -0.173R (117) | %22.2 |
| 10 | DONCH · Donchian 55 · hacim şoku + MACD yön 1s | %50@1R>BE_IZ | +0.439R (113) | -0.274R (59) | %42.4 |
| 11 | DONCH · Donchian 20 · filtresiz + MACD yön | IZ_SUREN_2.5ATR | +0.550R (228) | +0.235R (96) | %31.2 |
| 12 | DONCH · Donchian 20 · sıkışma sonrası | TP1.5>BE_4R | +0.366R (307) | -0.129R (132) | %14.4 |
| 13 | DONCH · Donchian 20 · hacim şoku | TP1.5>BE_4R | +0.384R (266) | -0.260R (125) | %12.8 |
| 14 | DONCH · Donchian 55 · hacim şoku + MACD yön 1s | IZ_SUREN_2.5ATR | +0.675R (113) | -0.393R (59) | %16.9 |
| 15 | DONCH · Donchian 20 · sıkışma sonrası + MACD yön | TP1>BE_3R | +0.411R (149) | +0.171R (58) | %24.1 |

## XAG

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 47,264 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 0.506R | çalıştı |
| 30m | 23,635 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 0.358R | çalıştı |
| 1h | 89,215 | 2011-10-09 → 2022-03-30 | 2022-03-30 → 2026-10-07 | 0.346R | çalıştı |
| 4h | 23,997 | 2011-10-09 → 2022-04-07 | 2022-04-07 → 2026-10-07 | 0.177R | çalıştı |
| 1d | 4,665 | 2011-10-09 → 2022-04-07 | 2022-04-08 → 2026-10-07 | 0.075R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **META** | 1d | iki yön | gradient boosting · tüm adaylar · üst %35 | TP0.5>BE_3R | -0.071R (426) | +0.005R (215) | +0.076R | %13.0 | 1.01 | 0.474 | ⚠️ Pozitif, anlamsız |
| **MACDYON** | 1d | LONG | yön + EMA20'ye geri çekilme (1s eşdeğeri) | SABIT_1R | +0.134R (92) | -0.128R (35) | -0.072R | %48.6 | 0.77 | 0.774 | ❌ OOS'ta tutmadı |
| **DONCH** | 4h | iki yön | Donchian 20 · sıkışma sonrası + MACD yön 1s | IZ_SUREN_2.5ATR | +0.425R (166) | -0.175R (83) | -0.002R | %21.7 | 0.79 | 0.790 | ❌ OOS'ta tutmadı |
| **MA** | 1d | SHORT | zaman serisi momentumu 24 bar | TP1>BE_2R | +0.384R (75) | -0.242R (30) | -0.060R | %20.0 | 0.61 | 0.872 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | iki yön | WaveTrend · dinamik · volatilite şoku+onay mumu + MACD yön 1s | SABIT_4R | +0.715R (51) | -0.404R (25) | -0.154R | %16.0 | 0.60 | 0.864 | ❌ OOS'ta tutmadı |
| **RSI2** | 1d | SHORT | RSI(2) 10/90 · filtresiz | SABIT_2R | +0.006R (153) | -0.423R (68) | -0.141R | %23.5 | 0.51 | 0.997 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz + MACD yön 1s | IZ_SUREN_2.5ATR | +0.445R (114) | -0.563R (34) | -0.386R | %14.7 | 0.40 | 0.986 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1d) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| TP0.5>BE_3R | +0.011R | %55.0 | %14.5 | -0.012R | %13.6 | 42 |
| TP1.5>BE_4R | -0.004R | %35.0 | %18.8 | -0.022R | %18.6 | 42 |
| TP1>BE_3R_ERKEN | -0.009R | %40.0 | %19.5 | -0.018R | %19.2 | 42 |
| TP1>BE_3R | -0.019R | %35.0 | %20.6 | -0.020R | %20.3 | 42 |
| GENIS_%50@1R>BE_3R | -0.035R | %35.0 | %54.3 | -0.081R | %51.2 | 42 |
| TP1>BE_2R | -0.051R | %35.0 | %28.5 | -0.069R | %27.3 | 42 |
| SABIT_4R | -0.051R | %35.0 | %23.1 | -0.076R | %22.8 | 42 |
| %50@1R>BE_3R | -0.068R | %25.0 | %49.8 | -0.073R | %50.4 | 42 |
| SABIT_2R | -0.078R | %30.0 | %35.0 | -0.078R | %35.1 | 42 |
| %50@1R>BE_4R | -0.080R | %15.0 | %49.5 | -0.077R | %50.4 | 42 |
| %50@1R>BE_2R | -0.084R | %15.0 | %49.5 | -0.090R | %50.4 | 42 |
| SABIT_3R | -0.089R | %25.0 | %26.6 | -0.042R | %27.9 | 42 |
| SABIT_1R | -0.097R | %10.0 | %50.2 | -0.094R | %50.4 | 42 |
| %50@1R>BE_IZ | -0.103R | %15.0 | %50.3 | -0.129R | %50.4 | 42 |
| SABIT_1.5R | -0.105R | %15.0 | %40.4 | -0.098R | %40.8 | 42 |
| SABIT_2.5R | -0.108R | %25.0 | %29.5 | -0.082R | %30.4 | 42 |
| IZ_SUREN_2.5ATR | -0.123R | %15.0 | %27.4 | -0.072R | %28.3 | 42 |

**Sağlamlık (1d):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.098R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · zaman serisi momentumu 24 bar · TP1>BE_2R · SHORT

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2011-11-21 → 2015-06-04 | 26 | %57.7 | +0.675R |
| 2015-08-26 → 2019-04-02 | 26 | %38.5 | +0.252R |
| 2019-04-28 → 2022-08-24 | 26 | %46.2 | +0.283R |
| 2022-09-23 → 2026-07-23 | 27 | %14.8 | -0.366R |

Maksimum düşüş: IS 4.52R · OOS 12.29R

### İlk 15 ayar (1d, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | MA · EMA 9/21 kesişimi + MACD yön 1s | GENIS_%50@1R>BE_3R | +0.195R (82) | -0.123R (38) | %50.0 |
| 2 | MA · EMA 9/21 kesişimi + MACD yön 1s | SABIT_1R | +0.138R (82) | -0.088R (38) | %50.0 |
| 3 | MA · EMA 9/21 kesişimi + MACD yön 1s | %50@1R>BE_3R | +0.163R (82) | -0.103R (38) | %50.0 |
| 4 | MA · EMA 9/21 kesişimi + MACD yön 1s | SABIT_3R | +0.328R (82) | -0.102R (38) | %26.3 |
| 5 | MA · EMA 9/21 kesişimi + MACD yön 1s | TP1>BE_3R | +0.248R (82) | -0.076R (38) | %18.4 |
| 6 | MA · EMA 9/21 kesişimi + MACD yön 1s | %50@1R>BE_2R | +0.125R (82) | -0.035R (38) | %50.0 |
| 7 | MA · EMA 9/21 kesişimi | TP1>BE_2R | +0.119R (130) | -0.065R (65) | %26.2 |
| 8 | MA · EMA 9/21 kesişimi + MACD yön 1s | TP1.5>BE_4R | +0.337R (82) | -0.151R (38) | %15.8 |
| 9 | MA · EMA 9/21 kesişimi | %50@1R>BE_2R | +0.077R (130) | -0.065R (65) | %52.3 |
| 10 | MA · EMA 9/21 kesişimi + MACD yön 1s | %50@1R>BE_4R | +0.152R (82) | -0.164R (38) | %50.0 |
| 11 | MA · EMA 9/21 kesişimi | SABIT_1R | +0.056R (130) | -0.051R (65) | %52.3 |
| 12 | MA · EMA 9/21 kesişimi | TP1.5>BE_4R | +0.222R (130) | -0.154R (65) | %15.4 |
| 13 | MA · EMA 9/21 kesişimi | TP1>BE_3R | +0.145R (130) | -0.147R (65) | %15.4 |
| 14 | MACDYON · yön + hızlı MACD(12,26,9) kesişimi (bar) | TP1.5>BE_4R | +0.346R (76) | -0.101R (51) | %15.7 |
| 15 | MA · EMA 9/21 kesişimi | GENIS_%50@1R>BE_3R | +0.073R (130) | -0.125R (65) | %49.2 |

## NQ

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 45,596 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 1.074R | çalıştı |
| 30m | 23,051 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 0.739R | çalıştı |
| 1h | 74,987 | 2012-01-19 → 2022-12-12 | 2022-12-12 → 2026-10-07 | 0.538R | çalıştı |
| 4h | 21,272 | 2012-01-19 → 2022-10-10 | 2022-10-10 → 2026-10-07 | 0.282R | çalıştı |
| 1d | 4,301 | 2012-01-19 → 2022-08-15 | 2022-08-16 → 2026-10-07 | 0.113R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MACDYON** | 1d | LONG | yön + EMA20'ye geri çekilme (bar) | GENIS_%50@1R>BE_3R | +0.340R (70) | +0.171R (40) | +0.224R | %62.5 | 1.46 | 0.157 | ⚠️ Pozitif, anlamsız |
| **META** | 1d | LONG | gradient boosting · tüm adaylar · üst %35 | TP1>BE_3R | +0.160R (253) | +0.015R (166) | +0.072R | %23.5 | 1.02 | 0.451 | ⚠️ Pozitif, anlamsız |
| **DONCH** | 1d | LONG | Donchian 20 · filtresiz + MACD yön 1s | GENIS_%50@1R>BE_3R | +0.083R (40) | -0.030R (16) | +0.023R | %56.2 | 0.94 | 0.542 | ❌ OOS'ta tutmadı |
| **RSI2** | 1d | LONG | RSI(2) 10/90 · EMA200 trend | GENIS_%50@1R>BE_3R | +0.245R (92) | -0.165R (42) | -0.111R | %52.4 | 0.70 | 0.843 | ❌ OOS'ta tutmadı |
| **SQZ** | 4h | iki yön | BB-Keltner sıkışma çözülmesi · filtresiz | GENIS_%50@1R>BE_3R | -0.184R (74) | -0.389R (35) | -0.147R | %42.9 | 0.45 | 0.984 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | SHORT | Stoch · sabit · volatilite şoku + MACD yön 1s | TP0.5>BE_3R | +0.485R (51) | -0.583R (33) | -0.270R | %3.0 | 0.13 | 1.000 | ❌ OOS'ta tutmadı |
| **MA** | 4h | LONG | EMA 20/50 kesişimi + MACD yön | IZ_SUREN_2.5ATR | +1.030R (61) | -0.628R (36) | -0.403R | %16.7 | 0.37 | 0.996 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (4h) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| GENIS_%50@1R>BE_3R | -0.144R | %25.0 | %52.6 | -0.175R | %51.5 | 249 |
| TP0.5>BE_3R | -0.177R | %5.0 | %15.7 | -0.205R | %15.0 | 249 |
| SABIT_4R | -0.206R | %25.0 | %22.8 | -0.153R | %23.8 | 249 |
| TP1.5>BE_4R | -0.222R | %10.0 | %16.5 | -0.225R | %16.8 | 249 |
| SABIT_3R | -0.237R | %10.0 | %26.8 | -0.139R | %29.4 | 249 |
| SABIT_1.5R | -0.244R | %0.0 | %41.7 | -0.243R | %41.8 | 249 |
| SABIT_1R | -0.284R | %0.0 | %49.5 | -0.290R | %49.5 | 249 |
| SABIT_2R | -0.284R | %0.0 | %33.3 | -0.237R | %35.3 | 249 |
| TP1>BE_2R | -0.289R | %0.0 | %24.9 | -0.264R | %26.4 | 249 |
| SABIT_2.5R | -0.291R | %0.0 | %28.7 | -0.227R | %30.8 | 249 |
| %50@1R>BE_IZ | -0.303R | %0.0 | %47.6 | -0.296R | %48.4 | 249 |
| TP1>BE_3R_ERKEN | -0.305R | %0.0 | %15.2 | -0.252R | %17.3 | 249 |
| TP1>BE_3R | -0.307R | %0.0 | %16.7 | -0.234R | %18.9 | 249 |
| %50@1R>BE_4R | -0.307R | %0.0 | %47.5 | -0.259R | %47.5 | 249 |
| %50@1R>BE_2R | -0.318R | %0.0 | %47.2 | -0.281R | %48.5 | 249 |
| %50@1R>BE_3R | -0.319R | %0.0 | %47.0 | -0.271R | %48.3 | 249 |
| IZ_SUREN_2.5ATR | -0.379R | %0.0 | %24.7 | -0.249R | %25.3 | 249 |

**Sağlamlık (4h):** IS'te en iyi 20 ayarın %5.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.302R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — MA · EMA 20/50 kesişimi + MACD yön · IZ_SUREN_2.5ATR · LONG

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2013-08-23 → 2017-04-20 | 24 | %45.8 | +0.600R |
| 2017-05-22 → 2020-06-30 | 24 | %54.2 | +1.784R |
| 2020-07-30 → 2023-09-11 | 24 | %29.2 | -0.002R |
| 2023-09-13 → 2026-08-28 | 25 | %16.0 | -0.677R |

Maksimum düşüş: IS 5.34R · OOS 22.69R

### İlk 15 ayar (4h, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | MA · EMA 20/50 kesişimi + MACD yön | TP0.5>BE_3R | +0.342R (97) | -0.244R (58) | %13.8 |
| 2 | MA · EMA 20/50 kesişimi + MACD yön | IZ_SUREN_2.5ATR | +0.561R (97) | -0.613R (58) | %19.0 |
| 3 | MA · EMA 20/50 kesişimi + MACD yön | TP1>BE_3R | +0.272R (97) | -0.334R (58) | %13.8 |
| 4 | MA · EMA 20/50 kesişimi + MACD yön | SABIT_3R | +0.331R (97) | -0.538R (58) | %19.0 |
| 5 | MA · EMA 20/50 kesişimi + MACD yön | SABIT_2.5R | +0.285R (97) | -0.506R (58) | %22.4 |
| 6 | MA · EMA 20/50 kesişimi + MACD yön | TP1>BE_3R_ERKEN | +0.245R (97) | -0.321R (58) | %12.1 |
| 7 | MA · EMA 20/50 kesişimi + MACD yön | %50@1R>BE_IZ | +0.188R (97) | -0.308R (58) | %53.4 |
| 8 | MA · EMA 20/50 kesişimi + MACD yön | %50@1R>BE_3R | +0.149R (97) | -0.273R (58) | %51.7 |
| 9 | MA · EMA 20/50 kesişimi + MACD yön | %50@1R>BE_4R | +0.154R (97) | -0.279R (58) | %51.7 |
| 10 | MA · EMA 20/50 kesişimi + MACD yön | TP1.5>BE_4R | +0.302R (97) | -0.448R (58) | %12.1 |
| 11 | OSC · Stoch · sabit · EMA200 trend + MACD yön 1s | TP0.5>BE_3R | +0.088R (227) | -0.189R (100) | %14.0 |
| 12 | MA · EMA 20/50 kesişimi + MACD yön | %50@1R>BE_2R | +0.084R (97) | -0.229R (58) | %53.4 |
| 13 | MA · EMA 20/50 kesişimi + MACD yön | SABIT_1R | +0.060R (97) | -0.190R (58) | %53.4 |
| 14 | MA · EMA 20/50 kesişimi + MACD yön | TP1>BE_2R | +0.125R (97) | -0.255R (58) | %24.1 |
| 15 | MA · EMA 20/50 kesişimi | TP0.5>BE_3R | +0.053R (247) | -0.250R (127) | %15.0 |

## SPX

Veri: 5m tabanı `dukascopy` · 1h tabanı `dukascopy`

| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |
|---|---|---|---|---|---|
| 15m | 45,602 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 1.557R | çalıştı |
| 30m | 23,055 | 2024-10-07 → 2026-03-04 | 2026-03-04 → 2026-10-07 | 1.069R | çalıştı |
| 1h | 75,630 | 2012-01-16 → 2022-11-30 | 2022-11-30 → 2026-10-07 | 0.710R | çalıştı |
| 4h | 21,521 | 2012-01-16 → 2022-09-22 | 2022-09-22 → 2026-10-07 | 0.371R | çalıştı |
| 1d | 4,313 | 2012-01-16 → 2022-08-11 | 2022-08-12 → 2026-10-07 | 0.148R | çalıştı |

### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)

| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **MA** | 1d | LONG | zaman serisi momentumu 24 bar | TP1>BE_2R | +0.025R (66) | +0.114R (27) | +0.270R | %37.0 | 1.22 | 0.325 | ⚠️ Pozitif, anlamsız |
| **META** | 1d | LONG | gradient boosting · tüm adaylar · üst %35 | SABIT_1R | -0.124R (258) | -0.075R (152) | +0.105R | %56.6 | 0.86 | 0.826 | ❌ OOS'ta tutmadı |
| **DONCH** | 1d | iki yön | Donchian 55 · filtresiz + MACD yön 1s | SABIT_1.5R | +0.177R (57) | -0.211R (20) | +0.022R | %45.0 | 0.70 | 0.775 | ❌ OOS'ta tutmadı |
| **MACDYON** | 1d | LONG | yön dönüşü (1s eşdeğeri) | TP1>BE_2R | +0.105R (69) | -0.231R (28) | -0.075R | %32.1 | 0.70 | 0.811 | ❌ OOS'ta tutmadı |
| **RSI2** | 4h | SHORT | RSI(2) 10/90 · EMA200 trend | TP1>BE_3R_ERKEN | -0.062R (173) | -0.334R (74) | +0.109R | %12.2 | 0.49 | 0.992 | ❌ OOS'ta tutmadı |
| **OSC** | 4h | SHORT | Stoch · sabit · EMA200 trend + MACD yön | TP0.5>BE_3R | +0.072R (69) | -0.469R (27) | -0.034R | %7.4 | 0.30 | 0.990 | ❌ OOS'ta tutmadı |
| **SQZ** | 1h | LONG | BB-Keltner sıkışma çözülmesi · hacim şoku | GENIS_%50@1R>BE_3R | -0.209R (52) | -0.831R (21) | -0.300R | %14.3 | 0.19 | 1.000 | ❌ OOS'ta tutmadı |

### Çıkış yöntemleri (1d) — girişten bağımsız etkisi

| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |
|---|---|---|---|---|---|---|
| SABIT_3R | -0.100R | %25.0 | %31.7 | -0.184R | %29.8 | 41 |
| TP1>BE_2R | -0.102R | %20.0 | %30.8 | -0.122R | %30.0 | 41 |
| SABIT_1R | -0.126R | %15.0 | %55.4 | -0.131R | %54.8 | 41 |
| SABIT_2.5R | -0.140R | %35.0 | %34.1 | -0.177R | %33.1 | 41 |
| %50@1R>BE_2R | -0.141R | %10.0 | %51.1 | -0.148R | %51.7 | 41 |
| TP1>BE_3R | -0.168R | %5.0 | %20.0 | -0.198R | %19.0 | 41 |
| SABIT_1.5R | -0.169R | %10.0 | %44.2 | -0.164R | %44.1 | 41 |
| SABIT_2R | -0.181R | %10.0 | %37.3 | -0.184R | %37.1 | 41 |
| TP1>BE_3R_ERKEN | -0.183R | %5.0 | %17.5 | -0.205R | %17.2 | 41 |
| TP0.5>BE_3R | -0.194R | %10.0 | %13.9 | -0.150R | %15.2 | 41 |
| TP1.5>BE_4R | -0.194R | %10.0 | %19.2 | -0.248R | %17.9 | 41 |
| GENIS_%50@1R>BE_3R | -0.195R | %5.0 | %48.4 | -0.193R | %48.0 | 41 |
| %50@1R>BE_3R | -0.204R | %5.0 | %46.5 | -0.209R | %46.8 | 41 |
| SABIT_4R | -0.205R | %5.0 | %25.0 | -0.282R | %23.4 | 41 |
| %50@1R>BE_4R | -0.221R | %5.0 | %43.4 | -0.243R | %43.1 | 41 |
| %50@1R>BE_IZ | -0.222R | %10.0 | %49.4 | -0.237R | %50.3 | 41 |
| IZ_SUREN_2.5ATR | -0.267R | %0.0 | %25.5 | -0.302R | %25.2 | 41 |

**Sağlamlık (1d):** IS'te en iyi 20 ayarın %15.0'i OOS'ta pozitif kaldı, ortalama OOS beklentisi -0.119R. (%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)

### Seçilen ayarın kararlılığı — DONCH · Donchian 55 · filtresiz + MACD yön 1s · SABIT_1.5R · iki yön

| Dönem | İşlem | İsabet | Beklenti |
|---|---|---|---|
| 2012-05-14 → 2015-02-13 | 19 | %52.6 | -0.040R |
| 2015-05-18 → 2018-10-10 | 19 | %52.6 | -0.019R |
| 2018-12-17 → 2022-08-10 | 19 | %73.7 | +0.591R |
| 2022-09-21 → 2026-08-04 | 20 | %45.0 | -0.211R |

Maksimum düşüş: IS 9.21R · OOS 5.75R

### İlk 15 ayar (1d, iki yön, IS sıralı)

| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |
|---|---|---|---|---|---|
| 1 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | SABIT_1.5R | +0.177R (57) | -0.211R (20) | %45.0 |
| 2 | DONCH · Donchian 55 · EMA200 trend + MACD yön 1s | SABIT_1.5R | +0.171R (52) | -0.335R (20) | %40.0 |
| 3 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | TP1>BE_2R | +0.135R (57) | -0.067R (20) | %35.0 |
| 4 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | SABIT_2R | +0.153R (57) | -0.006R (20) | %45.0 |
| 5 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | %50@1R>BE_2R | +0.029R (57) | -0.142R (20) | %50.0 |
| 6 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | TP1>BE_3R | +0.185R (57) | -0.206R (20) | %20.0 |
| 7 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | SABIT_1R | -0.002R (57) | -0.167R (20) | %55.0 |
| 8 | DONCH · Donchian 55 · filtresiz | SABIT_1.5R | +0.033R (68) | -0.220R (27) | %44.4 |
| 9 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | TP1>BE_3R_ERKEN | +0.167R (57) | -0.206R (20) | %20.0 |
| 10 | DONCH · Donchian 55 · EMA200 trend + MACD yön 1s | SABIT_1R | +0.001R (52) | -0.163R (20) | %55.0 |
| 11 | DONCH · Donchian 55 · filtresiz + MACD yön 1s | %50@1R>BE_3R | +0.027R (57) | -0.231R (20) | %45.0 |
| 12 | DONCH · Donchian 55 · EMA200 trend | SABIT_1.5R | +0.016R (63) | -0.311R (27) | %40.7 |
| 13 | DONCH · Donchian 55 · EMA200 trend + MACD yön 1s | SABIT_2R | +0.115R (52) | -0.153R (20) | %40.0 |
| 14 | DONCH · Donchian 55 · EMA200 trend + MACD yön 1s | TP1>BE_2R | +0.057R (52) | -0.162R (20) | %30.0 |
| 15 | DONCH · Donchian 55 · EMA200 trend + MACD yön 1s | %50@1R>BE_2R | -0.010R (52) | -0.187R (20) | %50.0 |

---
Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`
