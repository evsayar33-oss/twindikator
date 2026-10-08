"""ATVS v5.2 — 4 SAATLİK KRİPTO DOĞRULAMASI + DÜŞÜŞ TOLERANSI / GETİRİ TABLOSU (limitli emir maliyetiyle)

Aynı iki MACD kuralı (hiç değiştirilmeden; MACD 675/875/475'in "1s eşdeğeri" 4 saatlikte ≈ 169/219/119 mum):
  EMA_4h : yön + EMA20'ye geri çekilme · iz süren stop · iki yön
  X_4h   : yön + hızlı MACD(12,26,9) kesişimi · iz süren stop · yalnız LONG
15 coin birlikte + batan coinler, v4.3'teki doğrulama testleri (D1 kümelenmiş t, D2 batan coinler, D3 placebo,
D4 ayar hassasiyeti, maliyet ×2). Günlük kurallar (EMA_1d, X_1d) karşılaştırma ve portföy için yeniden ölçülür.

Portföy: ETH 4h Donchian + XAU 4h + günlük kurallar + (geçerse) 4h kurallar; canlı botun RİSK YÖNETİCİSİ dahil
(zirveden %10 → risk ×0.5, %20 → ×0.25, %30 → yeni işlem yok). Her düşüş hedefi (%15/%20/%25/%30) için en yüksek CAGR.
Maliyet: config.ORDER_MODE (varsayılan "limit": giriş %80 maker, çıkış taker).

Kullanım: python run_dogrulama_4h.py [--sentetik]
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import run_dogrulama as RD
import run_kripto_gunluk as KG
from lab import config as C
from lab import data as D
from lab import exits as X
from lab import features as FT
from lab import portfolio as PF
from lab.kripto import direction, entries, EXIT, RULES as BASE_RULES

TFS = {"1d": 1440, "4h": 240}
OUT = os.path.join(C.OUT_DIR, "dogrulama_4h")
N_PLACEBO = int(os.getenv("ATVS_PLACEBO", "200"))
TARGETS = (0.15, 0.20, 0.25, 0.30)
DD_STEPS = [(0.10, 0.5), (0.20, 0.25), (0.30, 0.0)]
OOS_START = KG.OOS_START
LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


class Coin(RD.Coin):
    def rule(self, key, d=None, ema_len=20, cost_mult=1.0):
        r = key.split("_")[0]
        en = entries(self.df, self.dir if d is None else d, ema_len, self.tf_min)
        sm = self.sm
        if cost_mult != 1.0:
            if self.sm2 is None:
                f = FT.compute(self.df)
                self.sm2 = X.simulate(self.df, f["atr"], self.cost * cost_mult, C.EXITS[EXIT], fund_bps_bar=C.fund_bps_bar(self.tf_min))
            sm = self.sm2
        L, S = en[r]
        return self.trades(L, S, BASE_RULES[r], sm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentetik", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    log(f"═══ ATVS v5.2 4h DOĞRULAMA · {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · emir modu {C.ORDER_MODE} · "
        f"örnek maliyet BTC {KG.cost_of('BTCUSDT'):.1f} bps ═══")
    coins = {tf: {} for tf in TFS}
    dead = {tf: {} for tf in TFS}
    for tf, tm in TFS.items():
        for i, s in enumerate(KG.UNIVERSE + RD.DELISTED):
            df = KG.load_daily(s, a.sentetik, i + (0 if tf == "1d" else 1000), interval=tf)
            if len(df) < (300 if tf == "1d" else 1500):
                log(f"  {s} {tf}: veri yok/yetersiz ({len(df)})")
                continue
            (dead if s in RD.DELISTED else coins)[tf][s] = Coin(s, df, KG.cost_of(s), tm)
        log(f"  {tf}: {len(coins[tf])} coin + {len(dead[tf])} batan coin")
    keys = [f"{r}_{tf}" for tf in TFS for r in BASE_RULES]
    scope = {k: BASE_RULES[k.split("_")[0]] for k in keys}
    T, Td = {}, {}
    for k in keys:
        tf = k.split("_")[1]
        T[k] = pd.concat([c.rule(k) for c in coins[tf].values()], ignore_index=True)
        Td[k] = pd.concat([c.rule(k) for c in dead[tf].values()], ignore_index=True) if dead[tf] else T[k].iloc[:0]
    d1, d2, d3, d4, c2, verdict = {}, {}, {}, {}, {}, {}
    rng = np.random.default_rng(7)
    for k in keys:
        tf = k.split("_")[1]
        t = T[k]
        d1[k] = {"tum": RD.cstats(t), "is": RD.cstats(t[t["entry_time"] < OOS_START]), "oos": RD.cstats(t[t["entry_time"] >= OOS_START])}
        allt = pd.concat([t, Td[k]], ignore_index=True)
        d2[k] = {"dead": RD.cstats(Td[k]), "hepsi": RD.cstats(allt)}
        real = t["R"].mean()
        sims = []
        cl = list(coins[tf].values())
        for _ in range(N_PLACEBO):
            tt = pd.concat([c.rule(k, d=RD.placebo_dir(c.dir, rng)) for c in cl], ignore_index=True)
            sims.append(tt["R"].mean() if len(tt) else np.nan)
        arr = np.array(sims, float)
        arr = arr[np.isfinite(arr)]
        d3[k] = {"gercek": real, "ort": float(arr.mean()), "p95": float(np.percentile(arr, 95)), "p": float((arr >= real).mean())}
        rows = []
        for sc in (0.7, 0.85, 1.0, 1.15, 1.3):
            for el in ((15, 20, 25) if k.startswith("EMA") else (20,)):
                tt = pd.concat([c.rule(k, d=direction(c.c, sc, c.tf_min), ema_len=el) for c in cl], ignore_index=True)
                rows.append({"macd_olcek": sc, "ema": el, "n": len(tt), "exp": tt["R"].mean() if len(tt) else np.nan,
                             "oos_exp": tt.loc[tt["entry_time"] >= OOS_START, "R"].mean() if len(tt) else np.nan})
        tab = pd.DataFrame(rows)
        nb = tab[~((tab["macd_olcek"] == 1.0) & (tab["ema"] == 20))]
        d4[k] = {"tablo": tab, "pozitif": float((nb["exp"] > 0).mean()), "oos_pozitif": float((nb["oos_exp"] > 0).mean())}
        c2[k] = pd.concat([c.rule(k, cost_mult=C.GATE_COST_MULT) for c in cl], ignore_index=True)["R"].mean()
        g = {"D1 haftalık t ≥ 2 ve OOS > 0": bool(d1[k]["tum"]["t_hafta"] >= 2.0 and d1[k]["oos"]["exp"] > 0),
             "D2 batan coinler dahil > 0": bool(d2[k]["hepsi"]["exp"] > 0),
             "D3 placebo p ≤ 0.05": bool(d3[k]["p"] <= 0.05),
             "D4 komşuların ≥ %70'i pozitif": bool(d4[k]["pozitif"] >= 0.70),
             "maliyet ×2 > 0": bool(c2[k] > 0)}
        verdict[k] = {"kapilar": g, "gecti": all(g.values())}
        log(f"  {k}: {r_(d1[k]['tum']['exp'])} n={d1[k]['tum']['n']} haftalık t={RD.t_(d1[k]['tum']['t_hafta'])} · OOS {r_(d1[k]['oos']['exp'])} · "
            f"placebo p={d3[k]['p']:.3f} · komşular {RD.p_(d4[k]['pozitif'])} → {'GEÇTİ' if verdict[k]['gecti'] else 'GEÇEMEDİ'}")

    # ── portföy
    fr = {}
    for k in keys:
        if not (verdict[k]["gecti"] or k.endswith("_1d") or os.getenv("ATVS_HEPSI") == "1"):   # günlük kurallar v4.3'te zaten doğrulandı
            continue
        t = T[k]
        base = t["coin"].str.replace("USDT", "")
        fr[k] = pd.DataFrame({"entry_time": t["entry_time"], "exit_time": t["exit_time"], "R": t["R"], "sid": k, "asset": base, "cluster": base})
    if not a.sentetik:
        try:
            import run_endeks as RE
            meta = json.load(open(os.path.join(C.LIVE_STATE_DIR, "finalists.json"), encoding="utf-8"))
            H = {}
            for asset in {f["asset"] for f in meta.get("finalistler", [])}:
                raw, _ = D.load(asset, "1h", refresh=True)
                H[asset], _ = D.validate(asset, "1h", raw)
            for b in RE.base_finalists(H, meta):
                t = b["trades"]
                if len(t):
                    fr[b["id"]] = pd.DataFrame({"entry_time": pd.to_datetime(t["entry_time"], utc=True), "exit_time": pd.to_datetime(t["exit_time"], utc=True),
                                                "R": t["R"], "sid": b["id"], "asset": b["asset"], "cluster": b["asset"]})
        except Exception as ex:
            log(f"  mevcut finalistler eklenemedi: {type(ex).__name__}: {ex}")
    sids = list(fr)
    log(f"  portföy stratejileri: {', '.join(sids)}")
    grid_free = [s for s in sids if s.endswith("_4h") or s.startswith("F1")]
    fixed = {s: (0.0025 if s == "EMA_1d" else 0.01) for s in sids if s not in grid_free}
    rows = []
    for combo in itertools.product((0.0, 0.0025, 0.005, 0.0075, 0.01), repeat=len(grid_free)):
        for scale in (0.5, 0.75, 1.0, 1.25, 1.5, 2.0):
            for mo in (6, 8):
                risks = {s: v * scale for s, v in {**fixed, **dict(zip(grid_free, combo))}.items()}
                ev = _eval(fr, risks, mo)
                if not ev:
                    continue
                rows.append({"olcek": scale, "max_acik": mo, **{f"risk_{s}": risks[s] for s in sids}, "cagr": ev["m"]["cagr"], "mdd": ev["m"]["mdd"],
                             "p95": ev["mc"].get("p95_mdd", np.nan), "p_dd30": ev["mc"].get("p_dd30", np.nan), "sharpe": ev["m"]["sharpe"],
                             "islem_ay": ev["m"]["per_month"], "oos_cagr": np.nan, "kotu_yil": ev["m"]["yearly"].min()})
    tab = pd.DataFrame(rows, columns=["olcek", "max_acik", "cagr", "mdd", "p95", "p_dd30", "sharpe", "islem_ay", "oos_cagr", "kotu_yil"]
                       + [f"risk_{s}" for s in sids]) if not rows else pd.DataFrame(rows)
    best = {}
    for tg in TARGETS:
        ok = tab[tab["p95"] <= tg]
        if len(ok):
            r = ok.sort_values("cagr", ascending=False).iloc[0].copy()
            evo = _eval(fr, {s_: r[f"risk_{s_}"] for s_ in sids}, int(r["max_acik"]), start=OOS_START)
            r["oos_cagr"] = evo["m"]["cagr"] if evo else np.nan
            best[tg] = r
    tab.to_csv(os.path.join(OUT, "portfoy_izgara.csv.gz"), index=False)
    for tg, r in best.items():
        prop = {"aciklama": f"v5.2 önerisi — %95 olasılıkla düşüş ≤ %{100 * tg:.0f} hedefi (risk yöneticisi dahil). Emir modu: {C.ORDER_MODE}.",
                "max_acik": int(r["max_acik"]), "riskler": {s: float(r[f"risk_{s}"]) for s in sids},
                "cagr": float(r["cagr"]), "p95_mdd": float(r["p95"]), "oos_cagr": float(r["oos_cagr"])}
        json.dump(prop, open(os.path.join(OUT, f"oneri_dusus_{int(100 * tg)}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    render(a, coins, dead, keys, d1, d2, d3, d4, c2, verdict, sids, best, time.time() - t0)
    for k in keys:
        T[k].to_csv(os.path.join(OUT, f"islemler_{k}.csv.gz"), index=False)
    log(f"süre {time.time() - t0:.0f}s")


def _eval(fr, risks, mo, start=None):
    parts = []
    for s, f in fr.items():
        r = risks.get(s, 0.0)
        if r <= 0:
            continue
        x = f if start is None else f[f["entry_time"] >= start]
        if len(x):
            parts.append(x.assign(R=x["R"] * r))
    if not parts:
        return {}
    tr = pd.concat(parts).sort_values(["entry_time", "sid"]).reset_index(drop=True)
    sim = PF.simulate(tr, 1.0, max_open=mo, cluster_max=1, dd_steps=DD_STEPS)
    if sim["equity"].empty:
        return {}
    return {"m": PF.metrics(sim["equity"], sim["taken"]), "mc": PF.monte_carlo(sim["equity"]) or {}}


def r_(x):
    return RD.r_(x)


def render(a, coins, dead, keys, d1, d2, d3, d4, c2, verdict, sids, best, dur):
    p_, t_ = RD.p_, RD.t_
    L = ["# ATVS v5.2 — 4 saatlik kripto doğrulaması ve düşüş toleransı / getiri", "",
         f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · {'**SENTETİK (test)**' if a.sentetik else 'gerçek veri'} · emir modu **{C.ORDER_MODE}** "
         f"(giriş %{100 * C.LIMIT_FILL:.0f} maker, çıkış taker) · süre {dur / 60:.0f} dk", ""]
    gk = list(next(iter(verdict.values()))["kapilar"])
    L += ["## Hüküm", "", "| Kural | " + " | ".join(gk) + " | SONUÇ |", "|---|" + "---|" * (len(gk) + 1)]
    for k in keys:
        L.append(f"| {k} | " + " | ".join("✓" if verdict[k]["kapilar"][g] else "✗" for g in gk) + f" | {'✅' if verdict[k]['gecti'] else '❌'} |")
    L += ["", "## Ayrıntı", "", "| Kural | işlem | beklenti | haftalık t | OOS (n) | OOS haftalık t | batan coinler dahil | placebo (gerçek / rastgele %95) | komşular | maliyet×2 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in keys:
        L.append(f"| {k} | {d1[k]['tum']['n']} | {r_(d1[k]['tum']['exp'])} | {t_(d1[k]['tum']['t_hafta'])} | {r_(d1[k]['oos']['exp'])} ({d1[k]['oos']['n']}) | "
                 f"{t_(d1[k]['oos']['t_hafta'])} | {r_(d2[k]['hepsi']['exp'])} | {r_(d3[k]['gercek'])} / {r_(d3[k]['p95'])} (p={d3[k]['p']:.3f}) | "
                 f"{p_(d4[k]['pozitif'])} | {r_(c2[k])} |")
    L += ["", "## Düşüş toleransı → getiri (risk yöneticisi dahil, coin başına tek pozisyon)", "",
          "| %95 olasılıkla düşüş ≤ | " + " | ".join(f"risk {s}" for s in sids) + " | en fazla açık | CAGR | geçmiş maks. düşüş | %30+ düşüş olasılığı (1 yıl) | en kötü yıl | Sharpe | işlem/ay | OOS CAGR |",
          "|---|" + "---|" * (len(sids) + 9)]
    for tg, r in best.items():
        L.append(f"| **{p_(tg)}** | " + " | ".join(p_(r[f'risk_{s}'], 2) for s in sids) + f" | {int(r['max_acik'])} | **{p_(r['cagr'], 1)}** | {p_(r['mdd'], 1)} | "
                 f"{p_(r['p_dd30'], 1)} | {p_(r['kotu_yil'], 1)} | {r['sharpe']:.2f} | {r['islem_ay']:.1f} | {p_(r['oos_cagr'], 1)} |")
    L += ["", "Kasa koruması (tüm satırlarda): zirveden %10 düşüşte risk ×0.5, %20'de ×0.25, %30'da yeni işlem yok · günlük zarar limiti canlı botta ayrıca %3.",
          "Her satırın ayarı `oneri_dusus_XX.json` dosyasındadır; seçilen satır bota `state/kripto_finalist.json` ile uygulanır.", "",
          "## Ayar hassasiyeti (D4)", ""]
    for k in keys:
        tb = d4[k]["tablo"]
        L += [f"**{k}** — komşuların {p_(d4[k]['pozitif'])}'ı pozitif (OOS {p_(d4[k]['oos_pozitif'])})", "", "| MACD ölçeği | EMA | işlem | beklenti | OOS |", "|---|---|---|---|---|"]
        L += [f"| ×{r['macd_olcek']} | {int(r['ema'])} | {int(r['n'])} | {r_(r['exp'])} | {r_(r['oos_exp'])} |" for _, r in tb.iterrows()] + [""]
    open(os.path.join(OUT, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    open(os.path.join(OUT, "logu.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
