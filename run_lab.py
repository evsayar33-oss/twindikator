"""ATVS Lab — varlık × zaman dilimi × gösterge kombinasyonu araştırması.

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
from lab import engine as E

SCOPES = ("both", "long", "short")
SCOPE_TR = {"both": "iki yön", "long": "yalnız LONG", "short": "yalnız SHORT"}


# ───────────────────────── SEÇİM ─────────────────────────
def pick(res: pd.DataFrame, scope: str) -> pd.Series | None:
    """IS (ilk %70) üzerinde seç: önce yeterli işlem + pozitif beklenti + tabanın üstünde isabet,
    sonra isabetin Wilson alt sınırına göre sırala (küçük örneklem şansını cezalandırır)."""
    n, exp, edge, wlb = (res[f"{scope}_is_{k}"] for k in ("n", "exp", "edge", "wlb"))
    elig = res[(n >= C.MIN_TRADES_IS) & (exp > 0) & (edge > 0)]
    if elig.empty:
        elig = res[n >= C.MIN_TRADES_IS]
    if elig.empty:
        return None
    return elig.loc[elig[f"{scope}_is_wlb"].idxmax()]


def verdict(row: pd.Series, scope: str) -> str:
    n, wr, base, exp, p = (row[f"{scope}_oos_{k}"] for k in ("n", "wr", "base", "exp", "p"))
    if n < C.MIN_TRADES_OOS or not np.isfinite(wr):
        return "⏳ OOS yetersiz"
    if wr > base and exp > 0 and p < 0.05:
        return "✅ Kanıtlı"
    if wr > base and exp > 0:
        return "⚠️ Zayıf (anlamsız)"
    return "❌ OOS'ta tutmadı"


def key_of(row: pd.Series) -> tuple:
    s = tuple(row["subset"].split("+"))
    f = tuple() if row["filters"] == "-" else tuple(row["filters"].split("+"))
    return (s, row["mode"], f)


def pct(x) -> str:
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.1f}"


def num(x, f="{:+.2f}") -> str:
    return "—" if x is None or not np.isfinite(x) else f.format(x)


def pval(x) -> str:
    return "—" if x is None or not np.isfinite(x) else ("<0.001" if x < 0.001 else f"{x:.3f}")


# ───────────────────────── SENTETİK VERİ ─────────────────────────
def synthetic(base: str, years: float, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    step = pd.Timedelta("5min") if base == "5m" else pd.Timedelta("1h")
    n = int(years * 365 * 24 * (12 if base == "5m" else 1))
    vol = np.exp(np.cumsum(rng.normal(0, 0.02, n)) * 0.05) * (0.0015 if base == "5m" else 0.005)
    ret = rng.standard_t(4, n) * vol * 0.6
    c = 100 * np.exp(np.cumsum(ret))
    o = np.r_[c[0], c[:-1]]
    sp = np.abs(rng.normal(0, vol, n)) * c
    h, l = np.maximum(o, c) + sp, np.minimum(o, c) - sp
    v = np.exp(rng.normal(10, 0.6, n) + 3 * np.abs(ret) / vol.mean())
    idx = pd.date_range(end=pd.Timestamp.now(tz="UTC").floor("h"), periods=n, freq=step)
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": v}, index=idx)


# ───────────────────────── ANA AKIŞ ─────────────────────────
def run(assets: list[str], refresh: bool, synth: bool) -> dict:
    os.makedirs(C.OUT_DIR, exist_ok=True)
    all_rows, summary = [], {}
    n_cfg = len(E.SUBSETS) * len(E.MODES) * len(E.FSETS)
    for ai, asset in enumerate(assets):
        t0 = time.time()
        print(f"\n═══ {asset} ═══")
        bases, srcs = {}, {}
        for b in ("5m", "1h"):
            if synth:
                yrs = 0.5 if b == "5m" else 3
                bases[b], srcs[b] = synthetic(b, yrs, 100 * ai + (1 if b == "1h" else 0)), "SENTETİK"
            else:
                bases[b], srcs[b] = D.load(asset, b, refresh=refresh)
            df = bases[b]
            print(f"  taban {b}: {len(df):,} bar  {df.index[0] if len(df) else '-'} → {df.index[-1] if len(df) else '-'}  [{srcs[b]}]")

        tf_res, tf_aux = {}, {}
        for tf, spec in C.TIMEFRAMES.items():
            base = bases[spec["base"]]
            if base.empty:
                print(f"  {tf}: veri yok, atlandı")
                continue
            native = {"5m": "5min", "1h": "1h"}[spec["base"]]
            df = base if spec["rule"] == native else D.resample(base, spec["rule"])
            if len(df) < C.DYN_LEN * 3:
                print(f"  {tf}: yetersiz bar ({len(df)}), atlandı")
                continue
            res, aux = E.evaluate(df, C.ASSETS[asset]["cost_bps"])
            res.insert(0, "tf", tf)
            res.insert(0, "asset", asset)
            aux["bars"], aux["first"], aux["last"] = len(df), df.index[0], df.index[-1]
            tf_res[tf], tf_aux[tf] = res, aux
            all_rows.append(res)
            b = pick(res, "both")
            print(f"  {tf}: {len(df):,} bar · {n_cfg} kombinasyon · en iyi IS isabet {pct(b['both_is_wr']) if b is not None else '—'} → OOS {pct(b['both_oos_wr']) if b is not None else '—'}")

        summary[asset] = analyse_asset(asset, tf_res, tf_aux, srcs)
        print(f"  süre {time.time() - t0:.1f}s")

    full = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    if not full.empty:
        full.to_csv(os.path.join(C.OUT_DIR, "tum_sonuclar.csv.gz"), index=False, compression="gzip")
    with open(os.path.join(C.OUT_DIR, "en_iyi.json"), "w", encoding="utf-8") as fh:
        json.dump({a: s.get("json", {}) for a, s in summary.items()}, fh, ensure_ascii=False, indent=2, default=str)
    md = render(summary, n_cfg, synth)
    with open(os.path.join(C.OUT_DIR, "RAPOR.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(md)
    print(f"\nRapor: {os.path.join(C.OUT_DIR, 'RAPOR.md')}")
    return summary


def analyse_asset(asset, tf_res, tf_aux, srcs) -> dict:
    out = {"srcs": srcs, "tf": {}, "json": {}}
    if not tf_res:
        return out
    for tf, res in tf_res.items():
        out["tf"][tf] = {sc: pick(res, sc) for sc in SCOPES}
        out["tf"][tf]["bars"] = tf_aux[tf]["bars"]
        out["tf"][tf]["span"] = (tf_aux[tf]["first"], tf_aux[tf]["last"])
    # zaman dilimi seçimi: iki yönlü en iyi kombinasyonun IS Wilson alt sınırı
    cands = [(tf, d["both"]) for tf, d in out["tf"].items() if d["both"] is not None]
    if not cands:
        return out
    best_tf, best = max(cands, key=lambda x: x[1]["both_is_wlb"])
    # yön kapsamı: aynı ZD'de iki yön / yalnız long / yalnız short — IS Wilson alt sınırına göre
    scs = [(sc, out["tf"][best_tf][sc]) for sc in SCOPES if out["tf"][best_tf][sc] is not None]
    best_sc, best_sc_row = max(scs, key=lambda x: x[1][f"{x[0]}_is_wlb"])
    res, aux = tf_res[best_tf], tf_aux[best_tf]
    singles = res[(res["n_osc"] == 1) & (res["n_flt"] == 0)].copy()
    out.update({
        "best_tf": best_tf, "best": best, "best_scope": best_sc, "best_scope_row": best_sc_row,
        "singles": singles, "ablation": E.ablation(res, "both"),
        "stability": E.block_stability(aux, key_of(best_sc_row), best_sc),
        "top": res[res["both_is_n"] >= C.MIN_TRADES_IS].sort_values("both_is_wlb", ascending=False).head(10),
        "verdict": verdict(best_sc_row, best_sc),
    })
    r = best_sc_row
    out["json"] = {
        "zaman_dilimi": best_tf, "yon": best_sc,
        "rsi": "R" in r["subset"].split("+"), "stoch": "S" in r["subset"].split("+"), "wavetrend": "W" in r["subset"].split("+"),
        "esik": r["mode"], "filtreler": [] if r["filters"] == "-" else r["filters"].split("+"),
        "kombinasyon": r["name"],
        "is_isabet": r[f"{best_sc}_is_wr"], "is_n": int(r[f"{best_sc}_is_n"]),
        "oos_isabet": r[f"{best_sc}_oos_wr"], "oos_n": int(r[f"{best_sc}_oos_n"]),
        "oos_taban": r[f"{best_sc}_oos_base"], "oos_beklenti_R": r[f"{best_sc}_oos_exp"], "oos_p": r[f"{best_sc}_oos_p"],
        "karar": out["verdict"],
    }
    return out


# ───────────────────────── RAPOR ─────────────────────────
def render(summary: dict, n_cfg: int, synth: bool) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    be = C.SL_ATR / (C.TP_ATR + C.SL_ATR)
    L = [f"# ATVS Lab Raporu — {now}", ""]
    if synth:
        L += ["> ⚠️ **SENTETİK VERİ** — yalnızca boru hattı testi; sonuçlar anlamsızdır.", ""]
    L += [
        "**Yöntem.** Her varlık × zaman dilimi için "
        f"{n_cfg} kombinasyon (7 osilatör alt kümesi × 2 eşik tipi × 16 filtre kümesi), LONG ve SHORT ayrı. "
        f"Giriş: sinyal barından sonraki açılış · Çıkış: TP {C.TP_ATR} ATR / SL {C.SL_ATR} ATR / {C.HORIZON} bar · "
        f"maliyet dahil · aynı barda TP+SL = zarar. Başabaş isabet ≈ %{100 * be:.0f}.",
        "",
        f"**Seçim yalnızca ilk %{int(C.IS_FRACTION * 100)} veride (IS)** yapılır; tabloda asıl ölçü **son %{int(100 - C.IS_FRACTION * 100)} (OOS)** sonucudur. "
        "Taban = aynı dönemde her bara rastgele girişin isabeti (piyasanın kendi eğilimi). "
        "p = OOS isabetinin tabandan şans eseri yüksek çıkma olasılığı. "
        f"Varlık başına ~{n_cfg * 3 * len(C.TIMEFRAMES):,} test yapıldığı için IS rakamları iyimserdir; güvenilecek sütun OOS'tur.",
        "",
        "## Özet",
        "",
        "| Varlık | ZD | Yön | Kombinasyon | IS isabet (n) | **OOS isabet (n)** | OOS taban | OOS beklenti | p | Karar |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for a, s in summary.items():
        if "best_tf" not in s:
            L.append(f"| {a} | — | — | veri yok | | | | | | |")
            continue
        r, sc = s["best_scope_row"], s["best_scope"]
        L.append(
            f"| **{a}** | {s['best_tf']} | {SCOPE_TR[sc]} | {r['name']} | {pct(r[f'{sc}_is_wr'])} ({int(r[f'{sc}_is_n'])}) | "
            f"**{pct(r[f'{sc}_oos_wr'])}** ({int(r[f'{sc}_oos_n'])}) | {pct(r[f'{sc}_oos_base'])} | {num(r[f'{sc}_oos_exp'])}R | "
            f"{pval(r[f'{sc}_oos_p'])} | {s['verdict']} |"
        )
    L.append("")
    for a, s in summary.items():
        if "best_tf" not in s:
            continue
        L += [f"## {a}", "", f"Veri: 5m tabanı `{s['srcs'].get('5m')}`, 1h tabanı `{s['srcs'].get('1h')}`", ""]
        L += ["### Zaman dilimi karşılaştırması (her ZD'de IS'te seçilen en iyi iki yönlü kombinasyon)", "",
              "| ZD | Bar | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p | Karar |", "|---|---|---|---|---|---|---|---|---|"]
        for tf, d in s["tf"].items():
            r = d["both"]
            mark = " ◀" if tf == s["best_tf"] else ""
            if r is None:
                L.append(f"| {tf}{mark} | {d['bars']:,} | yetersiz sinyal | | | | | | |")
                continue
            L.append(f"| {tf}{mark} | {d['bars']:,} | {r['name']} | {pct(r['both_is_wr'])} ({int(r['both_is_n'])}) | {pct(r['both_oos_wr'])} ({int(r['both_oos_n'])}) | "
                     f"{pct(r['both_oos_base'])} | {num(r['both_oos_exp'])}R | {pval(r['both_oos_p'])} | {verdict(r, 'both')} |")
        L += ["", f"### Yön ayrımı ({s['best_tf']})", "", "| Kapsam | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti | p |", "|---|---|---|---|---|---|---|"]
        for sc in SCOPES:
            r = s["tf"][s["best_tf"]][sc]
            if r is None:
                L.append(f"| {SCOPE_TR[sc]} | yetersiz | | | | | |")
                continue
            L.append(f"| {SCOPE_TR[sc]} | {r['name']} | {pct(r[f'{sc}_is_wr'])} ({int(r[f'{sc}_is_n'])}) | {pct(r[f'{sc}_oos_wr'])} ({int(r[f'{sc}_oos_n'])}) | "
                     f"{pct(r[f'{sc}_oos_base'])} | {num(r[f'{sc}_oos_exp'])}R | {pval(r[f'{sc}_oos_p'])} |")
        L += ["", f"### Tekli göstergeler, filtresiz ({s['best_tf']}, iki yön)", "", "| Gösterge | Eşik | IS isabet (n) | OOS isabet (n) | OOS taban | OOS beklenti |", "|---|---|---|---|---|---|"]
        for _, r in s["singles"].sort_values(["subset", "mode"]).iterrows():
            L.append(f"| {E.OSC_NAME[r['subset']]} | {E.MODE_NAME[r['mode']]} | {pct(r['both_is_wr'])} ({int(r['both_is_n'])}) | {pct(r['both_oos_wr'])} ({int(r['both_oos_n'])}) | {pct(r['both_oos_base'])} | {num(r['both_oos_exp'])}R |")
        L += ["", f"### Bileşen katkısı ({s['best_tf']}) — yalnızca o bileşende farklı ayar çiftlerinde ortalama isabet farkı", "", "| Bileşen | Δ isabet | Çift sayısı |", "|---|---|---|"]
        for k, (dv, cnt) in s["ablation"].items():
            nm = "Dinamik eşik (sabite göre)" if k == "DYN" else E.FILTER_NAME[k]
            L.append(f"| {nm} | {'—' if not np.isfinite(dv) else f'{100 * dv:+.1f} puan'} | {cnt} |")
        L += ["", f"### Kararlılık — seçilen ayar ({SCOPE_TR[s['best_scope']]}), tüm dönem {C.N_BLOCKS} blok", "", "| Dönem | n | İsabet | Taban | Beklenti |", "|---|---|---|---|---|"]
        for b in s["stability"]:
            L.append(f"| {b['start']:%Y-%m-%d} → {b['end']:%Y-%m-%d} | {b['n']} | {pct(b['wr'])} | {pct(b['base'])} | {num(b['exp'])}R |")
        L += ["", f"### İlk 10 kombinasyon ({s['best_tf']}, IS sıralı, iki yön)", "", "| # | Kombinasyon | IS isabet (n) | OOS isabet (n) | OOS beklenti |", "|---|---|---|---|---|"]
        for i, (_, r) in enumerate(s["top"].iterrows(), 1):
            L.append(f"| {i} | {r['name']} | {pct(r['both_is_wr'])} ({int(r['both_is_n'])}) | {pct(r['both_oos_wr'])} ({int(r['both_oos_n'])}) | {num(r['both_oos_exp'])}R |")
        L.append("")
    L += ["---", "Ayrıntılı tüm sonuçlar: `reports/tum_sonuclar.csv.gz` · Pine ayarları: `reports/en_iyi.json`", ""]
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default=",".join(C.ASSETS))
    ap.add_argument("--no-refresh", action="store_true")
    ap.add_argument("--synthetic", action="store_true")
    a = ap.parse_args()
    run([x.strip().upper() for x in a.assets.split(",") if x.strip()], refresh=not a.no_refresh, synth=a.synthetic)
