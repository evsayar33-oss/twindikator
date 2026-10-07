"""ATVS v4 — ENDEKS ARAŞTIRMASI ve 3. VARLIK SEÇİMİ

  1) Bitget gerçekçi maliyetiyle mevcut finalistler (XAU, ETH) yeniden ölçülür.
  2) NQ (QQQ) ve SPX (SPY) için ABD seansına göre günlük strateji uzayı (10 aile, MACD kombinasyonları dahil) taranır.
  3) Kapılar: IS t ≥ 2 → OOS (Benjamini–Hochberg) → tüm dönem → maliyet ×2 → komşu parametreler → yıllar → veri şüphesi.
  4) Geçen her aday, MEVCUT portföye eklenerek Monte Carlo ile test edilir:
       amaç = yıllık getiri (CAGR) en yüksek; kısıt = %95 olasılıkla maks. düşüş ≤ hedef ve OOS dönemde de iyileşme.
  5) Çıktı: reports/ENDEKS_RAPOR.md, reports/endeks_*.csv, state/endeks_finalist.json (bot bunu okur).

Kullanım:  python run_endeks.py [--sentetik] [--hedef 0.15]
"""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from lab import config as C
from lab import data as D
from lab import finalists as FN
from lab import index_lab as IL
from lab import portfolio as PF

LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def r_(x, d=3):
    return "—" if x is None or not np.isfinite(x) else f"{x:+.{d}f}R"


def p_(x, d=1):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.{d}f}"


# ───────────────────────── veri ─────────────────────────
def load_1h(asset: str, synth: bool, seed: int = 0) -> pd.DataFrame:
    if synth:
        from run_lab import synthetic
        df = synthetic("1h", 12, seed)
        if asset in C.IDX_ASSETS:                          # hafta sonlarını çıkar (endeks seans yapısı)
            loc = df.index.tz_convert(C.IDX_TZ)
            df = df[~((loc.dayofweek == 5) | ((loc.dayofweek == 6) & (loc.hour < 18)) | ((loc.dayofweek == 4) & (loc.hour >= 17)))]
        return df
    raw, src = D.load(asset, "1h", refresh=True)
    df, rep = D.validate(asset, "1h", raw)
    log(f"  {asset}: {len(df)} saatlik mum · {df.index[0]:%Y-%m} → {df.index[-1]:%Y-%m} · kaynak {src} · doğrulama {rep.get('status')}")
    return df


# ───────────────────────── 1) mevcut finalistler, Bitget maliyetiyle ─────────────────────────
def base_finalists(h_by_asset: dict, fin_meta: dict) -> list[dict]:
    out = []
    for fz in fin_meta.get("finalistler", []):
        a = fz["asset"]
        if a not in h_by_asset:
            continue
        df = D.resample(h_by_asset[a], C.TIMEFRAMES[fz["tf"]]["rule"]) if fz["tf"] != "1h" else h_by_asset[a]
        res = {}
        for label, cost in (("eski", C.ASSETS[a]["cost_bps"]), ("bitget", C.bitget_cost_bps(a))):
            old = C.ASSETS[a]["cost_bps"]
            C.ASSETS[a]["cost_bps"] = cost
            try:
                dc = FN.DataCtx(a, fz["tf"], df, None, "", None)
                r = FN.run_spec(dc, fz["entry"], fz["exit_cfg"], fz["scope"])
            finally:
                C.ASSETS[a]["cost_bps"] = old
            t = r["trades"].copy() if r else pd.DataFrame()
            if label == "bitget" and len(t):                     # fonlama: tutulan gün × günlük oran (R cinsinden)
                f, _, _ = dc.book(FN.family_of(fz["entry"]), {})
                e = df["open"].to_numpy()[t["bar"].to_numpy() + 1]
                dist = fz["exit_cfg"]["sl_atr"] * f["atr"].to_numpy()[t["bar"].to_numpy()]
                days = (t["exit_time"] - t["entry_time"]).dt.total_seconds().to_numpy() / 86400
                t["R"] = t["R"] - (C.BITGET_FUNDING_BPS_DAY / 1e4) * days * e / dist
            res[label] = t
        tb = res["bitget"]
        st_old, st_new = FN.trade_stats(res["eski"]["R"]), FN.trade_stats(tb["R"])
        st_oos = FN.trade_stats(tb.loc[tb["oos"], "R"]) if len(tb) else FN.trade_stats([])
        out.append({"id": fz["id"], "asset": a, "tf": fz["tf"], "entry": fz["entry"], "exit": fz["exit"], "scope": fz["scope"],
                    "trades": tb, "old": st_old, "new": st_new, "oos": st_oos})
        log(f"  {fz['id']}: eski maliyet {r_(st_old['exp'])} → Bitget {r_(st_new['exp'])} (OOS {r_(st_oos['exp'])}, {st_new['n']} işlem)")
    return out


# ───────────────────────── 2–3) endeks taraması + kapılar ─────────────────────────
def scan(cx: IL.Ctx) -> list[dict]:
    rows = []
    for s in IL.all_specs(cx.asset):
        t = IL.run_spec(cx, s)
        ins = IL.stats(t.loc[~t["oos"], "R"]) if len(t) else IL.stats([])
        rows.append({"spec": s, "trades": t, "ins": ins})
    return rows


def gates(cx: IL.Ctx, e: dict) -> dict:
    s, t = e["spec"], e["trades"]
    full, oos = IL.stats(t["R"]), IL.stats(t.loc[t["oos"], "R"])
    base = IL.random_base(cx, s)
    alpha = oos["exp"] - base if np.isfinite(base) else np.nan
    e.update(full=full, oos=oos, alpha=alpha, years_pos=IL.year_pos(t))
    g = {"K1 OOS": None,
         "K2 tüm dönem": bool(full["n"] >= C.GATE_FULL_N and full["exp"] > 0),
         "K3 maliyet×2": None, "K4 komşular": None,
         "K5 yıllar": bool(np.isfinite(e["years_pos"]) and e["years_pos"] >= C.GATE_YEARS_POS),
         "K6 veri": bool(full["exp"] <= C.SUSPECT_EXP and full["wr"] <= C.IDX_SUSPECT_WR)}
    e["k1_raw"] = bool(oos["n"] >= C.GATE_OOS_N and oos["exp"] > 0 and np.isfinite(alpha) and alpha > 0)
    e["gates"] = g
    return e


def robust(cx: IL.Ctx, e: dict) -> dict:
    s, g = e["spec"], e["gates"]
    c2 = IL.stats(IL.run_spec(cx, s, cost_mult=C.GATE_COST_MULT)["R"])
    e["cost2"] = c2
    g["K3 maliyet×2"] = bool(np.isfinite(c2["exp"]) and c2["exp"] > 0)
    nb = []
    for label, ns in IL.neighbors(s):
        st = IL.stats(IL.run_spec(cx, ns)["R"])
        nb.append({"komşu": label, "n": st["n"], "exp": st["exp"]})
    nb = pd.DataFrame(nb)
    ok = nb[nb["n"] >= 20]
    e["neighbors"] = nb
    e["neighbor_pos"] = float((ok["exp"] > 0).mean()) if len(ok) else np.nan
    g["K4 komşular"] = bool(np.isfinite(e["neighbor_pos"]) and e["neighbor_pos"] >= C.GATE_NEIGHBOR_POS)
    e["passed"] = all(v is True for v in g.values())
    return e


# ───────────────────────── 4) portföy katkısı ─────────────────────────
def strat_frame(sid: str, asset: str, t: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"entry_time": pd.to_datetime(t["entry_time"], utc=True), "exit_time": pd.to_datetime(t["exit_time"], utc=True),
                         "R": t["R"].to_numpy(float), "oos": t["oos"].to_numpy(bool), "sid": sid, "asset": asset,
                         "cluster": C.CLUSTERS.get(asset, asset)})


def port_eval(frames: dict, risks: dict, start=None) -> dict:
    parts = []
    for sid, fr in frames.items():
        r = risks.get(sid, 0.0)
        if r <= 0:
            continue
        x = fr if start is None else fr[fr["entry_time"] >= start]
        if len(x):
            parts.append(x.assign(R=x["R"] * r))
    if not parts:
        return {}
    tr = pd.concat(parts).sort_values(["entry_time", "sid"]).reset_index(drop=True)
    sim = PF.simulate(tr, 1.0)
    if sim["equity"].empty:
        return {}
    m = PF.metrics(sim["equity"], sim["taken"])
    mc = PF.monte_carlo(sim["equity"])
    return {"m": m, "mc": mc, "eq": sim["equity"]}


def optimise(frames: dict, fixed: dict, free: list[str], target: float, oos_start) -> list[dict]:
    """fixed: risk sabit stratejiler · free: risk ızgarada aranan stratejiler. Kısıt: MC p95 düşüş ≤ hedef."""
    res = []
    for combo in __import__("itertools").product(C.IDX_RISK_GRID, repeat=len(free)):
        risks = {**fixed, **dict(zip(free, combo))}
        if all(v <= 0 for v in risks.values()):
            continue
        ev = port_eval(frames, risks)
        if not ev or not ev["mc"]:
            continue
        evo = port_eval(frames, risks, start=oos_start)
        res.append({"risks": risks, "cagr": ev["m"]["cagr"], "mdd": ev["m"]["mdd"], "p95": ev["mc"]["p95_mdd"],
                    "sharpe": ev["m"]["sharpe"], "n_month": ev["m"]["per_month"], "eq": ev["eq"],
                    "oos_cagr": evo["m"]["cagr"] if evo else np.nan, "oos_mdd": evo["m"]["mdd"] if evo else np.nan,
                    "ok": ev["mc"]["p95_mdd"] <= target})
    return res


# ───────────────────────── kurallar (insan dili) ─────────────────────────
def rules_text(s: dict) -> str:
    F = IL.FAMILIES[s["fam"]]
    par = ", ".join(f"{k}={v}" for k, v in s["p"].items())
    sym = C.IDX_SYMBOL.get(s["asset"], s["asset"]).split("/")[0]
    return (f"**{s['asset']} ({sym}) · günlük · yalnız LONG** — Her işlem günü New York saatiyle 15:00'te bakılır. "
            f"Giriş koşulu: {F['desc']} ({par}){', ve kapanış SMA(200) üstünde' if s['trend'] else ''}. "
            f"Giriş: 15:00 ET'de piyasadan. Stop (borsada): giriş − {s['k']} × günlük ATR(14). "
            f"Çıkış: sonraki günlerin 15:00 kontrolünde {IL.EXIT_DESC[s['exit']]} olursa ya da {s['tmax']} işlem günü dolunca piyasadan. "
            f"Hedef emri yok.")


# ───────────────────────── ana akış ─────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentetik", action="store_true")
    ap.add_argument("--hedef", type=float, default=C.IDX_TARGET_MDD)
    ap.add_argument("--finalist", default=os.path.join(C.LIVE_STATE_DIR, "finalists.json"))
    a = ap.parse_args()
    t0 = time.time()
    log(f"═══ ATVS v4 ENDEKS ARAŞTIRMASI · {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · hedef düşüş {p_(a.hedef, 0)} ═══")
    log(f"Bitget maliyeti: taker {C.BITGET_TAKER_BPS} bps × 2 + spread · fonlama {C.BITGET_FUNDING_BPS_DAY} bps/gün")
    fin_meta = json.load(open(a.finalist, encoding="utf-8")) if os.path.exists(a.finalist) else {"finalistler": []}
    need = sorted({f["asset"] for f in fin_meta.get("finalistler", [])} | set(C.IDX_ASSETS))
    log("\n── Veri")
    H = {x: load_1h(x, a.sentetik, seed=i) for i, x in enumerate(need)}

    log("\n── 1) Mevcut finalistler — Bitget gerçek maliyetiyle")
    base = base_finalists(H, fin_meta)

    log("\n── 2) Endeks taraması")
    cand_all, ctxs = [], {}
    for asset in C.IDX_ASSETS:
        if H.get(asset) is None or H[asset].empty:
            log(f"  {asset}: veri yok")
            continue
        cx = IL.Ctx(asset, H[asset])
        ctxs[asset] = cx
        t1 = time.time()
        rows = scan(cx)
        pool = sorted([r for r in rows if r["ins"]["n"] >= C.MIN_TRADES_IS and np.isfinite(r["ins"]["t"]) and r["ins"]["t"] >= C.IDX_IS_T_MIN],
                      key=lambda r: -r["ins"]["t"])[: C.IDX_POOL_PER_ASSET]
        log(f"  {asset}: {len(cx.d)} seans günü ({cx.d.index[0]:%Y-%m} → {cx.d.index[-1]:%Y-%m}) · {len(rows)} ayar · "
            f"IS t≥{C.IDX_IS_T_MIN}: {len(pool)} · {time.time() - t1:.0f}s")
        for r in pool:
            cand_all.append(gates(cx, r))
        ctxs[asset + "_all"] = rows
    pv = [e["oos"]["p"] if e["k1_raw"] else 1.0 for e in cand_all]
    for e, ok in zip(cand_all, FN.bh_pass(pv, C.GATE_OOS_P)):
        e["gates"]["K1 OOS"] = bool(e["k1_raw"] and ok)
    for e in cand_all:
        g = e["gates"]
        if g["K1 OOS"] and g["K2 tüm dönem"] and g["K5 yıllar"] and g["K6 veri"]:
            robust(ctxs[e["spec"]["asset"]], e)
        else:
            e["passed"] = False
    passed = sorted([e for e in cand_all if e["passed"]], key=lambda e: -e["full"]["t"])
    log(f"  kapıların hepsini geçen: {len(passed)} / {len(cand_all)} aday")
    picks, per = [], {}
    for e in passed:
        k = (e["spec"]["asset"], e["spec"]["fam"])
        if per.get(e["spec"]["asset"], 0) >= C.IDX_PICK_PER_ASSET or any((p["spec"]["asset"], p["spec"]["fam"]) == k for p in picks):
            continue
        picks.append(e)
        per[e["spec"]["asset"]] = per.get(e["spec"]["asset"], 0) + 1
    for i, e in enumerate(picks, 1):
        e["id"] = f"X{i}_{e['spec']['asset']}_1d_{e['spec']['fam']}"

    log("\n── 3) Portföy katkısı (Monte Carlo, hedef düşüş içinde en yüksek CAGR)")
    frames = {b["id"]: strat_frame(b["id"], b["asset"], b["trades"]) for b in base if len(b["trades"])}
    base_fixed = {sid: 0.01 for sid in frames}           # botun bugünkü ayarı: işlem başına %1
    allt = pd.concat(list(frames.values())) if frames else pd.DataFrame()
    oos_start = allt.loc[allt["oos"], "entry_time"].min() if len(allt) and allt["oos"].any() else None
    scen = []
    if frames:
        b0 = optimise(frames, base_fixed, [], a.hedef, oos_start)
        if b0:
            scen.append({"ad": "Mevcut (XAU+ETH, %1)", "x": None, **b0[0]})
    for e in picks:
        fr = dict(frames)
        fr[e["id"]] = strat_frame(e["id"], e["spec"]["asset"], e["trades"])
        if oos_start is None:
            oos_start = fr[e["id"]].loc[fr[e["id"]]["oos"], "entry_time"].min()
        res = [r for r in optimise(fr, base_fixed, [e["id"]], a.hedef, oos_start) if r["risks"][e["id"]] > 0]
        okr = [r for r in res if r["ok"]]
        best = max(okr, key=lambda r: r["cagr"]) if okr else (min(res, key=lambda r: r["p95"]) if res else None)
        if best:
            scen.append({"ad": f"+ {e['id']}", "x": e, **best})
            log(f"  {e['id']}: risk {p_(best['risks'][e['id']], 2)} → CAGR {p_(best['cagr'])} · p95 düşüş {p_(best['p95'])} · "
                f"OOS CAGR {p_(best['oos_cagr'])} {'✓' if best['ok'] else '✗ hedef aşıldı'}")
    # tam optimizasyon (bilgi amaçlı): bütün strateji riskleri serbest, en iyi adayla
    full_opt = None
    base_row = scen[0] if scen and scen[0]["x"] is None else None
    good = [s for s in scen if s["x"] is not None and s["ok"] and base_row is not None
            and s["cagr"] > base_row["cagr"] and (not np.isfinite(base_row["oos_cagr"]) or s["oos_cagr"] >= base_row["oos_cagr"])]
    rec = max(good, key=lambda s: s["cagr"]) if good else None
    if rec is not None:
        fr = dict(frames)
        fr[rec["x"]["id"]] = strat_frame(rec["x"]["id"], rec["x"]["spec"]["asset"], rec["x"]["trades"])
        allr = [r for r in optimise(fr, {}, list(fr), a.hedef, oos_start) if r["ok"]]
        full_opt = max(allr, key=lambda r: r["cagr"]) if allr else None
    log(f"\nÖNERİ: {'3. varlık → ' + rec['x']['id'] if rec else '3. varlık eklenmesin (hiçbir aday portföyü hedef içinde iyileştirmedi)'}")

    # ── çıktılar
    os.makedirs(C.OUT_DIR, exist_ok=True)
    os.makedirs(C.LIVE_STATE_DIR, exist_ok=True)
    tab = pd.DataFrame([{"varlık": e["spec"]["asset"], "ayar": IL.spec_name(e["spec"]), "IS_t": e["ins"]["t"], "IS_exp": e["ins"]["exp"],
                         "OOS_exp": e["oos"]["exp"], "OOS_n": e["oos"]["n"], "OOS_p": e["oos"]["p"], "alfa": e["alpha"],
                         "tüm_exp": e["full"]["exp"], "tüm_n": e["full"]["n"], "isabet": e["full"]["wr"], "yıl_pozitif": e["years_pos"],
                         "maliyet2_exp": e.get("cost2", {}).get("exp", np.nan), "komşu_pozitif": e.get("neighbor_pos", np.nan),
                         **{k: v for k, v in e["gates"].items()}, "geçti": e["passed"]} for e in cand_all])
    tab.to_csv(os.path.join(C.OUT_DIR, "endeks_adaylar.csv"), index=False)
    if picks:
        pd.concat([e["trades"].assign(id=e["id"]) for e in picks]).to_csv(os.path.join(C.OUT_DIR, "endeks_islemler.csv.gz"), index=False)
    if scen:
        eqs = pd.DataFrame({s["ad"]: s["eq"] for s in scen})
        eqs.index = eqs.index.tz_localize(None) if eqs.index.tz is not None else eqs.index
        eqs.ffill().to_csv(os.path.join(C.OUT_DIR, "endeks_kasa.csv"))
    out = {"olusturma": datetime.now(timezone.utc).isoformat(timespec="minutes"), "sentetik": a.sentetik, "hedef_mdd": a.hedef,
           "maliyet": {"taker_bps": C.BITGET_TAKER_BPS, "funding_bps_gun": C.BITGET_FUNDING_BPS_DAY},
           "temel": [{"id": b["id"], "eski_exp": b["old"]["exp"], "bitget_exp": b["new"]["exp"], "bitget_oos_exp": b["oos"]["exp"],
                      "n": b["new"]["n"]} for b in base],
           "finalistler": []}
    if rec is not None:
        e = rec["x"]
        out["finalistler"].append({
            "id": e["id"], "engine": "idx", "asset": e["spec"]["asset"], "tf": "1d", "family": e["spec"]["fam"],
            "spec": e["spec"], "risk": rec["risks"][e["id"]], "rules": rules_text(e["spec"]),
            "backtest": {"exp": e["full"]["exp"], "wr": e["full"]["wr"], "n": e["full"]["n"], "oos_exp": e["oos"]["exp"],
                         "oos_n": e["oos"]["n"], "alpha": e["alpha"]},
            "portfoy": {"cagr": rec["cagr"], "p95_mdd": rec["p95"], "mdd": rec["mdd"], "oos_cagr": rec["oos_cagr"]}})
    if full_opt:
        out["tam_optimizasyon_bilgi"] = {"riskler": full_opt["risks"], "cagr": full_opt["cagr"], "p95_mdd": full_opt["p95"]}
    if not a.sentetik:
        json.dump(out, open(os.path.join(C.LIVE_STATE_DIR, "endeks_finalist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    json.dump(out, open(os.path.join(C.OUT_DIR, "endeks_finalist.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    render(a, base, cand_all, picks, scen, rec, full_opt, ctxs, time.time() - t0)
    log(f"\nsüre {time.time() - t0:.0f}s")
    return out


def render(a, base, cand_all, picks, scen, rec, full_opt, ctxs, dur):
    L = [f"# ATVS v4 — Endeks araştırması ve 3. varlık", "",
         f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · {'**SENTETİK VERİ (test)**' if a.sentetik else 'gerçek veri'} · "
         f"hedef: %95 olasılıkla maks. düşüş ≤ {p_(a.hedef, 0)} · süre {dur / 60:.0f} dk", ""]
    L += ["## Sonuç", ""]
    if rec:
        x = rec["x"]
        b = scen[0]
        L += [f"**3. varlık önerisi: {x['id']}** — işlem başına risk {p_(rec['risks'][x['id']], 2)}", "",
              f"- Portföy yıllık getiri (CAGR): {p_(b['cagr'])} → **{p_(rec['cagr'])}**",
              f"- Maks. düşüş (geçmiş): {p_(b['mdd'])} → {p_(rec['mdd'])} · Monte Carlo %95: {p_(b['p95'])} → {p_(rec['p95'])}",
              f"- OOS dönem CAGR: {p_(b['oos_cagr'])} → {p_(rec['oos_cagr'])}", "",
              "Kurallar: " + rules_text(x["spec"]), "",
              "Bot bu stratejiyi ancak `aktif_botlar.txt` dosyasına "
              f"`{x['spec']['asset']}` (ya da `{x['spec']['asset']} OTO`) satırı eklenince işler.", ""]
    else:
        L += ["**3. varlık eklenmesi önerilmiyor.** Hiçbir endeks adayı, mevcut portföyü hedef düşüş içinde kalarak hem tüm "
              "dönemde hem OOS dönemde iyileştiremedi. (Ayrıntılar aşağıda.)", ""]
    L += ["## 1) Mevcut finalistler — Bitget gerçek maliyetiyle", "",
          f"Eski laboratuvar maliyeti CFD spread'iydi. Bitget: taker {C.BITGET_TAKER_BPS:g} bps × 2 + spread, fonlama {C.BITGET_FUNDING_BPS_DAY:g} bps/gün.", "",
          "| Finalist | eski maliyetle | Bitget maliyetiyle | Bitget OOS | işlem |", "|---|---|---|---|---|"]
    for b in base:
        L.append(f"| {b['id']} | {r_(b['old']['exp'])} | **{r_(b['new']['exp'])}** | {r_(b['oos']['exp'])} | {b['new']['n']} |")
    L += ["", "## 2) Endeks taraması", ""]
    for asset in C.IDX_ASSETS:
        rows = ctxs.get(asset + "_all")
        if rows:
            L.append(f"- {asset}: {len(rows)} ayar test edildi · IS t ≥ {C.IDX_IS_T_MIN}: {sum(1 for e in cand_all if e['spec']['asset'] == asset)}")
    L += ["", "Kapılar: K1 OOS (BH q=0.10) · K2 tüm dönem ≥80 işlem · K3 maliyet×2 · K4 komşular ≥%70 pozitif · K5 yılların ≥%60'ı pozitif · K6 veri şüphesi", "",
          "| Aday | IS t | OOS beklenti (n) | alfa | tüm dönem (n) | isabet | K1 K2 K3 K4 K5 K6 |", "|---|---|---|---|---|---|---|"]
    for e in sorted(cand_all, key=lambda e: (not e["passed"], -e["ins"]["t"]))[:40]:
        gs = " ".join("✓" if v else ("·" if v is None else "✗") for v in e["gates"].values())
        L.append(f"| {'**' if e['passed'] else ''}{IL.spec_name(e['spec'])}{'**' if e['passed'] else ''} | {e['ins']['t']:.1f} | "
                 f"{r_(e['oos']['exp'])} ({e['oos']['n']}) | {r_(e['alpha'])} | {r_(e['full']['exp'])} ({e['full']['n']}) | {p_(e['full']['wr'], 0)} | {gs} |")
    L += ["", "## 3) Portföy senaryoları", "",
          "| Senaryo | riskler | CAGR | maks. düşüş | MC %95 düşüş | Sharpe | işlem/ay | OOS CAGR | hedef |", "|---|---|---|---|---|---|---|---|---|"]
    for s in scen:
        rk = ", ".join(f"{k.split('_')[0]} {p_(v, 2)}" for k, v in s["risks"].items() if v > 0)
        L.append(f"| {s['ad']} | {rk} | {p_(s['cagr'])} | {p_(s['mdd'])} | {p_(s['p95'])} | {s['sharpe']:.2f} | {s['n_month']:.1f} | "
                 f"{p_(s['oos_cagr'])} | {'✓' if s['ok'] else '✗'} |")
    if full_opt:
        rk = ", ".join(f"{k} {p_(v, 2)}" for k, v in full_opt["risks"].items() if v > 0)
        L += ["", f"Bilgi — bütün riskler serbest bırakılırsa (aynı düşüş hedefi): {rk} → CAGR {p_(full_opt['cagr'])}, MC %95 düşüş {p_(full_opt['p95'])}. "
              "Bot bunu otomatik uygulamaz; XAU/ETH riski `ATVS_RISK` ile kalır."]
    for e in picks:
        L += ["", f"### {e['id']}", "", rules_text(e["spec"]), "",
              f"Tüm dönem {r_(e['full']['exp'])} ({e['full']['n']} işlem, isabet {p_(e['full']['wr'], 0)}) · OOS {r_(e['oos']['exp'])} ({e['oos']['n']}) · "
              f"alfa {r_(e['alpha'])} · maliyet×2 {r_(e['cost2']['exp'])} · komşular {p_(e['neighbor_pos'], 0)} pozitif"]
        yt = e["trades"].groupby(e["trades"]["entry_time"].dt.year)["R"].agg(["size", "mean", "sum"])
        L += ["", "| Yıl | işlem | ort. R | toplam R |", "|---|---|---|---|"] + [f"| {y} | {int(r['size'])} | {r['mean']:+.3f} | {r['sum']:+.2f} |" for y, r in yt.iterrows()]
    L += ["", "## Uygulama notları (Bitget hisse/endeks vadelileri)", "",
          "- Kontratlar 7/24 fiyatlanır ama ABD piyasası kapalıyken **yeni pozisyon açılamaz**; bu yüzden giriş/çıkış 15:00 ET'de (seans içi).",
          "- Gece ve hafta sonu açık pozisyonun stopu boşlukla (gap) geçilebilir; backtest bunu açılış fiyatıyla doldurarak hesaplar (R < −1 olabilir).",
          "- ABD tatil günlerinde veri olsa bile borsa emri reddedebilir; bot hatayı yazar ve o günü atlar.",
          "- Geçmiş sonuçtur; seçim yanlılığı tamamen yok edilemez. Önce demo."]
    open(os.path.join(C.OUT_DIR, "ENDEKS_RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    open(os.path.join(C.OUT_DIR, "endeks_logu.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
