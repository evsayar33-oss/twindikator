# ATVS v4.3 — Doğrulama paketi (kripto günlük MACD kuralları)

2026-10-07 20:41 UTC · gerçek veri · 15 coin + 8 listeden çıkmış coin · Bitget maliyeti · süre 16 dk · kural motoru lab ile birebir: evet

## Hüküm

| Kural | D1 haftalık küme t ≥ 2 (tüm) ve OOS > 0 | D2 batan coinler dahil > 0 | D3 placebo p ≤ 0.05 | D4 komşu ayarların ≥ %70'i pozitif | maliyet ×2 > 0 | SONUÇ |
|---|---|---|---|---|---|---|
| MACD yön + EMA20'ye geri çekilme · iki yön | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ GEÇTİ |
| MACD yön + hızlı MACD kesişimi · yalnız LONG | ✓ | ✓ | ✓ | ✓ | ✓ | ✅ GEÇTİ |

## D1 — Bağımlılık düzeltmeli istatistik

Kripto coinleri birlikte hareket eder; aynı hafta açılan işlemler bağımsız sayılmaz (küme-sağlam standart hata).

| Kural | dönem | işlem | beklenti | isabet | ham t | günlük küme t | **haftalık küme t** |
|---|---|---|---|---|---|---|---|
| EMA | tüm | 1602 | +0.333R | %33 | 5.37 | 4.28 | **3.76** |
| EMA | IS <2023 | 823 | +0.454R | %34 | 4.96 | 3.74 | **3.34** |
| EMA | OOS 2023+ | 779 | +0.205R | %33 | 2.47 | 2.17 | **1.87** |
| X | tüm | 463 | +0.668R | %38 | 4.92 | 4.02 | **2.99** |
| X | IS <2023 | 249 | +0.771R | %36 | 3.92 | 3.14 | **2.20** |
| X | OOS 2023+ | 214 | +0.548R | %39 | 2.98 | 2.56 | **2.18** |

## D2 — Listeden çıkan / batan coinler dahil

| Kural | batan coinler | batan coinlerde | hepsi birlikte |
|---|---|---|---|
| EMA | ANC, BTS, FTT, LUNA, MIR, SRM, WAVES, XEM | +0.186R (373) | +0.305R (1975) |
| X | ANC, BTS, FTT, LUNA, MIR, SRM, WAVES, XEM | +0.724R (126) | +0.680R (589) |

## D3 — Placebo (300 rastgele yön)

MACD yönü yerine aynı süre dağılımına sahip rastgele yön kullanıldı (EMA20 / hızlı MACD tetikleri aynı).

| Kural | gerçek | rastgele ortalama | rastgele %95 | p (rastgele ≥ gerçek) | maliyet ×2 |
|---|---|---|---|---|---|
| EMA | **+0.333R** | +0.146R | +0.221R | 0.000 | +0.310R |
| X | **+0.668R** | +0.271R | +0.382R | 0.000 | +0.642R |

## D4 — Ayar hassasiyeti

**EMA** — komşu ayarların %100'ı pozitif (OOS: %100)

| MACD ölçeği | EMA | işlem | beklenti | OOS beklenti |
|---|---|---|---|---|
| ×0.7 | 15 | 1803 | +0.257R | +0.143R |
| ×0.7 | 20 | 1683 | +0.256R | +0.086R |
| ×0.7 | 25 | 1568 | +0.276R | +0.076R |
| ×0.85 | 15 | 1762 | +0.286R | +0.151R |
| ×0.85 | 20 | 1646 | +0.299R | +0.127R |
| ×0.85 | 25 | 1544 | +0.338R | +0.142R |
| ×1.0 | 15 | 1716 | +0.346R | +0.229R |
| ×1.0 | 20 | 1602 | +0.333R | +0.205R |
| ×1.0 | 25 | 1516 | +0.282R | +0.181R |
| ×1.15 | 15 | 1687 | +0.292R | +0.164R |
| ×1.15 | 20 | 1585 | +0.285R | +0.182R |
| ×1.15 | 25 | 1495 | +0.237R | +0.156R |
| ×1.3 | 15 | 1649 | +0.277R | +0.170R |
| ×1.3 | 20 | 1559 | +0.288R | +0.203R |
| ×1.3 | 25 | 1467 | +0.228R | +0.146R |

**X** — komşu ayarların %100'ı pozitif (OOS: %100)

| MACD ölçeği | EMA | işlem | beklenti | OOS beklenti |
|---|---|---|---|---|
| ×0.7 | 20 | 461 | +0.527R | +0.284R |
| ×0.85 | 20 | 444 | +0.642R | +0.455R |
| ×1.0 | 20 | 463 | +0.668R | +0.548R |
| ×1.15 | 20 | 486 | +0.627R | +0.526R |
| ×1.3 | 20 | 513 | +0.540R | +0.419R |

## D5 — Diğer varlıklar (bilgi; aynı kurallar, değiştirilmeden, günlük)

| Varlık | kural | işlem | beklenti | OOS | haftalık küme t |
|---|---|---|---|---|---|
| XAU | EMA | 191 | -0.371R | -0.491R | -2.92 |
| XAU | X | 50 | +0.491R | +0.809R | 1.36 |
| XAG | EMA | 193 | -0.035R | -0.206R | -0.22 |
| XAG | X | 46 | +0.235R | +1.078R | 0.78 |
| NQ | EMA | 187 | -0.340R | -0.317R | -3.01 |
| NQ | X | 41 | -0.337R | -0.579R | -1.28 |
| SPX | EMA | 185 | -0.541R | -0.550R | -5.03 |
| SPX | X | 46 | -0.457R | -0.739R | -1.78 |

## D6 — Portföy (hedef: %95 olasılıkla düşüş ≤ %15)

| Senaryo | risk EMA | risk X | risk F1_XAU_4h_DONCH | risk F2_ETH_4h_DONCH | en fazla açık | CAGR | maks. düşüş | MC %95 | Sharpe | işlem/ay | OOS CAGR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mevcut finalistler | %0.00 | %0.00 | %0.00 | %1.00 | 4 | %21.9 | %16.6 | %14.2 | 1.22 | 3.5 | %25.9 |
| Yalnız EMA | %0.50 | %0.00 | %0.00 | %0.00 | 4 | %16.7 | %11.8 | %13.5 | 1.19 | 7.4 | %14.0 |
| Yalnız X | %0.00 | %0.75 | %0.00 | %0.00 | 4 | %15.9 | %12.7 | %13.6 | 1.07 | 3.0 | %16.6 |
| EMA + X | %0.50 | %1.00 | %0.00 | %0.00 | 4 | %23.9 | %11.7 | %13.8 | 1.47 | 7.7 | %24.4 |
| **EN İYİ (hedef içinde)** | %0.00 | %0.50 | %0.00 | %1.00 | 4 | %29.9 | %12.7 | %14.7 | 1.50 | 5.8 | %33.8 |

Kurallar: coin başına aynı anda tek pozisyon (EMA ve X aynı coinde çakışmaz; ETH 4h Donchian ile ETH günlük de çakışmaz).

## Notlar

- Kurallar v4.2'deki haliyle sabittir; bu pakette hiçbir parametre sonuca bakılarak değiştirilmedi.
- Batan coinler yalnızca istatistik testinde kullanılır (bugün işlem görmezler).
- Geçmiş sonuçtur; önce demo.
