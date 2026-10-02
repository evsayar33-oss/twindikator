"""Göstergeler, sinyal kombinasyonları, üçlü bariyer etiketleme ve istatistik.

Mantık Pine 'ATVS Lab' göstergesiyle birebir aynıdır:
  • Osilatörler: RSI, Stoch %K, WaveTrend (tanh ile 0-100'e normalize)
  • Eşik: SABİT 80/20 veya DİNAMİK (kayan 300 bar persentil 90/10, bir önceki bara kadar)
  • Olay: seçilen osilatörlerin TÜMÜ son ARM bar içinde bölgeye değmiş + HERHANGİ biri bölgeden çıkıyor
  • Filtreler: VOL (hacim şoku), VTY (volatilite şoku), TREND (EMA200 yönü), CONF (onay mumu)
  • Giriş: sinyal barından sonraki barın açılışı; çıkış: TP 1.5 ATR / SL 1 ATR / 24 bar
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd

from . import config as C

OSC = ("R", "S", "W")
OSC_NAME = {"R": "RSI", "S": "Stoch", "W": "WaveTrend"}
FILTERS = ("VOL", "VTY", "TREND", "CONF")
FILTER_NAME = {"VOL": "Hacim şoku", "VTY": "Volatilite şoku", "TREND": "Trend (EMA200)", "CONF": "Onay mumu"}
MODES = ("static", "dynamic")
MODE_NAME = {"static": "sabit 80/20", "dynamic": "dinamik"}

SUBSETS = [tuple(s) for k in (1, 2, 3) for s in itertools.combinations(OSC, k)]
FSETS = [tuple(s) for k in range(0, len(FILTERS) + 1) for s in itertools.combinations(FILTERS, k)]


# ═════════════════════════ GÖSTERGELER ═════════════════════════
def _rma(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def _ema(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def rsi(c: pd.Series, n: int) -> pd.Series:
    d = c.diff()
    up, dn = _rma(d.clip(lower=0), n), _rma((-d).clip(lower=0), n)
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(100.0).where(dn.notna())


def stoch(h, l, c, n, sm) -> pd.Series:
    ll, hh = l.rolling(n).min(), h.rolling(n).max()
    k = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    return k.rolling(sm).mean()


def wavetrend_norm(h, l, c, n1, n2, scale) -> pd.Series:
    ap = (h + l + c) / 3
    esa = _ema(ap, n1)
    d = _ema((ap - esa).abs(), n1)
    ci = (ap - esa) / (0.015 * d.replace(0, np.nan))
    wt1 = _ema(ci.fillna(0), n2)
    return 50 + 50 * np.tanh(wt1 / scale)


def robust_z(x: pd.Series, n: int) -> pd.Series:
    med = x.rolling(n).median()
    mad = (x - med).abs().rolling(n).median()
    return (x - med.shift(1)) / (1.4826 * mad.shift(1)).replace(0, np.nan)


def features(df: pd.DataFrame) -> dict:
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    f = {
        "R": rsi(c, C.RSI_LEN),
        "S": stoch(h, l, c, C.STOCH_LEN, C.STOCH_SMOOTH),
        "W": wavetrend_norm(h, l, c, C.WT_N1, C.WT_N2, C.WT_SCALE),
        "atr": _rma(tr, C.ATR_LEN),
        "ema": _ema(c, C.TREND_EMA),
        "volZ": robust_z(np.log1p(v.clip(lower=0)), C.SHOCK_LEN),
        "vtyZ": robust_z(np.log(tr.clip(lower=1e-12)), C.SHOCK_LEN),
    }
    f["has_vol"] = bool((v > 0).mean() > 0.5)
    return f


def _bands(x: pd.Series) -> tuple[pd.Series, pd.Series]:
    up = x.rolling(C.DYN_LEN, min_periods=C.DYN_LEN // 2).quantile(C.DYN_PUP / 100).shift(1)
    dn = x.rolling(C.DYN_LEN, min_periods=C.DYN_LEN // 2).quantile(C.DYN_PDN / 100).shift(1)
    return up.clip(*C.DYN_UP_CLIP), dn.clip(*C.DYN_DN_CLIP)


# ═════════════════════════ SİNYALLER ═════════════════════════
def _rollmax(b: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(b.astype(np.int8)).rolling(n, min_periods=1).max().to_numpy().astype(bool)


def build_signals(df: pd.DataFrame, f: dict) -> dict:
    """Dönen: {(subset, mode, fset): (long_mask, short_mask)}"""
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    prev_c = np.r_[np.nan, c[:-1]]
    ev = {}
    for mode in MODES:
        tob, tos, xob, xos = {}, {}, {}, {}
        for k in OSC:
            x = f[k]
            if mode == "static":
                up = pd.Series(C.STATIC_UP, index=x.index)
                dn = pd.Series(C.STATIC_DN, index=x.index)
            else:
                up, dn = _bands(x)
            ob = (x > up).to_numpy() & up.notna().to_numpy()
            os_ = (x < dn).to_numpy() & dn.notna().to_numpy()
            tob[k], tos[k] = _rollmax(ob, C.ARM_BARS), _rollmax(os_, C.ARM_BARS)
            xob[k] = np.r_[False, ob[:-1] & ~ob[1:]]
            xos[k] = np.r_[False, os_[:-1] & ~os_[1:]]
        for s in SUBSETS:
            short = np.logical_and.reduce([tob[k] for k in s]) & np.logical_or.reduce([xob[k] for k in s])
            long_ = np.logical_and.reduce([tos[k] for k in s]) & np.logical_or.reduce([xos[k] for k in s])
            ev[(s, mode)] = (long_, short)

    volS = _rollmax((f["volZ"] >= C.SHOCK_Z).to_numpy(), C.ARM_BARS) if f["has_vol"] else np.ones(len(df), bool)
    vtyS = _rollmax((f["vtyZ"] >= C.SHOCK_Z).to_numpy(), C.ARM_BARS)
    ema = f["ema"].to_numpy()
    fl = {"VOL": volS, "VTY": vtyS, "TREND": c > ema, "CONF": (c > o) & (c > prev_c)}
    fs = {"VOL": volS, "VTY": vtyS, "TREND": c < ema, "CONF": (c < o) & (c < prev_c)}

    out = {}
    for (s, mode), (L, S) in ev.items():
        for fset in FSETS:
            l2, s2 = L.copy(), S.copy()
            for k in fset:
                l2 &= fl[k]
                s2 &= fs[k]
            out[(s, mode, fset)] = (_cooldown(l2), _cooldown(s2))
    return out


def _cooldown(e: np.ndarray) -> np.ndarray:
    """Aynı yönde ARM bar içinde tekrarlanan olayları kümele: yalnızca kümenin ilki."""
    prev = pd.Series(e.astype(np.int8)).shift(1).rolling(C.ARM_BARS, min_periods=1).max().fillna(0).to_numpy().astype(bool)
    return e & ~prev


# ═════════════════════════ ÜÇLÜ BARİYER ═════════════════════════
def barrier_outcomes(df: pd.DataFrame, atr: pd.Series, cost_bps: float) -> dict:
    """Her bar için (sinyal o barda oluşsaydı) LONG ve SHORT net R sonucu."""
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    a = atr.to_numpy()
    n, H = len(c), C.HORIZON
    entry = np.r_[o[1:], np.nan]
    valid = np.isfinite(entry) & np.isfinite(a) & (a > 0)
    valid[max(0, n - H - 1):] = False
    rr = C.TP_ATR / C.SL_ATR
    res = {}
    for side in (1, -1):
        tp = entry + side * C.TP_ATR * a
        sl = entry - side * C.SL_ATR * a
        R = np.full(n, np.nan)
        done = np.zeros(n, bool)
        for k in range(1, H + 1):
            hh = np.r_[h[k:], np.full(k, np.nan)]
            ll = np.r_[l[k:], np.full(k, np.nan)]
            if side == 1:
                hit_sl, hit_tp = (ll <= sl), (hh >= tp)
            else:
                hit_sl, hit_tp = (hh >= sl), (ll <= tp)
            hit_sl &= ~done
            hit_tp &= ~done
            R[hit_sl] = -1.0                     # aynı barda ikisi: muhafazakâr → zarar
            R[hit_tp & ~hit_sl] = rr
            done |= hit_sl | hit_tp
        cH = np.r_[c[H:], np.full(H, np.nan)]
        t = ~done
        R[t] = np.clip(side * (cH[t] - entry[t]) / (C.SL_ATR * a[t]), -1.0, rr)
        cost_R = (cost_bps / 1e4) * entry / (C.SL_ATR * a)
        R = R - cost_R
        R[~valid] = np.nan
        res[side] = R
    res["valid"] = valid
    return res


# ═════════════════════════ İSTATİSTİK ═════════════════════════
def wilson_lb(w: int, n: int, z: float = C.WILSON_Z) -> float:
    if n == 0:
        return 0.0
    p = w / n
    d = 1 + z * z / n
    return (p + z * z / (2 * n) - z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d


def binom_p(w: int, n: int, p0: float) -> float:
    """Tek yönlü: isabet > p0 (normal yaklaşım, süreklilik düzeltmeli)."""
    if n == 0 or p0 <= 0 or p0 >= 1:
        return 1.0
    z = (w - 0.5 - n * p0) / math.sqrt(n * p0 * (1 - p0))
    return 0.5 * math.erfc(z / math.sqrt(2))


def stats(R: np.ndarray, base_wr: float) -> dict:
    R = R[np.isfinite(R)]
    n = len(R)
    if n == 0:
        return {"n": 0, "wr": np.nan, "wlb": 0.0, "exp": np.nan, "pf": np.nan, "base": base_wr, "edge": np.nan, "p": 1.0}
    w = int((R > 0).sum())
    pos, neg = R[R > 0].sum(), -R[R < 0].sum()
    return {
        "n": n, "wr": w / n, "wlb": wilson_lb(w, n), "exp": float(R.mean()),
        "pf": float(pos / neg) if neg > 0 else np.inf, "base": base_wr,
        "edge": w / n - base_wr, "p": binom_p(w, n, base_wr),
    }


def cfg_name(s, mode, fset) -> str:
    osc = "+".join(OSC_NAME[k] for k in s)
    flt = " + ".join(FILTER_NAME[k] for k in fset) if fset else "filtre yok"
    return f"{osc} · {MODE_NAME[mode]} · {flt}"


def evaluate(df: pd.DataFrame, cost_bps: float) -> tuple[pd.DataFrame, dict]:
    """Bir varlık × zaman dilimi için tüm kombinasyonlar. Dönen: (sonuç tablosu, yardımcı veri)."""
    f = features(df)
    sig = build_signals(df, f)
    bo = barrier_outcomes(df, f["atr"], cost_bps)
    n = len(df)
    split = int(n * C.IS_FRACTION)
    is_m = np.zeros(n, bool)
    is_m[:split] = True
    valid = bo["valid"]

    base = {}
    for side in (1, -1):
        for part, m in (("is", is_m), ("oos", ~is_m)):
            r = bo[side][valid & m]
            base[(side, part)] = float((r > 0).mean()) if len(r) else np.nan

    rows = []
    for (s, mode, fset), (L, S) in sig.items():
        row = {"subset": "+".join(s), "mode": mode, "filters": "+".join(fset) or "-", "name": cfg_name(s, mode, fset), "n_osc": len(s), "n_flt": len(fset)}
        for part, m in (("is", is_m), ("oos", ~is_m)):
            Lm, Sm = L & m & valid, S & m & valid
            rl, rs = bo[1][Lm], bo[-1][Sm]
            bl, bs = base[(1, part)], base[(-1, part)]
            st_l, st_s = stats(rl, bl), stats(rs, bs)
            nb = len(rl) + len(rs)
            bb = (len(rl) * bl + len(rs) * bs) / nb if nb else np.nan
            st_b = stats(np.r_[rl, rs], bb)
            for scope, st in (("long", st_l), ("short", st_s), ("both", st_b)):
                for k, v in st.items():
                    row[f"{scope}_{part}_{k}"] = v
        rows.append(row)
    res = pd.DataFrame(rows)
    aux = {"sig": sig, "bo": bo, "valid": valid, "base": base, "split": split, "index": df.index, "has_vol": f["has_vol"]}
    return res, aux


def block_stability(aux: dict, key: tuple, scope: str) -> list[dict]:
    """Seçilen ayarın tüm dönem boyunca N_BLOCKS zaman bloğundaki isabeti ve aynı bloktaki taban isabet."""
    L, S = aux["sig"][key]
    bo, valid = aux["bo"], aux["valid"]
    n = len(valid)
    edges = np.linspace(0, n, C.N_BLOCKS + 1).astype(int)
    out = []
    for i in range(C.N_BLOCKS):
        m = np.zeros(n, bool)
        m[edges[i]:edges[i + 1]] = True
        parts, bases = [], []
        for side, mask in ((1, L), (-1, S)):
            if scope == "long" and side == -1 or scope == "short" and side == 1:
                continue
            r = bo[side][mask & m & valid]
            parts.append(r)
            allr = bo[side][m & valid]
            bases.append((len(r), float((allr > 0).mean()) if len(allr) else np.nan))
        r = np.concatenate(parts) if parts else np.array([])
        nb = sum(k for k, _ in bases)
        bw = sum(k * b for k, b in bases) / nb if nb else np.nan
        st = stats(r, bw)
        out.append({"start": aux["index"][edges[i]], "end": aux["index"][min(edges[i + 1], n) - 1], **st})
    return out


def ablation(res: pd.DataFrame, scope: str = "both") -> dict:
    """Her filtrenin marjinal etkisi: yalnızca o filtrede farklı olan eşleştirilmiş ayar çiftlerinde ortalama Δisabet (tüm dönem, IS+OOS birleşik)."""
    r = res.copy()
    n = r[f"{scope}_is_n"] + r[f"{scope}_oos_n"]
    w = r[f"{scope}_is_wr"].fillna(0) * r[f"{scope}_is_n"] + r[f"{scope}_oos_wr"].fillna(0) * r[f"{scope}_oos_n"]
    r["n_all"], r["wr_all"] = n, w / n.replace(0, np.nan)
    key = r.set_index(["subset", "mode", "filters"])
    out = {}
    for flt in FILTERS + ("DYN",):
        deltas = []
        for (s, mode, fs), row in key.iterrows():
            parts = [] if fs == "-" else fs.split("+")
            if flt == "DYN":
                if mode != "static":
                    continue
                other = (s, "dynamic", fs)
            else:
                if flt in parts:
                    continue
                newf = [k for k in FILTERS if k in parts or k == flt]
                other = (s, mode, "+".join(newf))
            if other not in key.index:
                continue
            o = key.loc[other]
            if row["n_all"] >= C.MIN_TRADES_IS and o["n_all"] >= C.MIN_TRADES_IS:
                deltas.append(o["wr_all"] - row["wr_all"])
        out[flt] = (float(np.mean(deltas)) if deltas else np.nan, len(deltas))
    return out
