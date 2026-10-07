"""ATVS v4.3 — DOĞRULAMA PAKETİ: kripto günlük MACD kuralları gerçekten sağlam mı?

İki kural (v4.2'de 15 coinde geçti, burada hiç DEĞİŞTİRİLMEDEN sınanır):
  EMA : MACD yön (1s eşdeğeri) + EMA20'ye geri çekilme · iz süren stop 2.5 ATR · iki yön
  X   : MACD yön (1s eşdeğeri) + hızlı MACD(12,26,9) kesişimi · iz süren stop 2.5 ATR · yalnız LONG

Testler
  D1  Bağımlılık düzeltmeli istatistik — aynı hafta açılan işlemler tek gözlem (küme) sayılır
  D2  Batan/listeden çıkan coinler dahil (LUNA, FTT, SRM, WAVES, XEM …) — hayatta kalma yanlılığı
  D3  Placebo — MACD yönü yerine aynı süre dağılımlı RASTGELE yön (300 deneme). Gerçek kural rastgelelerin %95'inden iyi olmalı
  D4  Ayar hassasiyeti — MACD uzunlukları ×0.7…×1.3 ve EMA 15/20/25: komşu ayarların ≥ %70'i pozitif olmalı
  D5  Diğer varlıklar (bilgi) — aynı kurallar XAU, XAG, NQ, SPX günlükte
  D6  Portföy — ETH 4h Donchian (+ XAU) ile birlikte, kural başına risk ızgarası, en fazla N açık, coin başına tek pozisyon;
      Monte Carlo %95 düşüş ≤ hedef koşuluyla en yüksek CAGR; OOS (2023+) da raporlanır
Hüküm: D1–D4 geçerse kurallar canlıya (önce demo) alınabilir.

Kullanım: python run_dogrulama.py [--sentetik] [--hedef 0.15]
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

import run_kripto_gunluk as KG
from lab import config as C
from lab import data as D
from lab import exits as X
from lab import features as FT
from lab import finalists as FN
from lab import portfolio as PF
from lab import strategies as ST

DELISTED = ["LUNAUSDT", "FTTUSDT", "SRMUSDT", "WAVESUSDT", "XEMUSDT", "ANCUSDT", "MIRUSDT", "BTSUSDT"]
OTHER = ["XAU", "XAG", "NQ", "SPX"]
EXIT = "IZ_SUREN_2.5ATR"
RULES = {"EMA": "both", "X": "long"}
RULE_NAME = {"EMA": "MACD yön + EMA20'ye geri çekilme · iki yön", "X": "MACD yön + hızlı MACD kesişimi · yalnız LONG"}
OOS_START = KG.OOS_START
N_PLACEBO = int(os.getenv("ATVS_PLACEBO", "300"))
OUT = os.path.join(C.OUT_DIR, "dogrulama")
LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ───────────────────────── kurallar (lab/strategies.fam_macdyon ile birebir; selftest benzeri kontrol aşağıda) ─────────────────────────
def direction(c: pd.Series, scale: float = 1.0, tf_min: int = 1440) -> np.ndarray:
    s = C.MACD_DIR_BASE_MIN / tf_min * scale
    nf, ns, nsig = (max(2, int(round(x * s))) for x in C.MACD_DIR)
    m = FT.ema(c, nf) - FT.ema(c, ns)
    return np.sign((m - FT.ema(m, nsig)).to_numpy())


def entries(df: pd.DataFrame, d: np.ndarray, ema_len: int = 20) -> dict:
    c, h, l = (df[k].to_numpy(float) for k in ("close", "high", "low"))
    up, dn = d > 0, d < 0
    e = FT.ema(df["close"], ema_len).to_numpy()
    with np.errstate(invalid="ignore"):
        Le, Se = up & (l <= e) & (c > e), dn & (h >= e) & (c < e)
    fm = FT.ema(df["close"], 12) - FT.ema(df["close"], 26)
    xx = (fm - FT.ema(fm, 9)).to_numpy()
    Lx = up & ST.cross_up(xx, 0.0)
    z = np.zeros(len(c), bool)
    f = lambda a, n: ST.cooldown(np.nan_to_num(a.astype(float)).astype(bool), n)  # noqa: E731
    return {"EMA": (f(Le, 6), f(Se, 6)), "X": (f(Lx, 3), z)}


def placebo_dir(d: np.ndarray, rng) -> np.ndarray:
    """Gerçek yön serisinin rejim sürelerini karıştırıp rastgele işaret verir (aynı dönüş sayısı ve süre dağılımı)."""
    out = d.copy()
    ok = np.flatnonzero(np.isfinite(d))
    if len(ok) < 10:
        return out
    seg = d[ok]
    br = np.flatnonzero(np.diff(seg) != 0) + 1
    lens = np.diff(np.r_[0, br, len(seg)])
    lens = rng.permutation(lens)
    sgn = rng.choice([-1.0, 1.0])
    vals = np.concatenate([np.full(n, sgn * (1 if i % 2 == 0 else -1)) for i, n in enumerate(lens)])
    out[ok] = vals
    return out


class Coin:
    def __init__(self, name: str, df: pd.DataFrame, cost: float, tf_min: int = 1440):
        self.name, self.df, self.tf_min = name, df, tf_min
        f = FT.compute(df)
        self.c = df["close"]
        self.sm = X.simulate(df, f["atr"], cost, C.EXITS[EXIT], fund_bps_bar=C.fund_bps_bar(tf_min))
        self.sm2 = None
        self.cost = cost
        self.dir = direction(self.c, tf_min=tf_min)

    def trades(self, L, S, scope, sm=None) -> pd.DataFrame:
        sm = sm or self.sm
        valid, idx = sm["valid"], self.df.index
        ev = []
        if scope in ("long", "both"):
            ev += [(int(i), 1) for i in np.flatnonzero(L & valid)]
        if scope in ("short", "both"):
            ev += [(int(i), -1) for i in np.flatnonzero(S & valid)]
        ev.sort()
        cnt = {}
        for i, _ in ev:
            cnt[i] = cnt.get(i, 0) + 1
        rows, last = [], -1
        step = pd.Timedelta(minutes=self.tf_min)
        for i, side in ev:
            if cnt[i] > 1 or i < last:
                continue
            k, R = sm[(side, "k")][i], sm[side][i]
            if not (np.isfinite(k) and np.isfinite(R)):
                continue
            k = int(k)
            rows.append((idx[i + 1], idx[i + k] + step, side, float(R)))
            last = i + k
        return pd.DataFrame(rows, columns=["entry_time", "exit_time", "side", "R"]).assign(coin=self.name)

    def rule(self, key, d=None, ema_len=20, cost_mult=1.0):
        en = entries(self.df, self.dir if d is None else d, ema_len)
        sm = self.sm
        if cost_mult != 1.0:
            if self.sm2 is None:
                f = FT.compute(self.df)
                self.sm2 = X.simulate(self.df, f["atr"], self.cost * cost_mult, C.EXITS[EXIT], fund_bps_bar=C.fund_bps_bar(self.tf_min))
            sm = self.sm2
        L, S = en[key]
        return self.trades(L, S, RULES[key], sm)


# ───────────────────────── istatistik ─────────────────────────
def cstats(t: pd.DataFrame) -> dict:
    """Ham ve kümelenmiş (gün / hafta) t-istatistikleri. Küme-sağlam standart hata: aynı kümedeki işlemler birlikte."""
    if t.empty:
        return {"n": 0, "exp": np.nan, "t": np.nan, "t_gun": np.nan, "t_hafta": np.nan, "wr": np.nan, "kume_hafta": 0}
    R = t["R"].to_numpy()
    n, m = len(R), R.mean()
    base = FN.trade_stats(R)
    out = {"n": n, "exp": m, "t": base["t"], "wr": base["wr"]}
    for lab, key in (("gun", t["entry_time"].dt.floor("D")), ("hafta", t["entry_time"].dt.tz_localize(None).dt.to_period("W").astype(str))):
        g = pd.Series(R - m).groupby(key.values).sum()
        se = np.sqrt((g ** 2).sum()) / n
        out[f"t_{lab}"] = m / se if se > 0 else np.nan
        if lab == "hafta":
            out["kume_hafta"] = len(g)
    return out


def r_(x, d=3):
    return "—" if x is None or not np.isfinite(x) else f"{x:+.{d}f}R"


def p_(x, d=0):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.{d}f}"


def t_(x):
    return "—" if x is None or not np.isfinite(x) else f"{x:.2f}"


# ───────────────────────── ana akış ─────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentetik", action="store_true")
    ap.add_argument("--hedef", type=float, default=C.IDX_TARGET_MDD)
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    log(f"═══ ATVS v4.3 DOĞRULAMA · {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · Bitget maliyeti (taker {C.BITGET_TAKER_BPS:g} bps) ═══")

    # veri
    coins, dead = {}, {}
    for i, s in enumerate(KG.UNIVERSE + DELISTED):
        df = KG.load_daily(s, a.sentetik, i)
        if len(df) < 300:
            log(f"  {s}: veri yok/yetersiz ({len(df)}) — atlandı")
            continue
        (dead if s in DELISTED else coins)[s] = Coin(s, df, KG.cost_of(s))
        log(f"  {s}: {len(df)} gün · {df.index[0]:%Y-%m} → {df.index[-1]:%Y-%m}{' · LİSTEDEN ÇIKMIŞ' if s in DELISTED else ''}")

    # kural motoru = lab ile aynı mı? (lab/strategies.fam_macdyon)
    any_coin = next(iter(coins.values()))
    f = FT.compute(any_coin.df)
    book = ST.build_all(any_coin.df, f, 1440, np.zeros(len(any_coin.df), bool), None, "", None, families=("MACDYON",))
    en = entries(any_coin.df, any_coin.dir)
    same = all(np.array_equal(book.items[k][1], en[r][0]) and (r == "X" or np.array_equal(book.items[k][2], en[r][1]))
               for k, r in (("MACDYON · yön + EMA20'ye geri çekilme (1s eşdeğeri)", "EMA"),
                            ("MACDYON · yön + hızlı MACD(12,26,9) kesişimi (1s eşdeğeri)", "X")))
    log(f"  kural motoru lab ile birebir: {'evet' if same else 'HAYIR'}")

    res = {"ayni_motor": same}
    T = {k: pd.concat([c.rule(k) for c in coins.values()], ignore_index=True) for k in RULES}
    Td = {k: pd.concat([c.rule(k) for c in dead.values()], ignore_index=True) if dead else pd.DataFrame(columns=T[k].columns) for k in RULES}

    # D1 kümelenmiş istatistik
    d1 = {}
    for k in RULES:
        t = T[k]
        d1[k] = {"tum": cstats(t), "is": cstats(t[t["entry_time"] < OOS_START]), "oos": cstats(t[t["entry_time"] >= OOS_START])}
        log(f"  D1 {k}: tüm {r_(d1[k]['tum']['exp'])} n={d1[k]['tum']['n']} t={t_(d1[k]['tum']['t'])} · haftalık küme t={t_(d1[k]['tum']['t_hafta'])} · "
            f"OOS haftalık t={t_(d1[k]['oos']['t_hafta'])}")
    # D2 batan coinler dahil
    d2 = {}
    for k in RULES:
        both = pd.concat([T[k], Td[k]], ignore_index=True)
        d2[k] = {"dead": cstats(Td[k]), "hepsi": cstats(both), "dead_coins": sorted(Td[k]["coin"].unique().tolist()) if len(Td[k]) else []}
        log(f"  D2 {k}: batan coinlerde {r_(d2[k]['dead']['exp'])} (n={d2[k]['dead']['n']}) · hepsi birlikte {r_(d2[k]['hepsi']['exp'])}")
    # D3 placebo
    rng = np.random.default_rng(42)
    d3 = {}
    allc = list(coins.values())
    real = {k: T[k]["R"].mean() for k in RULES}
    sims = {k: [] for k in RULES}
    for j in range(N_PLACEBO):
        dirs = {c.name: placebo_dir(c.dir, rng) for c in allc}
        for k in RULES:
            parts = [c.rule(k, d=dirs[c.name]) for c in allc]
            tt = pd.concat(parts, ignore_index=True)
            sims[k].append(tt["R"].mean() if len(tt) else np.nan)
    for k in RULES:
        arr = np.array(sims[k], float)
        arr = arr[np.isfinite(arr)]
        d3[k] = {"gercek": real[k], "placebo_ort": float(arr.mean()) if len(arr) else np.nan,
                 "placebo_p95": float(np.percentile(arr, 95)) if len(arr) else np.nan,
                 "p": float((arr >= real[k]).mean()) if len(arr) else np.nan, "n": len(arr)}
        log(f"  D3 {k}: gerçek {r_(real[k])} · rastgele yön ort {r_(d3[k]['placebo_ort'])} · %95 {r_(d3[k]['placebo_p95'])} · p={d3[k]['p']:.3f}")
    # D4 ayar hassasiyeti
    d4 = {}
    for k in RULES:
        rows = []
        for sc in (0.7, 0.85, 1.0, 1.15, 1.3):
            for el in ((15, 20, 25) if k == "EMA" else (20,)):
                parts = [c.rule(k, d=direction(c.c, sc), ema_len=el) for c in allc]
                tt = pd.concat(parts, ignore_index=True)
                rows.append({"macd_olcek": sc, "ema": el, "n": len(tt), "exp": tt["R"].mean() if len(tt) else np.nan,
                             "oos_exp": tt.loc[tt["entry_time"] >= OOS_START, "R"].mean() if len(tt) else np.nan})
        tab = pd.DataFrame(rows)
        nb = tab[~((tab["macd_olcek"] == 1.0) & (tab["ema"] == 20))]
        d4[k] = {"tablo": tab, "pozitif": float((nb["exp"] > 0).mean()), "oos_pozitif": float((nb["oos_exp"] > 0).mean())}
        log(f"  D4 {k}: komşu ayarların {p_(d4[k]['pozitif'])}'ı pozitif (OOS {p_(d4[k]['oos_pozitif'])})")
    # D3b maliyet ×2
    c2 = {k: pd.concat([c.rule(k, cost_mult=C.GATE_COST_MULT) for c in allc], ignore_index=True)["R"].mean() for k in RULES}

    # D5 diğer varlıklar
    d5 = {}
    other_frames = {}
    for i, asset in enumerate(OTHER):
        try:
            if a.sentetik:
                df = KG.load_daily(asset, True, 500 + i)
            else:
                raw, _ = D.load(asset, "1h", refresh=True)
                h, _ = D.validate(asset, "1h", raw)
                df = D.resample(h, "1D")
            cc = Coin(asset, df, C.ASSETS[asset]["cost_bps"])
            other_frames[asset] = cc
            for k in RULES:
                tt = cc.rule(k)
                d5[(asset, k)] = {**cstats(tt), "oos": cstats(tt[tt["entry_time"] >= OOS_START])["exp"] if len(tt) else np.nan}
            log(f"  D5 {asset}: EMA {r_(d5[(asset, 'EMA')]['exp'])} (n={d5[(asset, 'EMA')]['n']}) · X {r_(d5[(asset, 'X')]['exp'])} (n={d5[(asset, 'X')]['n']})")
        except Exception as ex:
            log(f"  D5 {asset}: hata {type(ex).__name__}: {ex}")

    # D6 portföy
    d6 = portfolio(T, a, other_frames)

    # hüküm
    verdict = {}
    for k in RULES:
        g = {"D1 haftalık küme t ≥ 2 (tüm) ve OOS > 0": bool(d1[k]["tum"]["t_hafta"] >= 2.0 and d1[k]["oos"]["exp"] > 0),
             "D2 batan coinler dahil > 0": bool(d2[k]["hepsi"]["exp"] > 0),
             "D3 placebo p ≤ 0.05": bool(np.isfinite(d3[k]["p"]) and d3[k]["p"] <= 0.05),
             "D4 komşu ayarların ≥ %70'i pozitif": bool(d4[k]["pozitif"] >= 0.70),
             "maliyet ×2 > 0": bool(c2[k] > 0)}
        verdict[k] = {"kapilar": g, "gecti": all(g.values())}
        log(f"  HÜKÜM {k}: {'GEÇTİ' if verdict[k]['gecti'] else 'GEÇEMEDİ'}")
    render(a, coins, dead, d1, d2, d3, d4, c2, d5, d6, verdict, same, time.time() - t0)
    for k in RULES:
        T[k].to_csv(os.path.join(OUT, f"islemler_{k}.csv.gz"), index=False)
    json.dump({"olusturma": datetime.now(timezone.utc).isoformat(timespec="minutes"), "sentetik": a.sentetik,
               "hukum": {k: v["gecti"] for k, v in verdict.items()},
               "portfoy": d6.get("best_json") if d6 else None}, open(os.path.join(OUT, "sonuc.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=float)
    log(f"süre {time.time() - t0:.0f}s")


def portfolio(T: dict, a, other_frames: dict) -> dict:
    """ETH 4h Donchian (F2) ve XAU 4h (F1, Bitget taker) + kripto günlük kurallar. Coin başına tek pozisyon (küme = coin)."""
    fr = {}
    for k in RULES:
        t = T[k]
        fr[k] = pd.DataFrame({"entry_time": t["entry_time"], "exit_time": t["exit_time"], "R": t["R"],
                              "sid": k, "asset": t["coin"].str.replace("USDT", ""), "cluster": t["coin"].str.replace("USDT", "")})
    fin_path = os.path.join(C.LIVE_STATE_DIR, "finalists.json")
    if os.path.exists(fin_path) and not a.sentetik:
        try:
            import run_endeks as RE
            meta = json.load(open(fin_path, encoding="utf-8"))
            need = {f["asset"] for f in meta.get("finalistler", [])}
            H = {}
            for asset in need:
                raw, _ = D.load(asset, "1h", refresh=True)
                H[asset], _ = D.validate(asset, "1h", raw)
            for b in RE.base_finalists(H, meta):
                t = b["trades"]
                if len(t):
                    fr[b["id"]] = pd.DataFrame({"entry_time": pd.to_datetime(t["entry_time"], utc=True), "exit_time": pd.to_datetime(t["exit_time"], utc=True),
                                                "R": t["R"], "sid": b["id"], "asset": b["asset"],
                                                "cluster": b["asset"] if b["asset"] in ("ETH", "BTC") else C.CLUSTERS.get(b["asset"], b["asset"])})
        except Exception as ex:
            log(f"  D6: mevcut finalistler eklenemedi ({type(ex).__name__}: {ex})")
    sids = list(fr)
    grid = (0.0, 0.0025, 0.005, 0.0075, 0.01)
    rows = []
    for mo in (4, 6):
        for combo in itertools.product(grid, repeat=len(sids)):
            risks = dict(zip(sids, combo))
            if sum(v > 0 for v in risks.values()) == 0:
                continue
            ev = _eval(fr, risks, mo)
            if not ev:
                continue
            evo = _eval(fr, risks, mo, start=OOS_START)
            rows.append({"max_acik": mo, **{f"risk_{s}": risks[s] for s in sids}, "cagr": ev["m"]["cagr"], "mdd": ev["m"]["mdd"],
                         "p95": ev["mc"].get("p95_mdd", np.nan), "sharpe": ev["m"]["sharpe"], "islem_ay": ev["m"]["per_month"],
                         "oos_cagr": evo["m"]["cagr"] if evo else np.nan, "oos_mdd": evo["m"]["mdd"] if evo else np.nan, "_eq": ev["eq"]})
    tab = pd.DataFrame(rows)
    if tab.empty:
        return {}
    ok = tab[tab["p95"] <= a.hedef]
    best = ok.sort_values("cagr", ascending=False).iloc[0] if len(ok) else None
    # referanslar: yalnız mevcut finalistler, yalnız EMA, yalnız X — her biri hedef içinde en iyi
    refs = {}
    for lab, keep in (("Mevcut finalistler", [s for s in sids if s not in RULES]), ("Yalnız EMA", ["EMA"]), ("Yalnız X", ["X"]),
                      ("EMA + X", ["EMA", "X"])):
        m = ok.copy()
        for s in sids:
            if s not in keep:
                m = m[m[f"risk_{s}"] == 0]
        if len(m):
            refs[lab] = m.sort_values("cagr", ascending=False).iloc[0]
    if best is not None:
        best["_eq"].to_csv(os.path.join(OUT, "portfoy_kasa.csv"))
    tab.drop(columns=["_eq"]).to_csv(os.path.join(OUT, "portfoy_izgara.csv.gz"), index=False)
    bj = None
    if best is not None:
        bj = {"max_acik": int(best["max_acik"]), "riskler": {s: float(best[f"risk_{s}"]) for s in sids},
              "cagr": float(best["cagr"]), "p95_mdd": float(best["p95"]), "mdd": float(best["mdd"]), "oos_cagr": float(best["oos_cagr"])}
    return {"sids": sids, "best": best, "refs": refs, "best_json": bj}


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
    sim = PF.simulate(tr, 1.0, max_open=mo, cluster_max=1)
    if sim["equity"].empty:
        return {}
    return {"m": PF.metrics(sim["equity"], sim["taken"]), "mc": PF.monte_carlo(sim["equity"]) or {}, "eq": sim["equity"]}


def render(a, coins, dead, d1, d2, d3, d4, c2, d5, d6, verdict, same, dur):
    L = ["# ATVS v4.3 — Doğrulama paketi (kripto günlük MACD kuralları)", "",
         f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · {'**SENTETİK (test)**' if a.sentetik else 'gerçek veri'} · {len(coins)} coin + "
         f"{len(dead)} listeden çıkmış coin · Bitget maliyeti · süre {dur / 60:.0f} dk · kural motoru lab ile birebir: {'evet' if same else '**HAYIR**'}", ""]
    L += ["## Hüküm", "", "| Kural | " + " | ".join(next(iter(verdict.values()))["kapilar"]) + " | SONUÇ |",
          "|---|" + "---|" * (len(next(iter(verdict.values()))["kapilar"]) + 1)]
    for k, v in verdict.items():
        L.append(f"| {RULE_NAME[k]} | " + " | ".join("✓" if x else "✗" for x in v["kapilar"].values()) + f" | {'✅ GEÇTİ' if v['gecti'] else '❌'} |")
    L += ["", "## D1 — Bağımlılık düzeltmeli istatistik", "",
          "Kripto coinleri birlikte hareket eder; aynı hafta açılan işlemler bağımsız sayılmaz (küme-sağlam standart hata).", "",
          "| Kural | dönem | işlem | beklenti | isabet | ham t | günlük küme t | **haftalık küme t** |", "|---|---|---|---|---|---|---|---|"]
    for k in RULES:
        for lab, key in (("tüm", "tum"), ("IS <2023", "is"), ("OOS 2023+", "oos")):
            s = d1[k][key]
            L.append(f"| {k} | {lab} | {s['n']} | {r_(s['exp'])} | {p_(s['wr'])} | {t_(s['t'])} | {t_(s['t_gun'])} | **{t_(s['t_hafta'])}** |")
    L += ["", "## D2 — Listeden çıkan / batan coinler dahil", "",
          "| Kural | batan coinler | batan coinlerde | hepsi birlikte |", "|---|---|---|---|"]
    for k in RULES:
        L.append(f"| {k} | {', '.join(c.replace('USDT', '') for c in d2[k]['dead_coins']) or '—'} | {r_(d2[k]['dead']['exp'])} ({d2[k]['dead']['n']}) | "
                 f"{r_(d2[k]['hepsi']['exp'])} ({d2[k]['hepsi']['n']}) |")
    L += ["", f"## D3 — Placebo ({N_PLACEBO} rastgele yön)", "",
          "MACD yönü yerine aynı süre dağılımına sahip rastgele yön kullanıldı (EMA20 / hızlı MACD tetikleri aynı).", "",
          "| Kural | gerçek | rastgele ortalama | rastgele %95 | p (rastgele ≥ gerçek) | maliyet ×2 |", "|---|---|---|---|---|---|"]
    for k in RULES:
        L.append(f"| {k} | **{r_(d3[k]['gercek'])}** | {r_(d3[k]['placebo_ort'])} | {r_(d3[k]['placebo_p95'])} | {d3[k]['p']:.3f} | {r_(c2[k])} |")
    L += ["", "## D4 — Ayar hassasiyeti", ""]
    for k in RULES:
        tb = d4[k]["tablo"]
        L += [f"**{k}** — komşu ayarların {p_(d4[k]['pozitif'])}'ı pozitif (OOS: {p_(d4[k]['oos_pozitif'])})", "",
              "| MACD ölçeği | EMA | işlem | beklenti | OOS beklenti |", "|---|---|---|---|---|"]
        L += [f"| ×{r['macd_olcek']} | {int(r['ema'])} | {int(r['n'])} | {r_(r['exp'])} | {r_(r['oos_exp'])} |" for _, r in tb.iterrows()]
        L.append("")
    L += ["## D5 — Diğer varlıklar (bilgi; aynı kurallar, değiştirilmeden, günlük)", "",
          "| Varlık | kural | işlem | beklenti | OOS | haftalık küme t |", "|---|---|---|---|---|---|"]
    for (asset, k), s in d5.items():
        L.append(f"| {asset} | {k} | {s['n']} | {r_(s['exp'])} | {r_(s['oos'])} | {t_(s['t_hafta'])} |")
    L += ["", f"## D6 — Portföy (hedef: %95 olasılıkla düşüş ≤ {p_(a.hedef)})", ""]
    if d6 and d6.get("best") is not None:
        sids = d6["sids"]
        L += ["| Senaryo | " + " | ".join(f"risk {s}" for s in sids) + " | en fazla açık | CAGR | maks. düşüş | MC %95 | Sharpe | işlem/ay | OOS CAGR |",
              "|---|" + "---|" * (len(sids) + 7)]
        for lab, r in list(d6["refs"].items()) + [("**EN İYİ (hedef içinde)**", d6["best"])]:
            L.append(f"| {lab} | " + " | ".join(p_(r[f'risk_{s}'], 2) for s in sids) + f" | {int(r['max_acik'])} | {p_(r['cagr'], 1)} | {p_(r['mdd'], 1)} | "
                     f"{p_(r['p95'], 1)} | {r['sharpe']:.2f} | {r['islem_ay']:.1f} | {p_(r['oos_cagr'], 1)} |")
        L += ["", "Kurallar: coin başına aynı anda tek pozisyon (EMA ve X aynı coinde çakışmaz; ETH 4h Donchian ile ETH günlük de çakışmaz)."]
    else:
        L.append("Portföy hedef düşüş içinde kurulamadı.")
    L += ["", "## Notlar", "",
          "- Kurallar v4.2'deki haliyle sabittir; bu pakette hiçbir parametre sonuca bakılarak değiştirilmedi.",
          "- Batan coinler yalnızca istatistik testinde kullanılır (bugün işlem görmezler).",
          "- Geçmiş sonuçtur; önce demo."]
    open(os.path.join(OUT, "DOGRULAMA_RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    open(os.path.join(OUT, "logu.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
