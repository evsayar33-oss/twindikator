# ATVS v4 — Endeks araştırması ve 3. varlık

2026-10-07 19:52 UTC · gerçek veri · hedef: %95 olasılıkla maks. düşüş ≤ %15 · süre 16 dk

## Sonuç

**3. varlık eklenmesi önerilmiyor.** Hiçbir endeks adayı, mevcut portföyü hedef düşüş içinde kalarak hem tüm dönemde hem OOS dönemde iyileştiremedi. (Ayrıntılar aşağıda.)

## 1) Mevcut finalistler — Bitget gerçek maliyetiyle

Eski laboratuvar maliyeti CFD spread'iydi. Bitget: taker 2 bps × 2 + spread, fonlama 3 bps/gün.

| Finalist | eski maliyetle | Bitget maliyetiyle | Bitget OOS | işlem |
|---|---|---|---|---|
| F1_XAU_4h_DONCH | +0.317R | **+0.187R** | +0.262R | 434 |
| F2_ETH_4h_DONCH | +0.557R | **+0.550R** | +0.769R | 379 |

## 2) Endeks taraması

- NQ: 618 ayar test edildi · IS t ≥ 2.0: 10
- SPX: 618 ayar test edildi · IS t ≥ 2.0: 0

Kapılar: K1 OOS (BH q=0.10) · K2 tüm dönem ≥80 işlem · K3 maliyet×2 · K4 komşular ≥%70 pozitif · K5 yılların ≥%60'ı pozitif · K6 veri şüphesi

| Aday | IS t | OOS beklenti (n) | alfa | tüm dönem (n) | isabet | K1 K2 K3 K4 K5 K6 |
|---|---|---|---|---|---|---|
| NQ · CRSI(th=20) → çıkış rsi70 · stop 2.5ATR · en çok 10 gün | 2.6 | +0.040R (34) | +0.039R | +0.151R (111) | %76 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış rsi70 · stop 3.5ATR · en çok 10 gün | 2.5 | -0.024R (32) | -0.032R | +0.097R (103) | %76 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) + SMA200 trend → çıkış rsi70 · stop 3.5ATR · en çok 10 gün | 2.3 | +0.026R (22) | +0.018R | +0.118R (76) | %78 | ✗ ✗ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış sma5 · stop 3.5ATR · en çok 5 gün | 2.1 | +0.097R (35) | +0.085R | +0.113R (107) | %74 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış sma5 · stop 2.5ATR · en çok 10 gün | 2.1 | +0.158R (35) | +0.152R | +0.153R (113) | %73 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış sma5 · stop 3.5ATR · en çok 10 gün | 2.0 | +0.088R (34) | +0.077R | +0.108R (106) | %74 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış rsi70 · stop 3.5ATR · en çok 5 gün | 2.0 | +0.027R (35) | +0.025R | +0.092R (106) | %68 | ✗ ✓ · · ✓ ✓ |
| NQ · MACDDIP(k=3) + SMA200 trend → çıkış sma5 · stop 2.5ATR · en çok 5 gün | 2.0 | +0.019R (50) | +0.013R | +0.050R (145) | %61 | ✗ ✓ · · ✓ ✓ |
| NQ · MACDDIP(k=3) + SMA200 trend → çıkış sma5 · stop 2.5ATR · en çok 10 gün | 2.0 | +0.032R (49) | +0.027R | +0.054R (144) | %61 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış sma5 · stop 2.5ATR · en çok 5 gün | 2.0 | +0.152R (35) | +0.146R | +0.149R (113) | %73 | ✗ ✓ · · ✓ ✓ |

## 3) Portföy senaryoları

| Senaryo | riskler | CAGR | maks. düşüş | MC %95 düşüş | Sharpe | işlem/ay | OOS CAGR | hedef |
|---|---|---|---|---|---|---|---|---|
| Mevcut (XAU+ETH, %1) | F1 %1.00, F2 %1.00 | %20.1 | %17.3 | %14.8 | 1.21 | 4.6 | %33.3 | ✓ |

## Uygulama notları (Bitget hisse/endeks vadelileri)

- Kontratlar 7/24 fiyatlanır ama ABD piyasası kapalıyken **yeni pozisyon açılamaz**; bu yüzden giriş/çıkış 15:00 ET'de (seans içi).
- Gece ve hafta sonu açık pozisyonun stopu boşlukla (gap) geçilebilir; backtest bunu açılış fiyatıyla doldurarak hesaplar (R < −1 olabilir).
- ABD tatil günlerinde veri olsa bile borsa emri reddedebilir; bot hatayı yazar ve o günü atlar.
- Geçmiş sonuçtur; seçim yanlılığı tamamen yok edilemez. Önce demo.
