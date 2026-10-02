"""Giriş × çıkış × yön istatistikleri ve seçim."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from . import config as C
from . import exits as X
from . import features as FE
from . import meta as M
from . import strategies as ST

SCOPES = ("both", "long", "short")


def _p_gt0(R: np.ndarray) -> float:
    """Tek yönlü: ortalama R > 0 (t yaklaşımı)."""
    n = len(R)
    if n < 3:
        return 1.0
    sd = R.std(ddof=1)
    if sd == 0:
        return 0.0 if R.mean() > 0 else 1.0
    t = R.mean() / (sd / math.sqrt(n))
    return 0.5 * math.erfc(t / math.sqrt(2))


def stats(R: np.ndarray, months: float, base_wr: float) -> dict:
    R = R[np.isfinite(R)]
    n = len(R)
    if n == 0:
        return {"n": 0, "wr": np.nan, "exp": np.nan, "lb": -np.inf, "pf": np.nan, "pm": 0.0, "p": 1.0, "edge": np.nan}
    m = float(R.mean())
    sd = float(R.std(ddof=1)) if n > 1 else 0.0
    pos, neg = R[R > 0].sum(), -R[R < 0].sum()
    wr = float((R > 0).mean())
    return {
        "n": n, "wr": wr, "exp": m, "lb": m - 1.96 * sd / math.sqrt(n) if n > 1 else -np.inf,
        "pf": float(pos / neg) if neg > 0 else np.inf, "pm": n / max(months, 1e-9), "p": _p_gt0(R),
        "edge": wr - base_wr,
    }


def evaluate(df: pd.DataFrame, cost_bps: float, tf_min: int, partner: pd.Series | None, pname: str,
             funding: pd.Series | None) -> tuple[pd.DataFrame, dict]:
    n = len(df)
    split = int(n * C.IS_FRACTION)
    is_mask = np.zeros(n, bool)
    is_mask[:split] = True
    f = FE.compute(df)
    book = ST.build_all(df, f, tf_min, is_mask, partner, pname, funding)
    sims = X.simulate_all(df, f["atr"], cost_bps)
    valid = sims[next(iter(sims))]["valid"]
    meta_msg = None
    if C.META_ON:
        meta_msg = M.add_meta(book, f, df.index, sims[C.META_EXIT], valid, split)

    span = {"is": (df.index[0], df.index[split - 1]), "oos": (df.index[split], df.index[-1])}
    months = {k: max((b - a).days / 30.44, 0.1) for k, (a, b) in span.items()}
    base = {}
    for ex, sm in sims.items():
        for side in (1, -1):
            for part, m in (("is", is_mask), ("oos", ~is_mask)):
                r = sm[side][valid & m]
                base[(ex, side, part)] = float((r > 0).mean()) if len(r) else np.nan

    rows = []
    for name, (fam, L, S) in book.items.items():
        il, is_ = np.flatnonzero(L & valid), np.flatnonzero(S & valid)
        parts = {"is": (il[il < split], is_[is_ < split]), "oos": (il[il >= split], is_[is_ >= split])}
        for ex, sm in sims.items():
            row = {"family": fam, "entry": name, "exit": ex}
            for part, (pl, ps) in parts.items():
                rl, rs = sm[1][pl], sm[-1][ps]
                bl, bs = base[(ex, 1, part)], base[(ex, -1, part)]
                nb = len(rl) + len(rs)
                bb = (len(rl) * bl + len(rs) * bs) / nb if nb else np.nan
                for sc, r, b in (("long", rl, bl), ("short", rs, bs), ("both", np.r_[rl, rs], bb)):
                    for k, v in stats(r, months[part], b).items():
                        row[f"{sc}_{part}_{k}"] = v
            rows.append(row)
    res = pd.DataFrame(rows)
    aux = {"book": book, "sims": sims, "valid": valid, "split": split, "index": df.index, "span": span,
           "months": months, "meta": meta_msg, "n_entries": len(book.items)}
    return res, aux


def pick(res: pd.DataFrame, scope: str, mask: pd.Series | None = None) -> pd.Series | None:
    """IS'te seç: yeterli işlem + pozitif beklenti; beklentinin %95 alt sınırını maksimize et."""
    r = res if mask is None else res[mask]
    n, e = r[f"{scope}_is_n"], r[f"{scope}_is_exp"]
    el = r[(n >= C.MIN_TRADES_IS) & (e > 0)]
    if el.empty:
        el = r[n >= C.MIN_TRADES_IS]
    if el.empty:
        return None
    return el.loc[el[f"{scope}_is_lb"].idxmax()]


def verdict(row: pd.Series, sc: str, k: int = 1) -> str:
    """k: aynı tabloda yapılan OOS test sayısı → Bonferroni düzeltmesi (çoklu test şansını cezalandırır)."""
    n, e, p = row[f"{sc}_oos_n"], row[f"{sc}_oos_exp"], row[f"{sc}_oos_p"]
    if n < C.MIN_TRADES_OOS or not np.isfinite(e):
        return "⏳ OOS yetersiz"
    if e > 0 and p < 0.05 / max(k, 1) and n >= 2 * C.MIN_TRADES_OOS:
        return "✅ Kanıtlı"
    if e > 0:
        return "⚠️ Pozitif, anlamsız"
    return "❌ OOS'ta tutmadı"


def trade_path(aux: dict, row: pd.Series, sc: str) -> pd.DataFrame:
    """Seçilen ayarın tüm işlemleri (zaman sıralı) — kararlılık ve düşüş analizi için."""
    _, L, S = aux["book"].items[row["entry"]]
    sm, valid = aux["sims"][row["exit"]], aux["valid"]
    parts = []
    if sc in ("both", "long"):
        i = np.flatnonzero(L & valid)
        parts.append(pd.DataFrame({"bar": i, "R": sm[1][i], "side": 1}))
    if sc in ("both", "short"):
        i = np.flatnonzero(S & valid)
        parts.append(pd.DataFrame({"bar": i, "R": sm[-1][i], "side": -1}))
    t = pd.concat(parts).sort_values("bar")
    t["time"] = aux["index"][t["bar"].to_numpy()]
    t["oos"] = t["bar"] >= aux["split"]
    return t.dropna(subset=["R"])


def max_dd(R: np.ndarray) -> float:
    if len(R) == 0:
        return np.nan
    eq = np.cumsum(R)
    return float((np.maximum.accumulate(np.r_[0, eq])[1:] - eq).max())
