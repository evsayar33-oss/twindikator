"""Yol bağımlı çıkış simülatörü — tüm barlar için vektörize.

Her bar i için 'sinyal i'de oluşsaydı' sonucu hesaplanır: giriş open[i+1], ilk stop = sl_atr × ATR[i].
Sıra (her bar, muhafazakâr):
  1) stop kontrolü (aynı barda hedef + stop → stop sayılır)
  2) TP1: kısmi kapama + stop girişe (bir SONRAKİ bardan itibaren geçerli)
  3) son hedef
  4) iz süren stop güncellemesi (bir SONRAKİ bardan itibaren geçerli)
Zaman bariyerinde kalan pozisyon kapanış fiyatından kapatılır. Sonuç R cinsinden, maliyet düşülmüş.
SHORT, fiyat ekseni ters çevrilerek aynı LONG mantığıyla hesaplanır.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


R_CAP = 20.0


def _shift(x: np.ndarray, k: int) -> np.ndarray:
    out = np.empty_like(x)
    out[: len(x) - k] = x[k:]
    out[len(x) - k:] = np.nan
    return out


def simulate(df: pd.DataFrame, atr: pd.Series, cost_bps: float, cfg: dict) -> dict:
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    a = atr.to_numpy(float)
    n, H = len(c), C.HORIZON
    entry0 = _shift(o, 1)
    valid = np.isfinite(entry0) & np.isfinite(a) & (a > 0)
    valid[max(0, n - H - 1):] = False
    out = {"valid": valid}
    sl_atr = cfg["sl_atr"]
    tp, tp1, part = cfg.get("tp"), cfg.get("tp1"), cfg.get("part", 0.0)
    trail, tmode = cfg.get("trail"), cfg.get("trail_mode", "always")
    for side in (1, -1):
        e = side * entry0
        hi_s, lo_s, cl_s = (h, l, c) if side == 1 else (-l, -h, -c)
        risk = sl_atr * a
        stop = e - risk
        R = np.zeros(n)
        size = np.ones(n)
        alive = valid.copy()
        be = np.zeros(n, bool)
        ext = e.copy()
        for k in range(1, H + 1):
            hh, ll = _shift(hi_s, k), _shift(lo_s, k)
            with np.errstate(invalid="ignore"):
                hs = alive & (ll <= stop)
            R[hs] += size[hs] * (stop[hs] - e[hs]) / risk[hs]
            alive &= ~hs
            if tp1 is not None:
                with np.errstate(invalid="ignore"):
                    h1 = alive & ~be & (hh >= e + tp1 * risk)
                if part > 0:
                    R[h1] += part * tp1
                    size[h1] -= part
                be |= h1
                stop = np.where(h1, np.maximum(stop, e), stop)
            if tp is not None:
                with np.errstate(invalid="ignore"):
                    ht = alive & (hh >= e + tp * risk)
                R[ht] += size[ht] * tp
                alive &= ~ht
            if trail is not None:
                act = alive & (be if tmode == "be" else True)
                with np.errstate(invalid="ignore"):
                    ext = np.where(alive, np.fmax(ext, hh), ext)
                    stop = np.where(act, np.fmax(stop, ext - trail * a), stop)
            if not alive.any():
                break
        cH = _shift(cl_s, H)
        R[alive] += size[alive] * (cH[alive] - e[alive]) / risk[alive]
        cost = (cost_bps / 1e4) * entry0 / risk
        R = np.clip(R, -3.0, R_CAP) - cost   # boşluk/hatalı tik koruması: tek işlem en fazla −3R / +R_CAP
        R[~valid] = np.nan
        out[side] = R
    return out


def simulate_all(df: pd.DataFrame, atr: pd.Series, cost_bps: float) -> dict:
    return {name: simulate(df, atr, cost_bps, cfg) for name, cfg in C.EXITS.items()}
