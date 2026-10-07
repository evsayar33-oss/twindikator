# Kripto günlük — MACD kombinasyonları (havuzlanmış yeniden sınama)

2026-10-07 20:01 UTC · gerçek veri · 15 coin · Bitget maliyeti (taker 6 bps × 2 + spread, fonlama 3 bps/gün) · süre 2 dk

IS = 2023-01-01 öncesi · OOS = sonrası · seçim IS'te havuzlanmış t'ye göre ilk 10 · OOS'ta BH q=0.1

## Sonuç

**8 kural bütün şartları geçti.** En iyisi: **MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) · IZ_SUREN_2.5ATR · both** — tüm dönem +0.351R (1386 işlem), OOS +0.170R (710), coinlerin %87'ında pozitif.

Portföy önizlemesi (geçen kural, tüm coinler, işlem başına %0.5 risk, en fazla 4 açık): CAGR %8.9 · maks. düşüş %18.5 · MC %95 düşüş %15.9 · ayda 6.6 işlem

## IS'te seçilen ilk hipotezler ve şartlar

| Giriş | Çıkış | Yön | IS t | IS (n) | OOS (n) | tüm dönem (n) | coin pozitif | maliyet×2 | BTC 2014+ (n) | K1 | geçti |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | IZ_SUREN_2.5ATR | both | 5.2 | +0.540R (676) | +0.170R (710) | +0.351R (1386) | %87 (15) | +0.327R | +1.057R (148) | ✓ | ✅ |
| MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri) | IZ_SUREN_2.5ATR | both | 5.0 | +0.454R (823) | +0.205R (779) | +0.333R (1602) | %93 (15) | +0.310R | +0.593R (169) | ✓ | ✅ |
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | IZ_SUREN_2.5ATR | long | 4.6 | +0.630R (463) | +0.090R (420) | +0.373R (883) | %87 (15) | +0.350R | +1.484R (78) | ✗ | ❌ |
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | SABIT_4R | both | 4.4 | +0.366R (659) | +0.205R (656) | +0.286R (1315) | %93 (15) | +0.262R | +0.492R (146) | ✓ | ✅ |
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | TP0.5>BE_3R | both | 4.3 | +0.198R (885) | +0.131R (880) | +0.165R (1765) | %100 (15) | +0.141R | +0.279R (174) | ✓ | ✅ |
| MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri) | IZ_SUREN_2.5ATR | long | 4.3 | +0.520R (553) | +0.218R (484) | +0.379R (1037) | %80 (15) | +0.355R | +0.920R (93) | ✓ | ✅ |
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | SABIT_4R | long | 4.1 | +0.430R (445) | +0.018R (398) | +0.235R (843) | %80 (15) | +0.212R | +0.681R (80) | ✗ | ❌ |
| MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) | %50@1R>BE_4R | both | 4.0 | +0.188R (750) | +0.080R (770) | +0.133R (1520) | %93 (15) | +0.109R | +0.225R (166) | ✓ | ✅ |
| MACDYON · yön + hızlı MACD(12,26,9) kesişimi (1s eşdeğeri) | IZ_SUREN_2.5ATR | long | 3.9 | +0.771R (249) | +0.548R (214) | +0.668R (463) | %93 (15) | +0.642R | +1.098R (44) | ✓ | ✅ |
| MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri) | TP0.5>BE_3R | both | 3.8 | +0.160R (1013) | +0.086R (993) | +0.123R (2006) | %87 (15) | +0.100R | +0.244R (203) | ✓ | ✅ |

### Coin bazında — MACDYON · yön + RSI(2) aşırı (1s eşdeğeri) · IZ_SUREN_2.5ATR · both

| Coin | işlem | ort. R | toplam R |
|---|---|---|---|
| DOGEUSDT | 80 | +0.804 | +64.4 |
| BTCUSDT | 115 | +0.746 | +85.8 |
| ADAUSDT | 98 | +0.609 | +59.7 |
| DOTUSDT | 76 | +0.552 | +42.0 |
| BNBUSDT | 113 | +0.525 | +59.3 |
| XRPUSDT | 91 | +0.496 | +45.2 |
| XLMUSDT | 102 | +0.364 | +37.1 |
| ETHUSDT | 101 | +0.314 | +31.7 |
| ETCUSDT | 108 | +0.307 | +33.1 |
| LTCUSDT | 98 | +0.222 | +21.8 |
| BCHUSDT | 83 | +0.128 | +10.7 |
| AVAXUSDT | 66 | +0.064 | +4.2 |
| TRXUSDT | 97 | +0.053 | +5.1 |
| SOLUSDT | 74 | -0.065 | -4.8 |
| LINKUSDT | 84 | -0.106 | -8.9 |

| Yıl | işlem | ort. R |
|---|---|---|
| 2017 | 8 | +0.400 |
| 2018 | 82 | -0.222 |
| 2019 | 116 | +0.519 |
| 2020 | 136 | +1.174 |
| 2021 | 168 | +0.854 |
| 2022 | 166 | +0.102 |
| 2023 | 176 | +0.097 |
| 2024 | 220 | -0.125 |
| 2025 | 209 | +0.460 |
| 2026 | 105 | +0.336 |

## Karşılaştırma — aynı coinlerde filtresiz DONCH / RSI2 (IS'e göre ilk 5)

| Giriş | Çıkış | Yön | IS (n) | OOS (n) | coin pozitif |
|---|---|---|---|---|---|
| RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | both | +0.254R (1025) | -0.003R (1020) | %67 |
| DONCH · Donchian 20 · filtresiz | GENIS_%50@1R>BE_3R | long | +0.206R (361) | +0.106R (346) | %80 |
| RSI2 · RSI(2) 10/90 · filtresiz | IZ_SUREN_2.5ATR | long | +0.281R (782) | -0.133R (741) | %60 |
| RSI2 · RSI(2) 5/95 · filtresiz | IZ_SUREN_2.5ATR | long | +0.325R (569) | +0.143R (514) | %87 |
| DONCH · Donchian 20 · filtresiz | IZ_SUREN_2.5ATR | long | +0.422R (362) | +0.154R (352) | %80 |

## Notlar

- Coin listesi bugünün büyük coinleridir (hayatta kalma yanlılığı: batan coinler listede yok) — sonuçları biraz iyimser yapar.
- BTC 2014+ testi yfinance spot verisiyledir; 2017 öncesi dönem hiç seçimde kullanılmadı (bağımsız sınav).
- Bot bugün yalnızca BTC/ETH/XAU/XAG ve endeksleri işleyebilir; diğer coinler için sembol desteği gerekir.
