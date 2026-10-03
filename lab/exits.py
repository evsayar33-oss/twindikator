"""Yol bağımlı çıkış simülatörü.

İki uygulama, BİREBİR aynı kurallar (selftest eşitliği doğrular):
  simulate()      — tüm barlar için vektörize (araştırma / backtest)
  simulate_one()  — tek işlem, adım adım (canlı kâğıt işlem motoru; işlem açıkken ara durum döner)

Kurallar (sinyal barı i):
  giriş = open[i+1], ilk risk = sl_atr × ATR[i], 1R = ilk risk
  her bar k = 1..H (bar i+k), muhafazakâr sıra:
    1) stop kontrolü (aynı barda hedef + stop → stop)
    2) TP1: kısmi kapama (part) + stop girişe (bir SONRAKİ bardan itibaren geçerli)
    3) son hedef
    4) iz süren stop güncellemesi: en uç fiyat − trail × ATR[i] (bir SONRAKİ bardan itibaren)
  k = H: kalan pozisyon close[i+H] ile kapanır
  sonuç: clip(R, −3, +20) − maliyet (R cinsinden)
  giriş ile zaman bariyeri arasında > GAP_DAYS boşluk varsa işlem geçersiz
SHORT, fiyat ekseni ters çevrilerek aynı LONG mantığıyla hesaplanır.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C

R_CAP = 20.0
R_FLOOR = -3.0
GAP_DAYS = 4


def _shift(x: np.ndarray, k: int) -> np.ndarray:
    out = np.empty_like(x)
    out[: len(x) - k] = x[k:]
    out[len(x) - k:] = np.nan
    return out


def _seconds(index: pd.DatetimeIndex) -> np.ndarray:
    return index.values.astype("datetime64[s]").astype(np.int64)


def gap_mask(index: pd.DatetimeIndex, H: int) -> np.ndarray:
    """True = (i, i+H+1] penceresinde GAP_DAYS'ten uzun veri boşluğu var."""
    gap = np.r_[False, np.diff(_seconds(index)) > GAP_DAYS * 86400].astype(np.int8)
    ahead = pd.Series(gap[::-1]).rolling(H + 1, min_periods=1).max().to_numpy()[::-1].astype(bool)
    return np.r_[ahead[1:], False]


def simulate(df: pd.DataFrame, atr: pd.Series, cost_bps: float, cfg: dict, H: int | None = None) -> dict:
    """Dönen: {1: R_long, -1: R_short, (1,'k'): çıkış ofseti, (-1,'k'): ..., 'valid': maske}.
    Çıkış ofseti k: işlem bar i+k içinde kapanır (1..H)."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    a = atr.to_numpy(float)
    n = len(c)
    H = H or C.HORIZON
    entry0 = _shift(o, 1)
    valid = np.isfinite(entry0) & np.isfinite(a) & (a > 0)
    valid[max(0, n - H - 1):] = False
    valid &= ~gap_mask(df.index, H)
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
        kx = np.full(n, float(H))
        for k in range(1, H + 1):
            hh, ll = _shift(hi_s, k), _shift(lo_s, k)
            with np.errstate(invalid="ignore"):
                hs = alive & (ll <= stop)
            R[hs] += size[hs] * (stop[hs] - e[hs]) / risk[hs]
            kx[hs] = k
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
                kx[ht] = k
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
        R = np.clip(R, R_FLOOR, R_CAP) - cost
        R[~valid] = np.nan
        kx[~valid] = np.nan
        out[side] = R
        out[(side, "k")] = kx
    return out


def simulate_all(df: pd.DataFrame, atr: pd.Series, cost_bps: float) -> dict:
    return {name: simulate(df, atr, cost_bps, cfg) for name, cfg in C.EXITS.items()}


def simulate_one(o, h, l, c, a_sig: float, i: int, side: int, cfg: dict, cost_bps: float, H: int | None = None) -> dict:
    """Tek işlem. Mevcut barlarla ilerler; veri bitince 'open' durumunu ve güncel stopu döner.
    Fiyatlar gerçek eksende döner (SHORT için geri çevrilmiş)."""
    H = H or C.HORIZON
    n = len(c)
    res = {"status": "pending", "events": [], "R": None, "exit_k": None, "tp1_k": None,
           "entry": None, "stop": None, "tp1_px": None, "tp_px": None, "size": 1.0, "be": False}
    if i + 1 >= n:
        return res                                          # giriş barı henüz oluşmadı
    entry = float(o[i + 1])
    risk = cfg["sl_atr"] * a_sig
    tp, tp1, part = cfg.get("tp"), cfg.get("tp1"), cfg.get("part", 0.0)
    trail, tmode = cfg.get("trail"), cfg.get("trail_mode", "always")
    e = side * entry
    stop = e - risk
    ext = e
    size, R, be = 1.0, 0.0, False
    res.update(entry=entry, tp1_px=None if tp1 is None else side * (e + tp1 * risk), tp_px=None if tp is None else side * (e + tp * risk))
    cost = (cost_bps / 1e4) * entry / risk

    def fin(Rv, k, why):
        Rv = float(np.clip(Rv, R_FLOOR, R_CAP) - cost)
        res.update(status="closed", R=Rv, exit_k=k, reason=why)
        res["events"].append(("exit", k, why, Rv))
        return res

    for k in range(1, H + 1):
        j = i + k
        if j >= n:
            res.update(status="open", stop=side * stop, size=size, be=be, bars_held=k - 1, R_realized=R)
            return res
        hh = h[j] if side == 1 else -l[j]
        ll = l[j] if side == 1 else -h[j]
        if ll <= stop:
            why = "stop" if not be and stop <= e - risk + 1e-12 else ("başabaş stop" if abs(stop - e) < 1e-12 else "iz süren stop")
            return fin(R + size * (stop - e) / risk, k, why)
        if tp1 is not None and not be and hh >= e + tp1 * risk:
            if part > 0:
                R += part * tp1
                size -= part
            be = True
            stop = max(stop, e)
            res["tp1_k"] = k
            res["events"].append(("tp1", k))
        if tp is not None and hh >= e + tp * risk:
            return fin(R + size * tp, k, "hedef")
        if trail is not None:
            ext = max(ext, hh)
            if be or tmode != "be":
                stop = max(stop, ext - trail * a_sig)
    if i + H >= n:
        res.update(status="open", stop=side * stop, size=size, be=be, bars_held=H, R_realized=R)
        return res
    cl = c[i + H] if side == 1 else -c[i + H]
    return fin(R + size * (cl - e) / risk, H, "zaman")
