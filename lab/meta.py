"""Meta-etiketleme: tüm ailelerin aday olaylarından hangisinin çalışacağını öğrenen gradient boosting.

Dürüstlük kuralları:
  • IS içinde zaman sıralı genişleyen pencere CV → IS istatistikleri katlama DIŞI tahminden gelir
    (model kendi eğitim verisinde ölçülmez; diğer ailelerle adil karşılaştırma)
  • Eğitim ile tahmin arasında HORIZON bar boşluk (etiket sızıntısı yok)
  • Eşik (üst %35) yalnızca IS katlama dışı tahminlerden belirlenir
  • OOS: tüm IS ile eğitilen model, OOS'a hiç dokunmadan tahmin eder
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C
from .strategies import Book


def _matrix(f: dict, idx: pd.DatetimeIndex, fam_l: dict, fam_s: dict, side: int, rows: np.ndarray) -> np.ndarray:
    c, a = f["c"].to_numpy(), f["atr"].to_numpy()
    hh, ll = f["h"].rolling(20).max().to_numpy(), f["l"].rolling(20).min().to_numpy()
    hr = idx.hour.to_numpy() + idx.minute.to_numpy() / 60
    cols = [
        f["R"].to_numpy(), f["S"].to_numpy(), f["W"].to_numpy(), f["rsi2"].to_numpy(),
        f["er"].to_numpy(), f["adx"].to_numpy(), f["volZ"].to_numpy(), f["vtyZ"].to_numpy(),
        (c - f["ema200"].to_numpy()) / a, (c - f["ema50"].to_numpy()) / a,
        f["bbw_pct"].to_numpy(), (c - ll) / np.where(hh - ll > 0, hh - ll, np.nan), f["ret_z"].to_numpy(),
        np.sin(2 * np.pi * hr / 24), np.cos(2 * np.pi * hr / 24), idx.dayofweek.to_numpy().astype(float),
    ]
    X = np.column_stack(cols)[rows]
    if side == -1:  # yönden bağımsız temsil: SHORT için yön duyarlı özellikleri çevir
        for j in (0, 1, 2, 3):
            X[:, j] = 100 - X[:, j]
        for j in (8, 9, 12):
            X[:, j] = -X[:, j]
        X[:, 11] = 1 - X[:, 11]
    fams = sorted(fam_l)
    F = np.column_stack([(fam_l if side == 1 else fam_s)[k][rows] for k in fams]).astype(float)
    return np.column_stack([X, F, F.sum(axis=1), np.full(len(rows), side, float)])


def add_meta(book: Book, f: dict, idx: pd.DatetimeIndex, R_by_side: dict, valid: np.ndarray, split: int) -> str | None:
    try:
        from sklearn.ensemble import HistGradientBoostingClassifier
    except ImportError:
        return "scikit-learn yok"
    n = len(idx)
    fam_l, fam_s = {}, {}
    for _, (fam, L, S) in book.items.items():
        fam_l[fam] = fam_l.get(fam, np.zeros(n, bool)) | L
        fam_s[fam] = fam_s.get(fam, np.zeros(n, bool)) | S
    rows_l = np.flatnonzero(np.logical_or.reduce(list(fam_l.values())) & valid)
    rows_s = np.flatnonzero(np.logical_or.reduce(list(fam_s.values())) & valid)
    X = np.vstack([_matrix(f, idx, fam_l, fam_s, 1, rows_l), _matrix(f, idx, fam_l, fam_s, -1, rows_s)])
    y = np.r_[R_by_side[1][rows_l], R_by_side[-1][rows_s]] > 0
    bar = np.r_[rows_l, rows_s]
    side = np.r_[np.ones(len(rows_l)), -np.ones(len(rows_s))]
    ok = np.isfinite(np.r_[R_by_side[1][rows_l], R_by_side[-1][rows_s]])
    X, y, bar, side = X[ok], y[ok], bar[ok], side[ok]
    is_ev = bar < split
    if is_ev.sum() < 400:
        return "yetersiz aday"

    def model():
        return HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=200,
                                              l2_regularization=1.0, min_samples_leaf=50, random_state=7)

    # IS: genişleyen pencere, katlama dışı tahmin
    is_bars = np.sort(np.unique(bar[is_ev]))
    edges = np.quantile(is_bars, np.linspace(0, 1, C.META_FOLDS + 1)).astype(int)
    p = np.full(len(bar), np.nan)
    for k in range(1, C.META_FOLDS):
        lo, hi = edges[k], edges[k + 1] if k + 1 < C.META_FOLDS else split
        tr = bar < lo - C.HORIZON
        te = (bar >= lo) & (bar < hi)
        if tr.sum() < 300 or te.sum() == 0 or y[tr].all() or not y[tr].any():
            continue
        m = model().fit(X[tr], y[tr])
        p[te] = m.predict_proba(X[te])[:, 1]
    oof = p[is_ev & np.isfinite(p)]
    if len(oof) < 100:
        return "yetersiz katlama dışı tahmin"
    thr = np.quantile(oof, 1 - C.META_KEEP)
    tr = bar < split - C.HORIZON
    m = model().fit(X[tr], y[tr])
    te = bar >= split
    if te.any():
        p[te] = m.predict_proba(X[te])[:, 1]
    take = np.isfinite(p) & (p >= thr)
    L, S = np.zeros(n, bool), np.zeros(n, bool)
    L[bar[take & (side == 1)]] = True
    S[bar[take & (side == -1)]] = True
    book.add("META", f"gradient boosting · tüm adaylar · üst %{int(C.META_KEEP * 100)}", L, S, 1)
    return None
