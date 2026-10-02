"""ATVS Lab v2 — tüm strateji aileleri × tüm çıkış yöntemleri × 5 zaman dilimi × 6 varlık.

Kullanım:
    python run_lab.py                     # tüm varlıklar, veriyi güncelle
    python run_lab.py --assets XAU,BTC    # seçili varlıklar
    python run_lab.py --no-refresh        # yalnızca önbellek
    python run_lab.py --synthetic         # internetsiz duman testi (sahte veri)
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
from lab import evaluate as EV
from lab import portfolio as PF

SC_TR = {"both": "iki yön", "long": "LONG", "short": "SHORT"}
TF_MIN = {"5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240}


def pct(x):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.1f}"


def rr(x):
    return "—" if x is None or not np.isfinite(x) else f"{x:+.3f}R"


def pv(x):
    return "—" if x is None or not np.isfinite(x) else ("<0.001" if x < 0.001 else f"{x:.3f}")


def f2(x):
    return "—" if x is None or not np.isfinite(x) else ("∞" if np.isinf(x) else f"{x:.2f}")


# ───────────────────────── SENTETİK ─────────────────────────
def synthetic(base: str, years: float, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    step = pd.Timedelta("5min") if base == "5m" else pd.Timedelta("1h")
    n = int(years * 365 * 24 * (12 if base == "5m" else 1))
    vol = np.exp(np.cumsum(rng.normal(0, 0.02, n)) * 0.05) * (0.0015 if base == "5m" else 0.005)
    ret = rng.standard_t(4, n) * vol * 0.6
    c = 100 * np.exp(np.cumsum(ret))
    o = np.r_[c[0], c[:-1]]
    sp = np.abs(rng.normal(0, vol, n)) * c
    idx = pd.date_range(end=pd.Timestamp("2026-10-02 16:00", tz="UTC"), periods=n, freq=step)
    v = np.exp(rng.normal(10, 0.6, n) + 3 * np.abs(ret) / vol.mean())
    return pd.DataFrame({"open": o, "high": np.maximum(o, c) + sp, "low": np.minimum(o, c) - sp, "close": c, "volume": v}, index=idx)


# ───────────────────────── ANA AKIŞ ─────────────────────────
def run(assets: list[str], refresh: bool, synth: bool):
    os.makedirs(C.OUT_DIR, exist_ok=True)
    need = list(dict.fromkeys(assets + [C.PARTNER[a] for a in assets if a in C.PARTNER]))
    tfs_run = [tf for tf in C.TIMEFRAMES if not C.FOCUS_TFS or tf in C.FOCUS_TFS]
    need_bases = sorted({C.TIMEFRAMES[tf]["base"] for tf in tfs_run})
    bases, srcs, funding, vreps = {}, {}, {}, []
    for ai, a in enumerate(need):
        for b in need_bases:
            if synth:
                bases[(a, b)], srcs[(a, b)] = synthetic(b, 0.5 if b == "5m" else 3, 100 * ai + (b == "1h")), "SENTETİK"
            else:
                raw, srcs[(a, b)] = D.load(a, b, refresh=refresh)
                bases[(a, b)], rep = D.validate(a, b, raw)
                vreps.append(rep)
                print(f"  doğrulama {a} {b}: {rep['status']} · düzeltilen ay {rep['fixed_months']} · atılan ay {rep['dropped_months']} · sıçrama {rep['spikes']}")
            df = bases[(a, b)]
            print(f"{a} {b}: {len(df):,} bar {df.index[0] if len(df) else '-'} → {df.index[-1] if len(df) else '-'} [{srcs[(a, b)]}]")
        funding[a] = None if synth else D.load_funding(a, refresh=refresh)
        if funding[a] is not None:
            print(f"{a} fonlama: {len(funding[a]):,} kayıt")

    summary, keep_rows, cands = {}, [], []
    for a in assets:
        t0 = time.time()
        print(f"\n═══ {a} ═══")
        pa = C.PARTNER.get(a)
        tf_res, tf_aux = {}, {}
        for tf in tfs_run:
            spec = C.TIMEFRAMES[tf]
            base = bases[(a, spec["base"])]
            if base.empty:
                continue
            native = {"5m": "5min", "1h": "1h"}[spec["base"]]
            df = base if spec["rule"] == native else D.resample(base, spec["rule"])
            if len(df) < C.DYN_LEN * 3:
                print(f"  {tf}: yetersiz bar ({len(df)})")
                continue
            partner = None
            if pa and (pa, spec["base"]) in bases and not bases[(pa, spec["base"])].empty:
                pb = bases[(pa, spec["base"])]
                partner = (pb if spec["rule"] == native else D.resample(pb, spec["rule"]))["close"]
            t1 = time.time()
            res, aux = EV.evaluate(df, C.ASSETS[a]["cost_bps"], TF_MIN[tf], partner, pa or "", funding.get(a))
            res.insert(0, "tf", tf)
            res.insert(0, "asset", a)
            aux["bars"] = len(df)
            cands += PF.collect(res, aux, a, tf)
            tf_res[tf], tf_aux[tf] = res, aux
            b = EV.pick(res, "both")
            print(f"  {tf}: {len(df):,} bar · {aux['n_entries']} giriş × {len(C.EXITS)} çıkış · "
                  f"meta: {aux['meta'] or 'tamam'} · IS {rr(b['both_is_exp']) if b is not None else '—'} → OOS {rr(b['both_oos_exp']) if b is not None else '—'} · {time.time() - t1:.0f}s")
            top = res[res["both_is_n"] >= C.MIN_TRADES_IS].nlargest(150, "both_is_lb")
            fam_best = res.loc[res.groupby("family")["both_is_lb"].idxmax().dropna().astype(int)]
            keep_rows += [top, fam_best]
        summary[a] = analyse(a, tf_res, tf_aux, {b: srcs.get((a, b)) for b in ("5m", "1h")})
        print(f"  süre {time.time() - t0:.0f}s")

    if keep_rows:
        pd.concat(keep_rows).drop_duplicates(["asset", "tf", "entry", "exit"]).to_csv(
            os.path.join(C.OUT_DIR, "secili_sonuclar.csv.gz"), index=False, compression="gzip")
    with open(os.path.join(C.OUT_DIR, "en_iyi.json"), "w", encoding="utf-8") as fh:
        json.dump({a: s.get("json", {}) for a, s in summary.items()}, fh, ensure_ascii=False, indent=2, default=str)
    port = PF.run(cands)
    if port.get("selected"):
        pd.concat([c["trades"].assign(strateji=f"{c['asset']} {c['tf']} {c['entry']} | {c['exit']} | {c['scope']}") for c in port["selected"]]
                  ).sort_values("time").to_csv(os.path.join(C.OUT_DIR, "portfoy_islemler.csv.gz"), index=False, compression="gzip")
        pd.DataFrame({f"risk_%{100 * lv['risk']:.2g}": lv["equity"] for lv in port["levels"]}).to_csv(os.path.join(C.OUT_DIR, "portfoy_kasa_oos.csv"))
        print(f"Portföy: {len(port['selected'])} strateji")
    md = render(summary, synth, port, vreps, tfs_run)
    with open(os.path.join(C.OUT_DIR, "RAPOR.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(md)
    print(f"\nRapor: {os.path.join(C.OUT_DIR, 'RAPOR.md')}")


def _best_any_scope(res: pd.DataFrame, mask=None):
    cands = [(sc, EV.pick(res, sc, mask)) for sc in EV.SCOPES]
    cands = [(sc, r) for sc, r in cands if r is not None]
    if not cands:
        return None, None
    return max(cands, key=lambda x: x[1][f"{x[0]}_is_lb"])


def analyse(a, tf_res, tf_aux, srcs) -> dict:
    out = {"srcs": srcs, "tf": {}}
    for tf, res in tf_res.items():
        sc, r = _best_any_scope(res)
        out["tf"][tf] = {"sc": sc, "row": r, "bars": tf_aux[tf]["bars"], "span": tf_aux[tf]["span"], "meta": tf_aux[tf]["meta"],
                         "cost_R": tf_aux[tf]["cost_R"]}
    cands = [(tf, d["sc"], d["row"]) for tf, d in out["tf"].items() if d["row"] is not None]
    if not cands:
        return out
    tf, sc, row = max(cands, key=lambda x: x[2][f"{x[1]}_is_lb"])
    res, aux = tf_res[tf], tf_aux[tf]
    out.update({"tf_sel": tf, "sc": sc, "row": row, "verdict": EV.verdict(row, sc)})

    # aileler: her aile için tüm ZD ve yönler içinde IS'te seçilen en iyi
    fams = []
    for fam in sorted(set().union(*[set(r["family"]) for r in tf_res.values()])):
        best = None
        for t, r in tf_res.items():
            s, rw = _best_any_scope(r, r["family"] == fam)
            if rw is not None and (best is None or rw[f"{s}_is_lb"] > best[2][f"{best[1]}_is_lb"]):
                best = (t, s, rw)
        if best:
            fams.append(best)
    out["fams"] = sorted(fams, key=lambda x: -(x[2][f"{x[1]}_oos_exp"] if np.isfinite(x[2][f"{x[1]}_oos_exp"]) else -9))

    # çıkış yöntemi karşılaştırması (seçilen ZD): her çıkış için IS'te en iyi 20 giriş → OOS ortalaması
    ex_rows = []
    for ex in C.EXITS:
        r = res[(res["exit"] == ex) & (res["both_is_n"] >= C.MIN_TRADES_IS)]
        t20 = r.nlargest(20, "both_is_lb")
        t20 = t20[t20["both_oos_n"] >= C.MIN_TRADES_OOS]
        allr = r[r["both_oos_n"] >= C.MIN_TRADES_OOS]
        ex_rows.append((ex, t20["both_oos_exp"].mean(), (t20["both_oos_exp"] > 0).mean() if len(t20) else np.nan,
                        t20["both_oos_wr"].mean(), allr["both_oos_exp"].mean(), allr["both_oos_wr"].mean(), len(allr)))
    out["exits"] = ex_rows

    # sağlamlık: seçilen ZD'de IS'te ilk 20 ayarın OOS'ta pozitif kalma oranı
    t20 = res[res["both_is_n"] >= C.MIN_TRADES_IS].nlargest(20, "both_is_lb")
    t20 = t20[t20["both_oos_n"] >= C.MIN_TRADES_OOS]
    out["robust"] = ((t20["both_oos_exp"] > 0).mean() if len(t20) else np.nan, t20["both_oos_exp"].mean() if len(t20) else np.nan, len(t20))
    out["top"] = res[res["both_is_n"] >= C.MIN_TRADES_IS].nlargest(15, "both_is_lb")

    tp = EV.trade_path(aux, row, sc)
    edges = np.linspace(0, len(tp), C.N_BLOCKS + 1).astype(int)
    blocks = []
    for i in range(C.N_BLOCKS):
        b = tp.iloc[edges[i]:edges[i + 1]]
        if len(b):
            blocks.append((b["time"].iloc[0], b["time"].iloc[-1], len(b), (b["R"] > 0).mean(), b["R"].mean()))
    out["blocks"] = blocks
    out["dd"] = (EV.max_dd(tp.loc[~tp["oos"], "R"].to_numpy()), EV.max_dd(tp.loc[tp["oos"], "R"].to_numpy()))
    out["json"] = {
        "zaman_dilimi": tf, "yon": sc, "aile": row["family"], "giris": row["entry"], "cikis": row["exit"],
        "cikis_parametreleri": C.EXITS[row["exit"]],
        "is": {k: row[f"{sc}_is_{k}"] for k in ("n", "wr", "exp", "pf", "pm")},
        "oos": {k: row[f"{sc}_oos_{k}"] for k in ("n", "wr", "exp", "pf", "pm", "p")},
        "karar": out["verdict"],
    }
    return out


# ───────────────────────── RAPOR ─────────────────────────
def render(summary: dict, synth: bool, port: dict | None = None, vreps: list | None = None, tfs_run: list | None = None) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = [f"# ATVS Lab v2 Raporu — {now}", ""]
    if synth:
        L += ["> ⚠️ **SENTETİK VERİ** — yalnızca boru hattı testi; sonuçlar anlamsızdır.", ""]
    L += [
        "**Ölçü birimi R:** 1R = ilk stop mesafesi. +0.20R = işlem başına riskin %20'si kadar ortalama net kazanç (maliyet dahil).",
        f"**Seçim** ilk %{int(C.IS_FRACTION * 100)} veride (IS) beklentinin %95 alt sınırına göre yapılır; **karar son %{100 - int(C.IS_FRACTION * 100)} (OOS) verisine göre** verilir. "
        "✅ = OOS'ta pozitif ve p < 0.05/k (k = o tablodaki test sayısı, Bonferroni: çok sayıda test şans eseri 'kazanan' üretir) · "
        "⚠️ = pozitif ama düzeltme sonrası anlamsız · ❌ = OOS'ta negatif.",
        f"Giriş: sinyalden sonraki bar açılışı · zaman bariyeri {C.HORIZON} bar · aynı barda hedef+stop = stop. "
        "TP1>BE = 1R'de stop girişe · %50@1R>BE = 1R'de yarısı kapanır, stop girişe · IZ = iz süren stop.",
        "",
        f"**Odak:** zaman dilimleri {', '.join(tfs_run or [])} · aileler {', '.join(C.FOCUS_FAMILIES) or 'tümü'}. "
        "**Alfa** = aynı çıkışla aynı dönemde rastgele girişe göre fark (piyasanın kendi yükselişini ayıklar). "
        "🚩 = fiziksel olarak inandırıcı olmayan sonuç (veri hatası belirtisi) — seçimden çıkarılır.",
        "",
        "## Veri doğrulama (yfinance günlük kapanışla ay ay karşılaştırma)",
        "",
        "| Varlık | Taban | Referans | Durum | Ay | Düzeltilen ay | Atılan ay | Atılan sıçrama | Medyan sapma |",
        "|---|---|---|---|---|---|---|---|---|",
        *[f"| {v['asset']} | {v['base']} | {v['ref']} | {v['status']} | {v.get('months', '—')} | {v['fixed_months']} | {v['dropped_months']} | {v['spikes']} | "
          f"{pct(v['median_dev'])} |" for v in (vreps or [])],
        "",
        "## Özet — varlık başına en iyi (IS'te seçilen, OOS'ta ölçülen)",
        "",
        "| Varlık | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | **OOS beklenti (n)** | OOS alfa | OOS isabet | OOS PF | İşlem/ay | OOS maks. düşüş | p | Karar |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    k_sum = sum(1 for s in summary.values() if "row" in s)
    for a, s in summary.items():
        if "row" not in s:
            L.append(f"| {a} | — | | veri/sinyal yok | | | | | | | | | |")
            continue
        r, sc = s["row"], s["sc"]
        s["verdict"] = EV.verdict(r, sc, k_sum)
        s["json"]["karar"] = s["verdict"]
        L.append(f"| **{a}** | {s['tf_sel']} | {SC_TR[sc]} | {r['entry']} | {r['exit']} | {rr(r[f'{sc}_is_exp'])} ({int(r[f'{sc}_is_n'])}) | "
                 f"**{rr(r[f'{sc}_oos_exp'])}** ({int(r[f'{sc}_oos_n'])}) | {rr(r[f'{sc}_oos_alpha'])} | {pct(r[f'{sc}_oos_wr'])} | {f2(r[f'{sc}_oos_pf'])} | "
                 f"{r[f'{sc}_oos_pm']:.1f} | {f2(s['dd'][1])}R | {pv(r[f'{sc}_oos_p'])} | {s['verdict']} |")
    if port is not None:
        L += [""] + PF.render(port)
    # ısı tablosu
    tfs = tfs_run or list(C.TIMEFRAMES)
    L += ["", "## Varlık × zaman dilimi — her hücrede IS'te seçilen en iyinin OOS beklentisi", "",
          "| Varlık | " + " | ".join(tfs) + " |", "|---|" + "---|" * len(tfs)]
    k_heat = sum(1 for s in summary.values() for d in s["tf"].values() if d["row"] is not None)
    for a, s in summary.items():
        cells = []
        for tf in tfs:
            d = s["tf"].get(tf)
            if not d or d["row"] is None:
                cells.append("—")
                continue
            v = EV.verdict(d["row"], d["sc"], k_heat)[0]
            cells.append(f"{v} {rr(d['row'][d['sc'] + '_oos_exp'])} ({int(d['row'][d['sc'] + '_oos_n'])})")
        L.append(f"| **{a}** | " + " | ".join(cells) + " |")
    L.append("")

    for a, s in summary.items():
        if "row" not in s:
            continue
        L += [f"## {a}", "", f"Veri: 5m tabanı `{s['srcs'].get('5m')}` · 1h tabanı `{s['srcs'].get('1h')}`", ""]
        L += ["| ZD | Bar | IS dönemi | OOS dönemi | Maliyet / işlem | Meta-model |", "|---|---|---|---|---|---|"]
        for tf, d in s["tf"].items():
            (a0, a1), (b0, b1) = d["span"]["is"], d["span"]["oos"]
            L.append(f"| {tf} | {d['bars']:,} | {a0:%Y-%m-%d} → {a1:%Y-%m-%d} | {b0:%Y-%m-%d} → {b1:%Y-%m-%d} | {d['cost_R']:.3f}R | {d['meta'] or 'çalıştı'} |")
        L += ["", "### Strateji aileleri (her aile için tüm ZD ve yönlerde IS'te seçilen en iyi, OOS'a göre sıralı)", "",
              "| Aile | ZD | Yön | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS alfa | OOS isabet | OOS PF | p | Karar |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for tf, sc, r in s["fams"]:
            L.append(f"| **{r['family']}** | {tf} | {SC_TR[sc]} | {r['entry'].split(' · ', 1)[-1]} | {r['exit']} | {rr(r[f'{sc}_is_exp'])} ({int(r[f'{sc}_is_n'])}) | "
                     f"{rr(r[f'{sc}_oos_exp'])} ({int(r[f'{sc}_oos_n'])}) | {rr(r[f'{sc}_oos_alpha'])} | {pct(r[f'{sc}_oos_wr'])} | {f2(r[f'{sc}_oos_pf'])} | {pv(r[f'{sc}_oos_p'])} | {EV.verdict(r, sc, len(s['fams']))} |")
        L += ["", f"### Çıkış yöntemleri ({s['tf_sel']}) — girişten bağımsız etkisi", "",
              "| Çıkış | IS ilk 20 → OOS beklenti | OOS'ta pozitif kalan | OOS isabet | Tüm girişler OOS beklenti | Tüm girişler OOS isabet | Giriş sayısı |",
              "|---|---|---|---|---|---|---|"]
        for ex, m20, pos, wr20, mall, wrall, cnt in sorted(s["exits"], key=lambda x: -(x[1] if np.isfinite(x[1]) else -9)):
            L.append(f"| {ex} | {rr(m20)} | {pct(pos)} | {pct(wr20)} | {rr(mall)} | {pct(wrall)} | {cnt} |")
        rb = s["robust"]
        L += ["", f"**Sağlamlık ({s['tf_sel']}):** IS'te en iyi {rb[2]} ayarın {pct(rb[0])}'i OOS'ta pozitif kaldı, ortalama OOS beklentisi {rr(rb[1])}. "
              "(%60 altı → sonuçlar büyük ölçüde şans/aşırı uyum.)", ""]
        L += [f"### Seçilen ayarın kararlılığı — {s['row']['entry']} · {s['row']['exit']} · {SC_TR[s['sc']]}", "",
              "| Dönem | İşlem | İsabet | Beklenti |", "|---|---|---|---|"]
        for t0, t1, n, wr, e in s["blocks"]:
            L.append(f"| {t0:%Y-%m-%d} → {t1:%Y-%m-%d} | {n} | {pct(wr)} | {rr(e)} |")
        L += [f"", f"Maksimum düşüş: IS {f2(s['dd'][0])}R · OOS {f2(s['dd'][1])}R", ""]
        L += [f"### İlk 15 ayar ({s['tf_sel']}, iki yön, IS sıralı)", "",
              "| # | Giriş | Çıkış | IS beklenti (n) | OOS beklenti (n) | OOS isabet |", "|---|---|---|---|---|---|"]
        for i, (_, r) in enumerate(s["top"].iterrows(), 1):
            L.append(f"| {i} | {r['entry']} | {r['exit']} | {rr(r['both_is_exp'])} ({int(r['both_is_n'])}) | {rr(r['both_oos_exp'])} ({int(r['both_oos_n'])}) | {pct(r['both_oos_wr'])} |")
        L.append("")
    L += ["---", "Ayrıntı: `reports/secili_sonuclar.csv.gz` · `reports/en_iyi.json` · `reports/portfoy_islemler.csv.gz` · `reports/portfoy_kasa_oos.csv`", ""]
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default=",".join(C.ASSETS))
    ap.add_argument("--no-refresh", action="store_true")
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args()
    run([x.strip().upper() for x in a.assets.split(",") if x.strip()], refresh=not a.no_refresh, synth=a.synthetic)
