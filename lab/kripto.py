"""Kripto günlük MACD kuralları (v4.3 doğrulamasını geçti). Araştırma, doğrulama ve canlı bot AYNI fonksiyonları kullanır.

  EMA : MACD yön (1s eşdeğeri: ≈28/36/20 günlük EMA) + EMA20'ye geri çekilme · iz süren stop 2.5 ATR · iki yön
  X   : MACD yön (1s eşdeğeri) + hızlı MACD(12,26,9) sıfır kesişimi · iz süren stop 2.5 ATR · yalnız LONG
Yön: MACD çizgisi sinyalin üstünde → yalnız LONG aranır; altında → yalnız SHORT (bir sonraki ters kesişime kadar).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C
from . import features as FT
from . import strategies as ST

COINS = ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE", "LTC", "LINK", "TRX", "DOT", "AVAX", "BCH", "ETC", "XLM"]
EXIT = "IZ_SUREN_2.5ATR"
RULES = {"EMA": "both", "X": "long"}


def direction(c: pd.Series, scale: float = 1.0, tf_min: int = 1440) -> np.ndarray:
    s = C.MACD_DIR_BASE_MIN / tf_min * scale
    nf, ns, nsig = (max(2, int(round(x * s))) for x in C.MACD_DIR)
    m = FT.ema(c, nf) - FT.ema(c, ns)
    return np.sign((m - FT.ema(m, nsig)).to_numpy())


def entries(df: pd.DataFrame, d: np.ndarray | None = None, ema_len: int = 20, tf_min: int = 1440) -> dict:
    """Dönen: {"EMA": (LONG, SHORT), "X": (LONG, SHORT)} — mum kapanışında sinyal; giriş sonraki mumun açılışı."""
    if d is None:
        d = direction(df["close"], tf_min=tf_min)
    c, h, l = (df[k].to_numpy(float) for k in ("close", "high", "low"))
    up, dn = d > 0, d < 0
    e = FT.ema(df["close"], ema_len).to_numpy()
    with np.errstate(invalid="ignore"):
        Le, Se = up & (l <= e) & (c > e), dn & (h >= e) & (c < e)
    fm = FT.ema(df["close"], 12) - FT.ema(df["close"], 26)
    xx = (fm - FT.ema(fm, 9)).to_numpy()
    Lx = up & ST.cross_up(xx, 0.0)
    z = np.zeros(len(c), bool)
    f = lambda a, n: ST.cooldown(np.nan_to_num(a.astype(float)).astype(bool), n)  # noqa: E731
    return {"EMA": (f(Le, 6), f(Se, 6)), "X": (f(Lx, 3), z)}
