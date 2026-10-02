"""Gösterge kütüphanesi. Tümü nedensel (yalnızca geçmiş veri), Pine ile aynı tanımlar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def rma(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def ema(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def rsi(c: pd.Series, n: int) -> pd.Series:
    d = c.diff()
    up, dn = rma(d.clip(lower=0), n), rma((-d).clip(lower=0), n)
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100.0).where(dn.notna())


def stoch(h, l, c, n, sm) -> pd.Series:
    ll, hh = l.rolling(n).min(), h.rolling(n).max()
    return (100 * (c - ll) / (hh - ll).replace(0, np.nan)).rolling(sm).mean()


def wavetrend_norm(h, l, c, n1, n2, scale) -> pd.Series:
    ap = (h + l + c) / 3
    esa = ema(ap, n1)
    d = ema((ap - esa).abs(), n1)
    wt1 = ema(((ap - esa) / (0.015 * d.replace(0, np.nan))).fillna(0), n2)
    return 50 + 50 * np.tanh(wt1 / scale)


def robust_z(x: pd.Series, n: int) -> pd.Series:
    med = x.rolling(n).median()
    mad = (x - med).abs().rolling(n).median()
    return (x - med.shift(1)) / (1.4826 * mad.shift(1)).replace(0, np.nan)


def true_range(h, l, c) -> pd.Series:
    return pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)


def adx(h, l, c, n=14) -> pd.Series:
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=h.index)
    ndm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=h.index)
    atr = rma(true_range(h, l, c), n)
    pdi, ndi = 100 * rma(pdm, n) / atr, 100 * rma(ndm, n) / atr
    dx = 100 * (pdi - ndi).abs() / (pdi + ndi).replace(0, np.nan)
    return rma(dx.fillna(0), n)


def efficiency_ratio(c: pd.Series, n: int) -> pd.Series:
    return (c - c.shift(n)).abs() / c.diff().abs().rolling(n).sum().replace(0, np.nan)


def local_index(idx: pd.DatetimeIndex, tz: str) -> pd.DatetimeIndex:
    return idx.tz_convert(tz)


def session_vwap(df: pd.DataFrame, tz: str = "America/New_York", anchor_hour: int = 18) -> pd.Series:
    """Seans VWAP'ı. Varsayılan çapa: New York 18:00 (CFD/futures günlük seans başlangıcı)."""
    loc = df.index.tz_convert(tz)
    sess = (loc - pd.Timedelta(hours=anchor_hour)).normalize()
    tp = (df["high"] + df["low"] + df["close"]) / 3
    v = df["volume"].clip(lower=0).replace(0, np.nan).fillna(1e-9)
    g = pd.Series(np.asarray(sess), index=df.index)
    pv = (tp * v).groupby(g.values).cumsum()
    vv = v.groupby(g.values).cumsum()
    return pv / vv


def compute(df: pd.DataFrame) -> dict:
    """Bütün stratejilerin ortak kullandığı gösterge sözlüğü."""
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))
    tr = true_range(h, l, c)
    f = {
        "o": o, "h": h, "l": l, "c": c, "v": v,
        "R": rsi(c, C.RSI_LEN),
        "S": stoch(h, l, c, C.STOCH_LEN, C.STOCH_SMOOTH),
        "W": wavetrend_norm(h, l, c, C.WT_N1, C.WT_N2, C.WT_SCALE),
        "rsi2": rsi(c, 2),
        "atr": rma(tr, C.ATR_LEN),
        "ema200": ema(c, C.TREND_EMA),
        "ema50": ema(c, 50),
        "volZ": robust_z(np.log1p(v.clip(lower=0)), C.SHOCK_LEN),
        "vtyZ": robust_z(np.log(tr.clip(lower=1e-12)), C.SHOCK_LEN),
        "er": efficiency_ratio(c, C.ER_LEN),
        "adx": adx(h, l, c, 14),
    }
    f["has_vol"] = bool((v > 0).mean() > 0.5)
    er = f["er"]
    f["er_lo"] = er.rolling(C.REGIME_LEN, min_periods=C.REGIME_LEN // 2).quantile(C.RANGE_PCT / 100).shift(1)
    f["er_hi"] = er.rolling(C.REGIME_LEN, min_periods=C.REGIME_LEN // 2).quantile(C.TREND_PCT / 100).shift(1)
    basis = c.rolling(C.BB_LEN).mean()
    sd = c.rolling(C.BB_LEN).std()
    f["bb_mid"], f["bb_up"], f["bb_dn"] = basis, basis + C.BB_K * sd, basis - C.BB_K * sd
    kc_atr = rma(tr, C.BB_LEN)
    f["kc_up"], f["kc_dn"] = ema(c, C.BB_LEN) + C.KC_K * kc_atr, ema(c, C.BB_LEN) - C.KC_K * kc_atr
    f["bbw_pct"] = ((f["bb_up"] - f["bb_dn"]) / basis).rolling(200, min_periods=100).rank(pct=True)
    f["ret"] = np.log(c).diff()
    f["ret_z"] = f["ret"] / f["ret"].rolling(100, min_periods=50).std().shift(1)
    return f
