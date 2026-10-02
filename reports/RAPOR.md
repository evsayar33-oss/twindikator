# ATVS Lab Raporu — 2026-10-02 17:03 UTC

**Yöntem.** Her varlık × zaman dilimi için 224 kombinasyon (7 osilatör alt kümesi × 2 eşik tipi × 16 filtre kümesi), LONG ve SHORT ayrı. Giriş: sinyal barından sonraki açılış · Çıkış: TP 1.5 ATR / SL 1.0 ATR / 24 bar · maliyet dahil · aynı barda TP+SL = zarar. Başabaş isabet ≈ %40.

**Seçim yalnızca ilk %70 veride (IS)** yapılır; tabloda asıl ölçü **son %30 (OOS)** sonucudur. Taban = aynı dönemde her bara rastgele girişin isabeti (piyasanın kendi eğilimi). p = OOS isabetinin tabandan şans eseri yüksek çıkma olasılığı. Varlık başına ~3,360 test yapıldığı için IS rakamları iyimserdir; güvenilecek sütun OOS'tur.

## Özet

| Varlık | ZD | Yön | Kombinasyon | IS isabet (n) | **OOS isabet (n)** | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|---|
| **XAU** | 5m | iki yön | RSI+Stoch · sabit 80/20 · Hacim şoku | %59.0 (61) | **%42.9** (28) | %32.4 | -0.10R | 0.164 | ❌ OOS'ta tutmadı |
| **XAG** | 5m | iki yön | RSI+Stoch+WaveTrend · sabit 80/20 · Hacim şoku + Volatilite şoku | %49.3 (75) | **%44.4** (36) | %31.9 | -0.16R | 0.075 | ❌ OOS'ta tutmadı |
| **BTC** | 15m | iki yön | WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %56.7 (60) | **%40.0** (25) | %39.4 | -0.38R | 0.556 | ❌ OOS'ta tutmadı |
| **ETH** | 15m | iki yön | WaveTrend · dinamik · Volatilite şoku + Trend (EMA200) + Onay mumu | %55.0 (80) | **%26.3** (38) | %39.7 | -0.64R | 0.968 | ❌ OOS'ta tutmadı |
| **NQ** | 15m | iki yön | Stoch · dinamik · Hacim şoku + Onay mumu | %54.7 (64) | **%43.5** (23) | %32.1 | -0.08R | 0.174 | ❌ OOS'ta tutmadı |
| **SPX** | 5m | yalnız LONG | RSI+Stoch+WaveTrend · dinamik · Hacim şoku + Volatilite şoku | %47.4 (152) | **%36.8** (68) | %31.9 | -0.50R | 0.231 | ❌ OOS'ta tutmadı |

## XAU

Veri: 5m tabanı `dukascopy`, 1h tabanı `dukascopy`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m ◀ | 39,456 | RSI+Stoch · sabit 80/20 · Hacim şoku | %59.0 (61) | %42.9 (28) | %32.4 | -0.10R | 0.164 | ❌ OOS'ta tutmadı |
| 15m | 13,152 | WaveTrend · sabit 80/20 · filtre yok | %49.4 (168) | %34.8 (69) | %32.4 | -0.24R | 0.387 | ❌ OOS'ta tutmadı |
| 30m | 6,576 | Stoch+WaveTrend · dinamik · filtre yok | %50.0 (86) | %30.2 (43) | %34.1 | -0.31R | 0.755 | ❌ OOS'ta tutmadı |
| 1h | 51,823 | RSI+Stoch+WaveTrend · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) | %49.4 (83) | %36.0 (25) | %30.3 | -0.25R | 0.342 | ❌ OOS'ta tutmadı |
| 4h | 12,956 | RSI · dinamik · Onay mumu | %43.7 (284) | %41.1 (141) | %41.0 | -0.02R | 0.517 | ❌ OOS'ta tutmadı |

### Yön ayrımı (5m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | RSI+Stoch · sabit 80/20 · Hacim şoku | %59.0 (61) | %42.9 (28) | %32.4 | -0.10R | 0.164 |
| yalnız LONG | Stoch · sabit 80/20 · Volatilite şoku | %41.7 (228) | %41.9 (93) | %31.4 | -0.11R | 0.019 |
| yalnız SHORT | RSI+Stoch · sabit 80/20 · filtre yok | %54.5 (66) | %47.6 (21) | %33.4 | -0.04R | 0.126 |

### Tekli göstergeler, filtresiz (5m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %38.7 (729) | %38.9 (334) | %32.4 | -0.37R |
| RSI | sabit 80/20 | %47.3 (112) | %41.9 (43) | %32.5 | -0.20R |
| Stoch | dinamik | %36.6 (1039) | %38.5 (452) | %32.4 | -0.25R |
| Stoch | sabit 80/20 | %36.5 (1462) | %38.3 (658) | %32.3 | -0.25R |
| WaveTrend | dinamik | %35.9 (608) | %39.6 (265) | %32.4 | -0.21R |
| WaveTrend | sabit 80/20 | %37.5 (544) | %42.7 (232) | %32.3 | -0.14R |

### Bileşen katkısı (5m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +1.8 puan | 74 |
| Volatilite şoku | +0.4 puan | 76 |
| Trend (EMA200) | +1.0 puan | 54 |
| Onay mumu | +0.2 puan | 82 |
| Dinamik eşik (sabite göre) | -4.5 puan | 68 |

### Kararlılık — seçilen ayar (iki yön), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2024-12-18 → 2026-06-04 | 20 | %70.0 | %31.4 | +0.34R |
| 2026-06-04 → 2026-07-14 | 24 | %50.0 | %32.5 | +0.09R |
| 2026-07-14 → 2026-08-23 | 21 | %47.6 | %32.4 | +0.04R |
| 2026-08-23 → 2026-10-01 | 24 | %50.0 | %33.1 | +0.06R |

### İlk 10 kombinasyon (5m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | RSI+Stoch · sabit 80/20 · Hacim şoku | %59.0 (61) | %42.9 (28) | -0.10R |
| 2 | RSI+WaveTrend · sabit 80/20 · Hacim şoku + Onay mumu | %59.6 (52) | %50.0 (24) | +0.07R |
| 3 | RSI+Stoch+WaveTrend · sabit 80/20 · Hacim şoku | %58.9 (56) | %46.2 (26) | -0.02R |
| 4 | RSI+Stoch · sabit 80/20 · Hacim şoku + Onay mumu | %58.6 (58) | %42.9 (28) | -0.10R |
| 5 | RSI+WaveTrend · sabit 80/20 · Hacim şoku | %57.4 (54) | %48.0 (25) | +0.02R |
| 6 | RSI+Stoch+WaveTrend · sabit 80/20 · Hacim şoku + Onay mumu | %57.4 (54) | %46.2 (26) | -0.02R |
| 7 | RSI+Stoch · sabit 80/20 · filtre yok | %51.8 (110) | %39.5 (38) | -0.20R |
| 8 | RSI+Stoch · sabit 80/20 · Onay mumu | %51.9 (106) | %39.5 (38) | -0.20R |
| 9 | RSI · sabit 80/20 · Hacim şoku | %54.5 (55) | %46.2 (26) | -0.02R |
| 10 | RSI · sabit 80/20 · Hacim şoku + Onay mumu | %54.5 (55) | %46.2 (26) | -0.02R |

## XAG

Veri: 5m tabanı `dukascopy`, 1h tabanı `dukascopy`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m ◀ | 95,414 | RSI+Stoch+WaveTrend · sabit 80/20 · Hacim şoku + Volatilite şoku | %49.3 (75) | %44.4 (36) | %31.9 | -0.16R | 0.075 | ❌ OOS'ta tutmadı |
| 15m | 31,805 | WaveTrend · dinamik · Onay mumu | %43.0 (414) | %36.6 (164) | %32.3 | -0.34R | 0.136 | ❌ OOS'ta tutmadı |
| 30m | 15,903 | RSI · sabit 80/20 · filtre yok | %47.4 (78) | %38.6 (44) | %32.5 | -0.38R | 0.240 | ❌ OOS'ta tutmadı |
| 1h | 2,976 | Stoch · dinamik · Onay mumu | %45.5 (55) | %36.4 (22) | %27.6 | -0.14R | 0.247 | ❌ OOS'ta tutmadı |

### Yön ayrımı (5m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | RSI+Stoch+WaveTrend · sabit 80/20 · Hacim şoku + Volatilite şoku | %49.3 (75) | %44.4 (36) | %31.9 | -0.16R | 0.075 |
| yalnız LONG | RSI+Stoch+WaveTrend · sabit 80/20 · Volatilite şoku | %50.0 (66) | %50.0 (26) | %31.8 | -0.08R | 0.037 |
| yalnız SHORT | Stoch · dinamik · filtre yok | %39.2 (1224) | %36.9 (550) | %32.0 | -0.50R | 0.007 |

### Tekli göstergeler, filtresiz (5m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %40.7 (1754) | %38.4 (769) | %31.9 | -3473370.02R |
| RSI | sabit 80/20 | %42.2 (230) | %45.0 (109) | %31.9 | -0.33R |
| Stoch | dinamik | %39.7 (2410) | %39.7 (1069) | %31.9 | -0.45R |
| Stoch | sabit 80/20 | %38.7 (3509) | %37.5 (1521) | %31.9 | -0.51R |
| WaveTrend | dinamik | %37.4 (1412) | %39.4 (640) | %31.9 | -0.47R |
| WaveTrend | sabit 80/20 | %39.1 (1140) | %38.2 (532) | %31.9 | -0.50R |

### Bileşen katkısı (5m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +1.3 puan | 93 |
| Volatilite şoku | +0.2 puan | 93 |
| Trend (EMA200) | +1.1 puan | 77 |
| Onay mumu | +0.1 puan | 94 |
| Dinamik eşik (sabite göre) | -1.4 puan | 77 |

### Kararlılık — seçilen ayar (iki yön), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2024-10-02 → 2025-01-07 | 29 | %41.4 | %30.5 | -0.21R |
| 2025-01-07 → 2025-04-15 | 14 | %64.3 | %31.6 | +0.33R |
| 2025-04-15 → 2025-07-22 | 37 | %45.9 | %30.9 | -0.07R |
| 2025-07-22 → 2026-05-28 | 31 | %48.4 | %32.2 | -0.06R |

### İlk 10 kombinasyon (5m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | RSI+WaveTrend · dinamik · Hacim şoku + Trend (EMA200) | %49.5 (91) | %45.0 (40) | -0.33R |
| 2 | RSI+Stoch+WaveTrend · dinamik · Hacim şoku + Volatilite şoku | %45.5 (242) | %42.0 (112) | -0.27R |
| 3 | RSI+Stoch+WaveTrend · sabit 80/20 · filtre yok | %46.3 (175) | %48.8 (86) | -0.13R |
| 4 | Stoch+WaveTrend · sabit 80/20 · Onay mumu | %41.8 (1038) | %37.6 (466) | -0.49R |
| 5 | RSI · dinamik · Onay mumu | %41.1 (1715) | %38.6 (751) | -0.50R |
| 6 | RSI+Stoch · sabit 80/20 · filtre yok | %45.6 (195) | %50.5 (95) | -0.10R |
| 7 | Stoch+WaveTrend · sabit 80/20 · Volatilite şoku | %43.5 (414) | %36.8 (193) | -0.46R |
| 8 | Stoch · sabit 80/20 · Hacim şoku + Trend (EMA200) + Onay mumu | %45.5 (191) | %42.6 (101) | -0.31R |
| 9 | Stoch+WaveTrend · sabit 80/20 · Volatilite şoku + Onay mumu | %43.6 (360) | %36.1 (166) | -0.47R |
| 10 | Stoch · sabit 80/20 · Hacim şoku + Trend (EMA200) | %45.0 (218) | %41.4 (116) | -0.33R |

## BTC

Veri: 5m tabanı `binance`, 1h tabanı `binance`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m | 210,240 | Stoch · sabit 80/20 · Hacim şoku + Volatilite şoku | %40.1 (2500) | %39.3 (1068) | %37.3 | -0.60R | 0.086 | ❌ OOS'ta tutmadı |
| 15m ◀ | 70,081 | WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %56.7 (60) | %40.0 (25) | %39.4 | -0.38R | 0.556 | ❌ OOS'ta tutmadı |
| 30m | 35,041 | Stoch · sabit 80/20 · Volatilite şoku + Trend (EMA200) + Onay mumu | %52.2 (134) | %41.3 (63) | %40.0 | -0.24R | 0.469 | ❌ OOS'ta tutmadı |
| 1h | 52,564 | WaveTrend · dinamik · Hacim şoku + Trend (EMA200) + Onay mumu | %50.0 (74) | %48.1 (27) | %39.6 | +0.07R | 0.238 | ⚠️ Zayıf (anlamsız) |
| 4h | 13,147 | WaveTrend · sabit 80/20 · Hacim şoku + Volatilite şoku + Onay mumu | %54.0 (50) | %27.3 (22) | %39.9 | -0.38R | 0.923 | ❌ OOS'ta tutmadı |

### Yön ayrımı (15m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %56.7 (60) | %40.0 (25) | %39.4 | -0.38R | 0.556 |
| yalnız LONG | Stoch · sabit 80/20 · Onay mumu | %40.7 (1262) | %39.6 (571) | %38.7 | -0.35R | 0.353 |
| yalnız SHORT | Stoch · sabit 80/20 · Hacim şoku + Volatilite şoku + Trend (EMA200) + Onay mumu | %53.2 (77) | %38.9 (36) | %40.4 | -0.42R | 0.637 |

### Tekli göstergeler, filtresiz (15m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %37.2 (1479) | %41.8 (662) | %39.6 | -0.30R |
| RSI | sabit 80/20 | %39.5 (167) | %38.7 (75) | %39.6 | -0.28R |
| Stoch | dinamik | %38.5 (2600) | %41.9 (1118) | %39.5 | -0.32R |
| Stoch | sabit 80/20 | %40.2 (3180) | %40.5 (1372) | %39.6 | -0.35R |
| WaveTrend | dinamik | %40.7 (1279) | %39.9 (549) | %39.5 | -0.37R |
| WaveTrend | sabit 80/20 | %39.8 (1085) | %40.4 (436) | %39.6 | -0.34R |

### Bileşen katkısı (15m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +1.2 puan | 96 |
| Volatilite şoku | +1.8 puan | 96 |
| Trend (EMA200) | +2.3 puan | 80 |
| Onay mumu | +0.3 puan | 96 |
| Dinamik eşik (sabite göre) | -0.2 puan | 80 |

### Kararlılık — seçilen ayar (iki yön), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2024-10-02 → 2025-04-03 | 25 | %60.0 | %40.4 | +0.24R |
| 2025-04-03 → 2025-10-02 | 16 | %68.8 | %39.7 | +0.37R |
| 2025-10-02 → 2026-04-03 | 24 | %45.8 | %40.1 | -0.17R |
| 2026-04-03 → 2026-10-02 | 20 | %35.0 | %39.3 | -0.54R |

### İlk 10 kombinasyon (15m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %56.7 (60) | %40.0 (25) | -0.38R |
| 2 | Stoch+WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) + Onay mumu | %53.6 (56) | %44.4 (27) | -0.24R |
| 3 | WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) + Onay mumu | %53.8 (52) | %40.0 (20) | -0.36R |
| 4 | Stoch · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) + Onay mumu | %49.2 (120) | %47.4 (57) | -0.18R |
| 5 | Stoch · sabit 80/20 · Hacim şoku + Volatilite şoku + Trend (EMA200) + Onay mumu | %47.6 (164) | %39.7 (78) | -0.35R |
| 6 | Stoch · sabit 80/20 · Hacim şoku + Volatilite şoku + Trend (EMA200) | %46.5 (187) | %39.1 (87) | -0.36R |
| 7 | RSI+Stoch · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) + Onay mumu | %50.0 (80) | %46.5 (43) | -0.14R |
| 8 | Stoch · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) | %46.9 (143) | %47.0 (66) | -0.19R |
| 9 | Stoch+WaveTrend · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %50.8 (61) | %43.3 (30) | -0.28R |
| 10 | Stoch · sabit 80/20 · filtre yok | %40.2 (3180) | %40.5 (1372) | -0.35R |

## ETH

Veri: 5m tabanı `binance`, 1h tabanı `binance`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m | 210,240 | Stoch · dinamik · Onay mumu | %41.2 (6778) | %39.6 (2821) | %39.4 | -0.53R | 0.411 | ❌ OOS'ta tutmadı |
| 15m ◀ | 70,081 | WaveTrend · dinamik · Volatilite şoku + Trend (EMA200) + Onay mumu | %55.0 (80) | %26.3 (38) | %39.7 | -0.64R | 0.968 | ❌ OOS'ta tutmadı |
| 30m | 35,041 | RSI+WaveTrend · dinamik · Trend (EMA200) | %49.6 (125) | %41.1 (56) | %40.1 | -0.16R | 0.496 | ❌ OOS'ta tutmadı |
| 1h | 52,564 | WaveTrend · dinamik · Trend (EMA200) + Onay mumu | %44.6 (251) | %41.7 (103) | %40.0 | -0.05R | 0.393 | ❌ OOS'ta tutmadı |
| 4h | 13,147 | Stoch · dinamik · Hacim şoku + Trend (EMA200) | %52.5 (61) | %46.4 (28) | %40.1 | +0.07R | 0.311 | ⚠️ Zayıf (anlamsız) |

### Yön ayrımı (15m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | WaveTrend · dinamik · Volatilite şoku + Trend (EMA200) + Onay mumu | %55.0 (80) | %26.3 (38) | %39.7 | -0.64R | 0.968 |
| yalnız LONG | Stoch · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) | %47.5 (120) | %37.7 (53) | %39.8 | -0.25R | 0.670 |
| yalnız SHORT | Stoch · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %49.3 (144) | %46.9 (64) | %39.7 | -0.11R | 0.147 |

### Tekli göstergeler, filtresiz (15m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %40.2 (1489) | %41.5 (655) | %39.7 | -0.22R |
| RSI | sabit 80/20 | %35.6 (202) | %44.6 (83) | %39.7 | -0.07R |
| Stoch | dinamik | %40.0 (2512) | %41.6 (1112) | %39.7 | -0.23R |
| Stoch | sabit 80/20 | %40.3 (2938) | %39.7 (1231) | %39.7 | -0.28R |
| WaveTrend | dinamik | %40.9 (1287) | %38.9 (550) | %39.7 | -0.30R |
| WaveTrend | sabit 80/20 | %41.2 (1074) | %39.9 (421) | %39.7 | -0.25R |

### Bileşen katkısı (15m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +1.2 puan | 96 |
| Volatilite şoku | +0.3 puan | 96 |
| Trend (EMA200) | +0.8 puan | 80 |
| Onay mumu | +0.1 puan | 96 |
| Dinamik eşik (sabite göre) | +2.0 puan | 80 |

### Kararlılık — seçilen ayar (iki yön), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2024-10-02 → 2025-04-03 | 29 | %51.7 | %39.9 | +0.11R |
| 2025-04-03 → 2025-10-02 | 28 | %46.4 | %40.1 | -0.03R |
| 2025-10-02 → 2026-04-03 | 29 | %62.1 | %40.3 | +0.33R |
| 2026-04-03 → 2026-10-02 | 32 | %25.0 | %39.6 | -0.69R |

### İlk 10 kombinasyon (15m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | WaveTrend · dinamik · Volatilite şoku + Trend (EMA200) + Onay mumu | %55.0 (80) | %26.3 (38) | -0.64R |
| 2 | WaveTrend · dinamik · Hacim şoku + Trend (EMA200) + Onay mumu | %53.8 (80) | %40.0 (40) | -0.29R |
| 3 | WaveTrend · dinamik · Volatilite şoku + Onay mumu | %46.1 (343) | %39.1 (169) | -0.28R |
| 4 | WaveTrend · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) + Onay mumu | %53.4 (58) | %40.0 (25) | -0.28R |
| 5 | Stoch · dinamik · Hacim şoku + Volatilite şoku + Trend (EMA200) | %47.6 (187) | %42.9 (98) | -0.17R |
| 6 | WaveTrend · dinamik · Volatilite şoku + Trend (EMA200) | %50.0 (94) | %25.6 (43) | -0.67R |
| 7 | WaveTrend · dinamik · Hacim şoku + Volatilite şoku + Onay mumu | %45.6 (259) | %42.8 (138) | -0.17R |
| 8 | Stoch · sabit 80/20 · Hacim şoku + Volatilite şoku + Trend (EMA200) | %46.2 (210) | %49.5 (93) | +0.01R |
| 9 | WaveTrend · dinamik · Hacim şoku + Trend (EMA200) | %49.5 (93) | %37.8 (45) | -0.37R |
| 10 | WaveTrend · dinamik · Trend (EMA200) + Onay mumu | %44.7 (338) | %33.1 (142) | -0.47R |

## NQ

Veri: 5m tabanı `dukascopy`, 1h tabanı `yfinance:NQ=F (yedek, kısa geçmiş)`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m | 27,157 | Stoch+WaveTrend · sabit 80/20 · Volatilite şoku + Onay mumu | %48.0 (127) | %49.0 (49) | %29.6 | -0.11R | 0.002 | ❌ OOS'ta tutmadı |
| 15m ◀ | 9,053 | Stoch · dinamik · Hacim şoku + Onay mumu | %54.7 (64) | %43.5 (23) | %32.1 | -0.08R | 0.174 | ❌ OOS'ta tutmadı |
| 30m | 4,527 | RSI+Stoch+WaveTrend · dinamik · filtre yok | %52.8 (53) | %43.8 (16) | %32.6 | +0.02R | 0.247 | ⏳ OOS yetersiz |
| 1h | 13,703 | Stoch+WaveTrend · sabit 80/20 · Hacim şoku + Volatilite şoku | %52.2 (67) | %34.2 (38) | %39.9 | -0.20R | 0.813 | ❌ OOS'ta tutmadı |
| 4h | 3,712 | RSI · dinamik · filtre yok | %43.9 (82) | %41.0 (39) | %39.2 | -0.00R | 0.470 | ❌ OOS'ta tutmadı |

### Yön ayrımı (15m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | Stoch · dinamik · Hacim şoku + Onay mumu | %54.7 (64) | %43.5 (23) | %32.1 | -0.08R | 0.174 |
| yalnız LONG | WaveTrend · sabit 80/20 · filtre yok | %49.1 (55) | %63.2 (19) | %33.0 | +0.39R | 0.005 |
| yalnız SHORT | Stoch · dinamik · Onay mumu | %46.7 (107) | %34.2 (38) | %31.0 | -0.33R | 0.400 |

### Tekli göstergeler, filtresiz (15m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %37.7 (167) | %43.9 (66) | %32.2 | -0.14R |
| RSI | sabit 80/20 | %43.1 (51) | %42.3 (26) | %31.7 | -0.26R |
| Stoch | dinamik | %42.5 (254) | %35.8 (106) | %32.0 | -0.26R |
| Stoch | sabit 80/20 | %39.6 (326) | %37.5 (128) | %31.9 | -0.23R |
| WaveTrend | dinamik | %37.2 (137) | %45.1 (51) | %32.0 | -0.06R |
| WaveTrend | sabit 80/20 | %37.0 (127) | %48.9 (45) | %31.9 | +0.05R |

### Bileşen katkısı (15m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +0.6 puan | 24 |
| Volatilite şoku | +1.4 puan | 18 |
| Trend (EMA200) | +1.4 puan | 9 |
| Onay mumu | +1.6 puan | 33 |
| Dinamik eşik (sabite göre) | +1.2 puan | 26 |

### Kararlılık — seçilen ayar (iki yön), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2024-10-02 → 2024-10-30 | 19 | %42.1 | %31.7 | -0.07R |
| 2024-10-30 → 2024-11-26 | 21 | %52.4 | %31.9 | +0.14R |
| 2024-11-26 → 2025-06-01 | 27 | %63.0 | %33.4 | +0.42R |
| 2025-06-01 → 2026-03-08 | 20 | %45.0 | %31.7 | -0.04R |

### İlk 10 kombinasyon (15m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | Stoch · dinamik · Hacim şoku + Onay mumu | %54.7 (64) | %43.5 (23) | -0.08R |
| 2 | Stoch · dinamik · Onay mumu | %46.6 (206) | %37.7 (77) | -0.26R |
| 3 | Stoch · dinamik · Hacim şoku | %49.3 (71) | %41.4 (29) | -0.12R |
| 4 | Stoch · dinamik · Volatilite şoku + Onay mumu | %50.0 (50) | %47.4 (19) | -0.00R |
| 5 | Stoch · dinamik · filtre yok | %42.5 (254) | %35.8 (106) | -0.26R |
| 6 | Stoch · sabit 80/20 · Onay mumu | %41.7 (252) | %39.6 (96) | -0.22R |
| 7 | Stoch · dinamik · Volatilite şoku | %47.5 (59) | %45.5 (22) | -0.09R |
| 8 | Stoch · dinamik · Trend (EMA200) + Onay mumu | %45.7 (70) | %38.9 (36) | -0.25R |
| 9 | Stoch · sabit 80/20 · filtre yok | %39.6 (326) | %37.5 (128) | -0.23R |
| 10 | Stoch · sabit 80/20 · Volatilite şoku | %44.6 (83) | %36.7 (30) | -0.24R |

## SPX

Veri: 5m tabanı `dukascopy`, 1h tabanı `dukascopy`

### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)

| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |
|---|---|---|---|---|---|---|---|---|
| 5m ◀ | 79,776 | Stoch · dinamik · Hacim şoku + Onay mumu | %43.6 (528) | %39.9 (263) | %31.8 | -0.44R | 0.003 | ❌ OOS'ta tutmadı |
| 15m | 26,592 | Stoch · dinamik · Volatilite şoku + Trend (EMA200) + Onay mumu | %50.0 (50) | %48.1 (27) | %31.5 | -0.06R | 0.049 | ❌ OOS'ta tutmadı |
| 30m | 13,296 | Stoch+WaveTrend · dinamik · filtre yok | %46.1 (178) | %32.6 (89) | %32.9 | -0.41R | 0.570 | ❌ OOS'ta tutmadı |
| 1h | 52,566 | WaveTrend · dinamik · Hacim şoku + Volatilite şoku | %42.9 (259) | %44.6 (121) | %30.0 | -0.06R | <0.001 | ❌ OOS'ta tutmadı |
| 4h | 13,142 | WaveTrend · dinamik · Trend (EMA200) + Onay mumu | %48.0 (50) | %33.3 (24) | %40.3 | -0.22R | 0.816 | ❌ OOS'ta tutmadı |

### Yön ayrımı (5m)

| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |
|---|---|---|---|---|---|---|
| iki yön | Stoch · dinamik · Hacim şoku + Onay mumu | %43.6 (528) | %39.9 (263) | %31.8 | -0.44R | 0.003 |
| yalnız LONG | RSI+Stoch+WaveTrend · dinamik · Hacim şoku + Volatilite şoku | %47.4 (152) | %36.8 (68) | %31.9 | -0.50R | 0.231 |
| yalnız SHORT | Stoch · dinamik · Hacim şoku + Onay mumu | %44.2 (226) | %37.3 (110) | %31.6 | -0.51R | 0.119 |

### Tekli göstergeler, filtresiz (5m, iki yön)

| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |
|---|---|---|---|---|---|
| RSI | dinamik | %38.0 (1449) | %39.2 (637) | %31.7 | -0.55R |
| RSI | sabit 80/20 | %39.9 (233) | %42.9 (70) | %31.7 | -0.49R |
| Stoch | dinamik | %39.6 (1971) | %36.6 (864) | %31.7 | -0.57R |
| Stoch | sabit 80/20 | %39.3 (2854) | %37.7 (1263) | %31.7 | -0.57R |
| WaveTrend | dinamik | %39.8 (1153) | %37.8 (513) | %31.7 | -0.56R |
| WaveTrend | sabit 80/20 | %38.5 (1001) | %36.9 (455) | %31.7 | -0.56R |

### Bileşen katkısı (5m) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı

| Bileşen | Δ isabet | Çift sayısı |
|---|---|---|
| Hacim şoku | +0.3 puan | 96 |
| Volatilite şoku | +0.2 puan | 96 |
| Trend (EMA200) | +0.3 puan | 80 |
| Onay mumu | -0.1 puan | 96 |
| Dinamik eşik (sabite göre) | -2.7 puan | 80 |

### Kararlılık — seçilen ayar (yalnız LONG), tüm dönem 4 blok

| Dönem | n | İsabet | Taban | Beklenti |
|---|---|---|---|---|
| 2025-03-07 → 2026-02-02 | 54 | %46.3 | %28.2 | -0.27R |
| 2026-02-02 → 2026-04-23 | 56 | %48.2 | %33.0 | -0.11R |
| 2026-04-23 → 2026-07-13 | 51 | %43.1 | %32.7 | -0.27R |
| 2026-07-13 → 2026-10-01 | 59 | %39.0 | %32.2 | -0.43R |

### İlk 10 kombinasyon (5m, IS sıralı, iki yön)

| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |
|---|---|---|---|---|
| 1 | Stoch · dinamik · Hacim şoku + Onay mumu | %43.6 (528) | %39.9 (263) | -0.44R |
| 2 | Stoch · dinamik · Hacim şoku | %42.4 (628) | %38.2 (304) | -0.48R |
| 3 | Stoch · dinamik · Hacim şoku + Volatilite şoku + Onay mumu | %42.8 (388) | %36.8 (190) | -0.50R |
| 4 | Stoch · sabit 80/20 · Volatilite şoku + Trend (EMA200) | %43.1 (318) | %38.0 (142) | -0.52R |
| 5 | Stoch · sabit 80/20 · Volatilite şoku | %40.7 (921) | %40.7 (381) | -0.43R |
| 6 | Stoch · sabit 80/20 · filtre yok | %39.3 (2854) | %37.7 (1263) | -0.57R |
| 7 | Stoch · sabit 80/20 · Volatilite şoku + Onay mumu | %41.0 (747) | %42.0 (312) | -0.40R |
| 8 | Stoch · dinamik · filtre yok | %39.6 (1971) | %36.6 (864) | -0.57R |
| 9 | RSI+Stoch+WaveTrend · dinamik · Hacim şoku + Volatilite şoku | %43.4 (256) | %37.0 (119) | -0.49R |
| 10 | Stoch · sabit 80/20 · Onay mumu | %39.4 (2248) | %38.3 (995) | -0.55R |

---
Ayrıntılı tüm sonuçlar: `reports/tum_sonuclar.csv.gz` · Pine ayarları: `reports/en_iyi.json`
