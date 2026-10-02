"""Portföy ve iflas riski modülü.

1) ADAY TOPLAMA: her varlık × ZD değerlendirmesinden, IS'te pozitif beklentili en sağlam (t-istatistiği yüksek)
   ilk K ayarın işlem listesi saklanır (bellek dostu: yalnızca işlem zamanı + R).
2) SEÇİM (yalnızca IS): t ≥ PORT_MIN_T; varlık başına en fazla PORT_PER_ASSET, aynı varlıkta aynı aile bir kez,
   toplam en fazla PORT_MAX strateji.
3) SİMÜLASYON: her işlemde kasanın sabit %'si riske atılır (bileşik), günlük zarar limiti dolunca o gün durulur.
4) MONTE CARLO: OOS günlük getirileri blok bootstrap ile 1 yıllık binlerce yola yeniden örneklenir →
   kasanın %20/%30/%50 düşme olasılığı, yılı zararla kapama olasılığı, toparlanma süresi.
Not: eşzamanlı açık işlemler aynı kasa üzerinden ayrı ayrı riske edilir (yaklaşım); işlem sonucu giriş anında
işlenir — günlük limit kontrolü bu yüzden hafif iyimserdir.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import config as C
from . import evaluate as EV


def _tstat(row: pd.Series, sc: str) -> float:
    e, lb = row[f"{sc}_is_exp"], row[f"{sc}_is_lb"]
    se = (e - lb) / 1.96 if np.isfinite(lb) else np.nan
    return float(e / se) if se and se > 0 else -np.inf


def collect(res: pd.DataFrame, aux: dict, asset: str, tf: str, k: int = 6) -> list[dict]:
    """IS'e göre en sağlam K ayar (her girişin yalnızca en iyi çıkışı) → işlem listeleri."""
    cands = []
    for sc in EV.SCOPES:
        r = res[(res[f"{sc}_is_n"] >= C.MIN_TRADES_IS) & (res[f"{sc}_is_exp"] > 0) & ~EV.suspect(res, sc, "is")]
        for _, row in r.iterrows():
            cands.append((_tstat(row, sc), sc, row))
    cands.sort(key=lambda x: -x[0])
    out, seen = [], set()
    for t, sc, row in cands:
        if row["entry"] in seen:
            continue
        seen.add(row["entry"])
        tp = EV.trade_path(aux, row, sc)
        out.append({
            "asset": asset, "tf": tf, "family": row["family"], "entry": row["entry"], "exit": row["exit"], "scope": sc,
            "t_is": t, "is_exp": row[f"{sc}_is_exp"], "is_n": int(row[f"{sc}_is_n"]),
            "oos_exp": row[f"{sc}_oos_exp"], "oos_n": int(row[f"{sc}_oos_n"]), "oos_wr": row[f"{sc}_oos_wr"],
            "oos_start": aux["span"]["oos"][0], "trades": tp[["time", "R", "oos"]].reset_index(drop=True),
        })
        if len(out) >= k:
            break
    return out


def select(cands: list[dict]) -> list[dict]:
    pool = sorted([c for c in cands if c["t_is"] >= C.PORT_MIN_T], key=lambda c: -c["t_is"])
    sel, per_asset, fam_seen = [], {}, set()
    for c in pool:
        if per_asset.get(c["asset"], 0) >= C.PORT_PER_ASSET or (c["asset"], c["family"]) in fam_seen:
            continue
        sel.append(c)
        per_asset[c["asset"]] = per_asset.get(c["asset"], 0) + 1
        fam_seen.add((c["asset"], c["family"]))
        if len(sel) >= C.PORT_MAX:
            break
    return sel


def simulate(trades: pd.DataFrame, risk: float, daily_limit: float) -> tuple[pd.Series, pd.DataFrame]:
    """Bileşik sabit oranlı risk + günlük zarar limiti. Dönen: günlük kasa serisi, alınan işlemler."""
    t = trades.sort_values("time").reset_index(drop=True)
    eq, day, day_pnl = 1.0, None, 0.0
    taken = np.zeros(len(t), bool)
    eq_after = np.empty(len(t))
    for i, (tm, R) in enumerate(zip(t["time"], t["R"])):
        d = tm.floor("D")
        if d != day:
            day, day_pnl = d, 0.0
        if day_pnl <= -daily_limit:
            eq_after[i] = eq
            continue
        pnl = risk * R
        eq *= (1 + pnl)
        day_pnl += pnl
        taken[i] = True
        eq_after[i] = eq
    t["equity"] = eq_after
    t["taken"] = taken
    if t.empty:
        return pd.Series(dtype=float), t
    daily = t.set_index("time")["equity"].resample("1D").last()
    full = pd.date_range(daily.index[0], daily.index[-1], freq="1D")
    daily = daily.reindex(full).ffill()
    return daily, t


def drawdown_stats(eq: pd.Series) -> dict:
    if eq.empty:
        return {"mdd": np.nan, "longest_dd_days": np.nan}
    peak = eq.cummax()
    dd = 1 - eq / peak
    under = dd > 1e-9
    longest, cur = 0, 0
    for u in under.to_numpy():
        cur = cur + 1 if u else 0
        longest = max(longest, cur)
    return {"mdd": float(dd.max()), "longest_dd_days": int(longest)}


def monte_carlo(daily_ret: np.ndarray, n_paths: int = 2000, horizon: int = 365, block: int = 5, seed: int = 11) -> dict:
    r = daily_ret[np.isfinite(daily_ret)]
    if len(r) < 30:
        return {}
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(horizon / block))
    starts = rng.integers(0, len(r) - block + 1, size=(n_paths, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n_paths, -1)[:, :horizon]
    paths = np.cumprod(1 + r[idx], axis=1)
    peak = np.maximum.accumulate(np.maximum(paths, 1.0), axis=1)
    mdd = (1 - paths / peak).max(axis=1)
    final = paths[:, -1]
    rec = []
    for p, pk in zip(paths[:400], peak[:400]):
        under = p < pk - 1e-12
        longest, cur = 0, 0
        for u in under:
            cur = cur + 1 if u else 0
            longest = max(longest, cur)
        rec.append(longest)
    return {
        "p_dd20": float((mdd >= 0.20).mean()), "p_dd30": float((mdd >= 0.30).mean()), "p_dd50": float((mdd >= 0.50).mean()),
        "p_loss_year": float((final < 1).mean()), "median_ret": float(np.median(final) - 1),
        "p5_ret": float(np.percentile(final, 5) - 1), "median_mdd": float(np.median(mdd)),
        "median_longest_dd": float(np.median(rec)),
    }


def run(cands: list[dict]) -> dict:
    sel = select(cands)
    if not sel:
        return {"selected": [], "msg": f"IS'te t ≥ {C.PORT_MIN_T} olan aday yok"}
    # her strateji yalnızca kendi OOS döneminde işlem yapar (hepsi seçimde görülmemiş veri);
    # 1h/4h stratejilerinin OOS'u daha uzun olduğu için pencere en erken OOS başlangıcından açılır
    oos_start = min(c["oos_start"] for c in sel)
    late = sorted({f"{c['tf']}" for c in sel if c["oos_start"] > oos_start + pd.Timedelta(days=30)})
    rows = []
    for i, c in enumerate(sel):
        t = c["trades"].copy()
        t["sid"] = i
        rows.append(t)
    allt = pd.concat(rows, ignore_index=True)
    is_t = allt[~allt["oos"]]
    oos_t = allt[allt["oos"] & (allt["time"] >= oos_start)]

    # strateji korelasyonu (OOS günlük R toplamları)
    piv = oos_t.assign(d=oos_t["time"].dt.floor("D")).pivot_table(index="d", columns="sid", values="R", aggfunc="sum").fillna(0)
    cm = piv.corr().to_numpy() if piv.shape[1] > 1 else np.array([[1.0]])
    off = cm[~np.eye(len(cm), dtype=bool)]
    avg_corr = float(np.nanmean(off)) if off.size else np.nan

    out = {"selected": sel, "oos_start": oos_start, "late": late, "avg_corr": avg_corr, "levels": []}
    for risk in C.PORT_RISKS:
        lv = {"risk": risk}
        for part, t in (("is", is_t), ("oos", oos_t)):
            daily, tk = simulate(t, risk, C.PORT_DAILY_LIMIT)
            taken = tk[tk["taken"]] if len(tk) else tk
            days = max((daily.index[-1] - daily.index[0]).days, 1) if len(daily) else 1
            dr = daily.pct_change().fillna(daily.iloc[0] - 1 if len(daily) else 0).to_numpy() if len(daily) else np.array([])
            mret = daily.resample("ME").last().pct_change() if len(daily) > 31 else pd.Series(dtype=float)
            lv[part] = {
                "n": len(taken), "per_day": len(taken) / days, "wr": float((taken["R"] > 0).mean()) if len(taken) else np.nan,
                "exp": float(taken["R"].mean()) if len(taken) else np.nan,
                "total": float(daily.iloc[-1] - 1) if len(daily) else np.nan,
                "cagr": float(daily.iloc[-1] ** (365 / days) - 1) if len(daily) and daily.iloc[-1] > 0 else np.nan,
                "pos_days": float((dr[dr != 0] > 0).mean()) if (dr != 0).any() else np.nan,
                "pos_months": float((mret.dropna() > 0).mean()) if len(mret.dropna()) else np.nan,
                "days": days, **drawdown_stats(daily),
            }
            if part == "oos":
                lv["mc"] = monte_carlo(dr)
                lv["equity"] = daily
        out["levels"].append(lv)
    return out


def render(p: dict) -> list[str]:
    L = ["## Portföy (IS'te seçilen stratejilerin birlikte çalışması)", ""]
    if not p.get("selected"):
        L += [f"> {p.get('msg', 'Portföy kurulamadı')}", ""]
        return L
    pc = lambda x: "—" if x is None or not np.isfinite(x) else f"%{100 * x:.1f}"
    rr = lambda x: "—" if x is None or not np.isfinite(x) else f"{x:+.3f}R"
    L += [f"Seçim kuralı (yalnızca IS): IS beklentisi > 0, t ≥ {C.PORT_MIN_T}, varlık başına en fazla {C.PORT_PER_ASSET}, aynı varlıkta aynı aile bir kez, "
          f"toplam en fazla {C.PORT_MAX}. OOS penceresi: **{p['oos_start']:%Y-%m-%d} → bugün** "
          f"(her strateji yalnızca kendi OOS döneminde işlem yapar{'; ' + '/'.join(p['late']) + ' stratejileri kısa geçmiş nedeniyle sonradan katılır' if p['late'] else ''}). "
          f"Stratejiler arası ortalama günlük korelasyon: **{p['avg_corr']:.2f}** (0'a yakın = iyi çeşitlendirme).", "",
          "| # | Varlık | ZD | Yön | Giriş | Çıkış | IS t | IS beklenti (n) | OOS beklenti (n) | OOS isabet |", "|---|---|---|---|---|---|---|---|---|---|"]
    sc_tr = {"both": "iki yön", "long": "LONG", "short": "SHORT"}
    for i, c in enumerate(p["selected"], 1):
        L.append(f"| {i} | {c['asset']} | {c['tf']} | {sc_tr[c['scope']]} | {c['entry']} | {c['exit']} | {c['t_is']:.2f} | {rr(c['is_exp'])} ({c['is_n']}) | "
                 f"{rr(c['oos_exp'])} ({c['oos_n']}) | {pc(c['oos_wr'])} |")
    # yıllık kararlılık: her stratejinin yıl bazında ortalama R'si (boş = o yıl işlem/veri yok)
    yrs = sorted({y for c in p["selected"] for y in c["trades"]["time"].dt.year.unique()})
    L += ["", "### Yıllık kararlılık — strateji başına yıl yıl ortalama R (boş hücre = o yıl işlem veya veri yok)", "",
          "| # | " + " | ".join(str(y) for y in yrs) + " |", "|---|" + "---|" * len(yrs)]
    for i, c in enumerate(p["selected"], 1):
        g = c["trades"].groupby(c["trades"]["time"].dt.year)["R"].mean()
        L.append(f"| {i} | " + " | ".join(("" if y not in g.index else f"{g[y]:+.2f}") for y in yrs) + " |")
    L += ["", f"### Portföy performansı — işlem başına sabit risk, günlük zarar limiti %{100 * C.PORT_DAILY_LIMIT:.0f}", "",
          "| Risk/işlem | Dönem | İşlem/gün | İsabet | Beklenti | Toplam getiri | Yıllık | Maks. düşüş | En uzun düşüş (gün) | Pozitif gün | Pozitif ay |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for lv in p["levels"]:
        for part, nm in (("is", "IS"), ("oos", "**OOS**")):
            m = lv[part]
            L.append(f"| %{100 * lv['risk']:.2g} | {nm} | {m['per_day']:.2f} | {pc(m['wr'])} | {rr(m['exp'])} | {pc(m['total'])} | {pc(m['cagr'])} | "
                     f"{pc(m['mdd'])} | {m['longest_dd_days']} | {pc(m['pos_days'])} | {pc(m['pos_months'])} |")
    L += ["", "### Monte Carlo — OOS günlük getirilerinden 2.000 adet 1 yıllık yol (5 günlük blok bootstrap)", "",
          "| Risk/işlem | Medyan yıllık getiri | En kötü %5 senaryo | Yılı zararla kapama | Kasa %20 düşer | %30 düşer | %50 düşer | Medyan maks. düşüş | Medyan en uzun düşüş (gün) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for lv in p["levels"]:
        m = lv.get("mc") or {}
        if not m:
            L.append(f"| %{100 * lv['risk']:.2g} | yetersiz OOS günü | | | | | | | |")
            continue
        L.append(f"| %{100 * lv['risk']:.2g} | {pc(m['median_ret'])} | {pc(m['p5_ret'])} | {pc(m['p_loss_year'])} | {pc(m['p_dd20'])} | {pc(m['p_dd30'])} | "
                 f"{pc(m['p_dd50'])} | {pc(m['median_mdd'])} | {m['median_longest_dd']:.0f} |")
    L += ["", "> Okuma: OOS beklentisi eksiyse risk seviyesi ne olursa olsun kasa uzun vadede erir — sabit oranlı risk yalnızca erimeyi yavaşlatır. "
          "OOS pozitifse, kasanın %30 düşme olasılığı kabul edilebilir düzeyde olan en yüksek risk seviyesi seçilir.", ""]
    return L
