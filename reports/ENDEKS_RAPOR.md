# ATVS v4 — Endeks araştırması ve 3. varlık

2026-10-07 18:11 UTC · gerçek veri · hedef: %95 olasılıkla maks. düşüş ≤ %15 · süre 8 dk

## Sonuç

**3. varlık eklenmesi önerilmiyor.** Hiçbir endeks adayı, mevcut portföyü hedef düşüş içinde kalarak hem tüm dönemde hem OOS dönemde iyileştiremedi. (Ayrıntılar aşağıda.)

## 1) Mevcut finalistler — Bitget gerçek maliyetiyle

Eski laboratuvar maliyeti CFD spread'iydi. Bitget: taker 6 bps × 2 + spread, fonlama 3 bps/gün.

| Finalist | eski maliyetle | Bitget maliyetiyle | Bitget OOS | işlem |
|---|---|---|---|---|
| F1_XAU_4h_DONCH | +0.317R | **+0.002R** | +0.090R | 434 |
| F2_ETH_4h_DONCH | +0.557R | **+0.508R** | +0.725R | 379 |

## 2) Endeks taraması

- NQ: 618 ayar test edildi · IS t ≥ 2.0: 3
- SPX: 618 ayar test edildi · IS t ≥ 2.0: 0

Kapılar: K1 OOS (BH q=0.10) · K2 tüm dönem ≥80 işlem · K3 maliyet×2 · K4 komşular ≥%70 pozitif · K5 yılların ≥%60'ı pozitif · K6 veri şüphesi

| Aday | IS t | OOS beklenti (n) | alfa | tüm dönem (n) | isabet | K1 K2 K3 K4 K5 K6 |
|---|---|---|---|---|---|---|
| NQ · CRSI(th=20) → çıkış rsi70 · stop 2.5ATR · en çok 10 gün | 2.3 | +0.021R (34) | +0.041R | +0.128R (111) | %75 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) → çıkış rsi70 · stop 3.5ATR · en çok 10 gün | 2.2 | -0.037R (32) | -0.030R | +0.081R (103) | %75 | ✗ ✓ · · ✓ ✓ |
| NQ · CRSI(th=20) + SMA200 trend → çıkış rsi70 · stop 3.5ATR · en çok 10 gün | 2.0 | +0.011R (22) | +0.018R | +0.100R (76) | %76 | ✗ ✗ · · ✓ ✓ |

## 3) Portföy senaryoları

| Senaryo | riskler | CAGR | maks. düşüş | MC %95 düşüş | Sharpe | işlem/ay | OOS CAGR | hedef |
|---|---|---|---|---|---|---|---|---|
| Mevcut (XAU+ETH, %1) | F1 %1.00, F2 %1.00 | %12.6 | %32.5 | %18.3 | 0.81 | 4.6 | %23.5 | ✗ |

## Uygulama notları (Bitget hisse/endeks vadelileri)

- Kontratlar 7/24 fiyatlanır ama ABD piyasası kapalıyken **yeni pozisyon açılamaz**; bu yüzden giriş/çıkış 15:00 ET'de (seans içi).
- Gece ve hafta sonu açık pozisyonun stopu boşlukla (gap) geçilebilir; backtest bunu açılış fiyatıyla doldurarak hesaplar (R < −1 olabilir).
- ABD tatil günlerinde veri olsa bile borsa emri reddedebilir; bot hatayı yazar ve o günü atlar.
- Geçmiş sonuçtur; seçim yanlılığı tamamen yok edilemez. Önce demo.
