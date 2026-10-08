"""v3 PORTFÖY — olay tabanlı (gerçek giriş/çıkış zamanları) çoklu strateji simülasyonu ve risk seçimi.

Kurallar
  • Her finalist aynı anda tek pozisyon (finalist backtest'i zaten çakışmasız)
  • Portföyde aynı anda en fazla PORT_MAX_OPEN pozisyon
  • Aynı kümede (birlikte hareket eden varlıklar: ABD endeksleri / metaller / kripto) en fazla PORT_CLUSTER_MAX pozisyon
  • İşlem riski = giriş anındaki (gerçekleşmiş) kasa × risk oranı; sonuç çıkış anında kasaya yazılır
  • Gün içinde gerçekleşen zarar PORT_DAILY_LIMIT'e ulaşınca o gün yeni işlem açılmaz
Risk seçimi: her risk seviyesi için günlük getiriler blok bootstrap ile 1 yıllık PORT_MC_PATHS yola yeniden örneklenir;
%95 olasılıkla maksimum düşüşün PORT_TARGET_MDD'yi aşmadığı EN YÜKSEK risk önerilir.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C


def combine(finalists: list[dict], only_oos: bool = False) -> pd.DataFrame:
    rows = []
    for e in finalists:
        t = e["trades"]
        if only_oos:
            t = t[t["oos"]]
        if t.empty:
            continue
        rows.append(pd.DataFrame({"entry_time": t["entry_time"].values, "exit_time": t["exit_time"].values, "R": t["R"].values,
                                  "sid": e["id"], "asset": e["asset"], "cluster": C.CLUSTERS.get(e["asset"], e["asset"])}))
    if not rows:
        return pd.DataFrame(columns=["entry_time", "exit_time", "R", "sid", "asset", "cluster"])
    df = pd.concat(rows, ignore_index=True)
    df["entry_time"] = pd.to_datetime(df["entry_time"], utc=True)
    df["exit_time"] = pd.to_datetime(df["exit_time"], utc=True)
    return df.sort_values(["entry_time", "sid"]).reset_index(drop=True)


def simulate(trades: pd.DataFrame, risk: float, max_open: int | None = None, cluster_max: int | None = None,
             daily_limit: float | None = None, dd_steps: list | None = None) -> dict:
    """dd_steps: [(düşüş eşiği, risk çarpanı), ...] — canlı botun risk yöneticisiyle aynı (zirveden düşüşe göre kademeli risk)."""
    max_open = max_open or C.PORT_MAX_OPEN
    cluster_max = cluster_max or C.PORT_CLUSTER_MAX
    daily_limit = C.PORT_DAILY_LIMIT if daily_limit is None else daily_limit
    eq = 1.0
    open_pos: list[dict] = []
    points = []
    taken, skipped = [], {"max_açık": 0, "küme": 0, "günlük_limit": 0}
    day, day_start_eq, day_pnl = None, 1.0, 0.0
    peak = 1.0

    def realize(upto):
        nonlocal eq, open_pos, day, day_start_eq, day_pnl
        due = sorted([p for p in open_pos if p["exit_time"] <= upto], key=lambda p: p["exit_time"])
        for p in due:
            pnl = p["risk_amt"] * p["R"]
            d = p["exit_time"].floor("D")
            if d != day:
                day, day_start_eq, day_pnl = d, eq, 0.0
            eq += pnl
            day_pnl += pnl
            points.append((p["exit_time"], eq))
            open_pos.remove(p)

    for tr in trades.itertuples(index=False):
        realize(tr.entry_time)
        d = tr.entry_time.floor("D")
        if d != day:
            day, day_start_eq, day_pnl = d, eq, 0.0
        if day_pnl <= -daily_limit * day_start_eq:
            skipped["günlük_limit"] += 1
            continue
        if len(open_pos) >= max_open:
            skipped["max_açık"] += 1
            continue
        if sum(1 for p in open_pos if p["cluster"] == tr.cluster) >= cluster_max:
            skipped["küme"] += 1
            continue
        if eq <= 0:
            break
        peak = max(peak, eq)
        scale = 1.0
        for thr, mult in sorted(dd_steps or []):
            if 1 - eq / peak >= thr:
                scale = mult
        if scale <= 0:
            skipped["günlük_limit"] += 1
            continue
        p = {"exit_time": tr.exit_time, "risk_amt": risk * eq * scale, "R": tr.R, "cluster": tr.cluster}
        open_pos.append(p)
        taken.append(tr)
    realize(pd.Timestamp.max.tz_localize("UTC"))
    if not points:
        return {"equity": pd.Series(dtype=float), "taken": pd.DataFrame(taken), "skipped": skipped}
    s = pd.Series([v for _, v in points], index=pd.DatetimeIndex([t for t, _ in points]))
    s = s.groupby(s.index.floor("D")).last()
    start = trades["entry_time"].min().floor("D")
    full = pd.date_range(min(start, s.index[0]), s.index[-1], freq="1D")
    s = s.reindex(full).ffill().fillna(1.0)
    return {"equity": s, "taken": pd.DataFrame(taken), "skipped": skipped}


def metrics(eq: pd.Series, taken: pd.DataFrame) -> dict:
    if eq.empty:
        return {}
    days = max((eq.index[-1] - eq.index[0]).days, 1)
    ret = eq.pct_change().fillna(eq.iloc[0] - 1)
    peak = eq.cummax()
    dd = 1 - eq / peak
    under = (dd > 1e-9).to_numpy()
    longest = cur = 0
    for u in under:
        cur = cur + 1 if u else 0
        longest = max(longest, cur)
    m = eq.resample("ME").last()
    mret = m.pct_change()
    mret.iloc[0] = m.iloc[0] - 1
    sd = ret.std()
    return {
        "total": float(eq.iloc[-1] - 1), "cagr": float(eq.iloc[-1] ** (365.25 / days) - 1) if eq.iloc[-1] > 0 else -1.0,
        "mdd": float(dd.max()), "longest_dd": int(longest), "sharpe": float(ret.mean() / sd * np.sqrt(365)) if sd > 0 else np.nan,
        "pos_months": float((mret > 0).mean()), "n": len(taken), "per_month": len(taken) / (days / 30.44),
        "wr": float((taken["R"] > 0).mean()) if len(taken) else np.nan, "exp": float(taken["R"].mean()) if len(taken) else np.nan,
        "years": days / 365.25, "monthly": mret, "yearly": eq.resample("YE").last().pct_change().fillna(eq.resample("YE").last().iloc[0] - 1),
    }


def monte_carlo(eq: pd.Series, horizon: int = 365, block: int = 10, paths: int | None = None, seed: int = 11) -> dict:
    paths = paths or C.PORT_MC_PATHS
    r = eq.pct_change().dropna().to_numpy()
    if len(r) < 60:
        return {}
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(horizon / block))
    st = rng.integers(0, len(r) - block + 1, size=(paths, nb))
    idx = (st[:, :, None] + np.arange(block)[None, None, :]).reshape(paths, -1)[:, :horizon]
    pth = np.cumprod(1 + r[idx], axis=1)
    peak = np.maximum.accumulate(np.maximum(pth, 1.0), axis=1)
    mdd = (1 - pth / peak).max(axis=1)
    fin = pth[:, -1]
    return {"p95_mdd": float(np.percentile(mdd, 95)), "med_mdd": float(np.median(mdd)), "p_dd20": float((mdd >= 0.2).mean()),
            "p_dd30": float((mdd >= 0.3).mean()), "p_loss": float((fin < 1).mean()), "med_ret": float(np.median(fin) - 1),
            "p5_ret": float(np.percentile(fin, 5) - 1)}


def run(finalists: list[dict]) -> dict:
    if not finalists:
        return {"ok": False, "msg": "finalist yok"}
    trades = combine(finalists)
    trades_oos = combine(finalists, only_oos=True)
    levels = []
    for r in C.PORT_RISKS:
        sim = simulate(trades, r)
        m = metrics(sim["equity"], sim["taken"])
        mc = monte_carlo(sim["equity"])
        so = simulate(trades_oos, r) if len(trades_oos) else None
        mo = metrics(so["equity"], so["taken"]) if so else {}
        levels.append({"risk": r, "m": m, "mc": mc, "skipped": sim["skipped"], "equity": sim["equity"], "oos": mo,
                       "equity_oos": so["equity"] if so else pd.Series(dtype=float)})
    ok = [lv for lv in levels if lv["mc"] and lv["mc"]["p95_mdd"] <= C.PORT_TARGET_MDD and lv["m"].get("exp", -1) > 0]
    rec = max(ok, key=lambda lv: lv["risk"]) if ok else None
    corr = np.nan
    if trades["sid"].nunique() > 1:
        piv = trades.assign(d=trades["exit_time"].dt.floor("D")).pivot_table(index="d", columns="sid", values="R", aggfunc="sum").fillna(0)
        cm = piv.corr().to_numpy()
        corr = float(np.nanmean(cm[~np.eye(len(cm), dtype=bool)]))
    return {"ok": True, "levels": levels, "rec": rec, "corr": corr, "n_strat": len(finalists),
            "span": (trades["entry_time"].min(), trades["exit_time"].max())}


def _p(x):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.1f}"


def render(p: dict) -> list[str]:
    L = ["## Portföy (v3, olay tabanlı)", ""]
    if not p.get("ok"):
        L += [f"> Portföy kurulamadı: {p.get('msg')}", ""]
        return L
    a, b = p["span"]
    L += [f"{p['n_strat']} finalist · {a:%Y-%m-%d} → {b:%Y-%m-%d} · aynı anda en fazla {C.PORT_MAX_OPEN} pozisyon · "
          f"küme başına en fazla {C.PORT_CLUSTER_MAX} (ABD endeksleri / metaller / kripto) · günlük zarar limiti %{100 * C.PORT_DAILY_LIMIT:.0f} · "
          f"stratejiler arası ortalama korelasyon {p['corr']:.2f}", ""]
    rec = p["rec"]
    if rec:
        m, mc = rec["m"], rec["mc"]
        L += [f"### ✅ Önerilen risk: işlem başına kasanın **%{100 * rec['risk']:.2g}**'i",
              f"Bu seviyede Monte Carlo'ya göre 1 yıllık maksimum düşüş %95 olasılıkla **{_p(mc['p95_mdd'])}**'i aşmıyor (hedef ≤ {_p(C.PORT_TARGET_MDD)}). "
              f"Tarihsel: yıllık getiri **{_p(m['cagr'])}**, maksimum düşüş **{_p(m['mdd'])}**, en uzun düşüş {m['longest_dd']} gün, "
              f"pozitif ay oranı {_p(m['pos_months'])}, ayda {m['per_month']:.1f} işlem.", ""]
    else:
        L += [f"> ⚠️ Hiçbir risk seviyesi hedef düşüş sınırını (%95 olasılıkla ≤ {_p(C.PORT_TARGET_MDD)}) karşılamadı. Canlı motor varsayılan riski "
              f"(%{100 * C.LIVE_DEFAULT_RISK:.2g}) kullanır; gerçek parayla işlem önerilmez.", ""]
    L += ["| Risk/işlem | Yıllık getiri | Toplam | Maks. düşüş | En uzun düşüş (gün) | Sharpe | Pozitif ay | İşlem/ay | Atlanan (açık/küme/gün) | "
          "MC %95 maks. düşüş | MC yılı zararla kapama | MC medyan yıllık | MC en kötü %5 | OOS yıllık | OOS maks. düşüş |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for lv in p["levels"]:
        m, mc, o, sk = lv["m"], lv["mc"] or {}, lv["oos"] or {}, lv["skipped"]
        mark = " ◀" if rec is lv else ""
        L.append(f"| %{100 * lv['risk']:.2g}{mark} | {_p(m.get('cagr'))} | {_p(m.get('total'))} | {_p(m.get('mdd'))} | {m.get('longest_dd', '—')} | "
                 f"{m.get('sharpe', float('nan')):.2f} | {_p(m.get('pos_months'))} | {m.get('per_month', 0):.1f} | {sk['max_açık']}/{sk['küme']}/{sk['günlük_limit']} | "
                 f"{_p(mc.get('p95_mdd'))} | {_p(mc.get('p_loss'))} | {_p(mc.get('med_ret'))} | {_p(mc.get('p5_ret'))} | {_p(o.get('cagr'))} | {_p(o.get('mdd'))} |")
    show = rec or p["levels"][0]
    yr = show["m"]["yearly"]
    L += ["", f"### Yıllık getiriler (risk %{100 * show['risk']:.2g})", "", "| " + " | ".join(str(d.year) for d in yr.index) + " |",
          "|" + "---|" * len(yr), "| " + " | ".join(_p(v) for v in yr.values) + " |", ""]
    mm = show["m"]["monthly"].tail(24)
    L += [f"### Son 24 ay (risk %{100 * show['risk']:.2g})", "", "| " + " | ".join(f"{d:%Y-%m}" for d in mm.index) + " |",
          "|" + "---|" * len(mm), "| " + " | ".join(_p(v) for v in mm.values) + " |", ""]
    return L
