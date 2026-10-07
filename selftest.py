"""ATVS öz-test — internetsiz. Her araştırma ve canlı çalıştırmadan önce iş akışında koşar.

Testler
  T1 çıkış simülatörü: vektörize ↔ tekil (canlı) birebir aynı sonuç ve çıkış zamanı
  T2 veri ayrıştırıcıları: Dukascopy mum + tick, Binance mikro-saniye, doğrulama (ölçek düzeltme / ay atma / sıçrama)
  T3 boşluk koruması
  T4 boru hattı: trend enjekte edilmiş sentetik veride araştırma → finalist → portföy uçtan uca çalışır
  T5 BOŞ HİPOTEZ: saf rastgele yürüyüşte finalist çıkmamalı (yanlış pozitif kontrolü)
  T6 canlı motor ↔ backtest: saatlik çalıştırmalar tekrar oynatılır; kâğıt işlemler backtest işlemleriyle aynı olmalı
  T7 canlı META yolu çöküşsüz çalışır
  T8 endeks motoru: canlı karar mantığı backtest ile birebir aynı işlemleri üretir
Çıkış kodu 0 = hepsi geçti.
"""
from __future__ import annotations

import io
import json
import lzma
import os
import shutil
import struct
import sys
import tempfile
import time
import traceback
import zipfile
from datetime import datetime, timezone

import numpy as np
import pandas as pd

os.environ.setdefault("ATVS_DRY", "1")
from lab import config as C  # noqa: E402
from lab import data as D  # noqa: E402
from lab import evaluate as EV  # noqa: E402
from lab import exits as X  # noqa: E402
from lab import finalists as FN  # noqa: E402
from lab import portfolio as PF  # noqa: E402

RESULTS = []


def check(name, cond, info=""):
    RESULTS.append((name, bool(cond), info))
    print(f"[{'OK ' if cond else 'HATA'}] {name} {info}")


def ohlc(c, rng, spread=0.002):
    o = np.r_[c[0], c[:-1]]
    sp = np.abs(rng.normal(0, spread, (2, len(c)))) * c
    return o, np.maximum(o, c) + sp[0], np.minimum(o, c) - sp[1]


def make_df(c, rng, start="2021-01-04"):
    o, h, l = ohlc(c, rng)
    idx = pd.date_range(start, periods=len(c), freq="1h", tz="UTC")
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": np.exp(rng.normal(10, 0.5, len(c)))}, index=idx)


def random_walk(seed, n):
    rng = np.random.default_rng(seed)
    return make_df(100 * np.exp(np.cumsum(rng.normal(0, 0.004, n))), rng)


def trending(seed, n, phi=0.12):
    """Momentum enjekte edilmiş seri: getiri, son 48 saatin ortalama getirisine bağlı (trend takibine gerçek avantaj)."""
    rng = np.random.default_rng(seed)
    e = rng.normal(0, 0.004, n)
    r = np.zeros(n)
    for t in range(n):
        r[t] = e[t] + (phi * r[max(0, t - 48):t].mean() * 48 / 6 if t > 48 else 0.0)
    return make_df(100 * np.exp(np.cumsum(r)), rng)


# ───────────────────────── T1
def t1():
    rng = np.random.default_rng(3)
    df = random_walk(5, 3000)
    atr = pd.Series(np.abs(rng.normal(0.4, 0.1, len(df))), index=df.index)
    o, h, l, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    bad = tot = 0
    for nm, cfg in C.EXITS.items():
        v = X.simulate(df, atr, 5.0, cfg, fund_bps_bar=0.4)
        for side in (1, -1):
            for i in rng.choice(np.flatnonzero(v["valid"]), 60, replace=False):
                r = X.simulate_one(o, h, l, c, atr.iloc[i], i, side, cfg, 5.0, fund_bps_bar=0.4)
                tot += 1
                if not (r["status"] == "closed" and abs(r["R"] - v[side][i]) < 1e-9 and r["exit_k"] == v[(side, "k")][i]):
                    bad += 1
    check("T1 çıkış simülatörü eşitliği", bad == 0, f"{tot - bad}/{tot}")


# ───────────────────────── T2
def t2():
    rng = np.random.default_rng(0)
    n = 1440
    p = 4200 + np.cumsum(rng.normal(0, 0.5, n))
    o, c = p, np.r_[p[1:], p[-1]]
    hi, lo = np.maximum(o, c) + 0.3, np.minimum(o, c) - 0.3
    raw = b"".join(struct.pack(">iiiiif", i * 60, int(o[i] * 1000), int(c[i] * 1000), int(lo[i] * 1000), int(hi[i] * 1000), 1.5) for i in range(n))
    rec = D._bi5_records(lzma.compress(raw, format=lzma.FORMAT_ALONE))
    rec[:, 0] += datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp()
    df = D._dk_frame(rec, C.ASSETS["XAU"]["price_range"])
    check("T2a Dukascopy mum ayrıştırma", np.allclose(df["close"].values, np.round(c * 1000) / 1000, atol=1e-3) and 4000 < df["close"].median() < 4500)
    ticks = [(k * 1500, 4200000 + k, 4199500 + k, 1.0, 2.0) for k in range(100)]
    blob = lzma.compress(b"".join(struct.pack(">IIIff", *t) for t in ticks), format=lzma.FORMAT_ALONE)

    class R:
        status_code = 200
        content = blob
    old = D._get
    D._get = lambda *a, **k: R()
    try:
        tk = D._dk_tick_hour("XAUUSD", datetime(2026, 10, 2, 10, tzinfo=timezone.utc))
    finally:
        D._get = old
    tdf = D._dk_frame(tk, C.ASSETS["XAU"]["price_range"])
    check("T2b Dukascopy tick → 1 dk mum", len(tdf) == 3 and abs(tdf["open"].iloc[0] - 4199.5) < 1e-6)
    ts = (np.arange(3) * 300_000 + 1735689600000) * 1000
    t = np.where(ts > 10 ** 14, ts // 1000, ts)
    check("T2c Binance mikro-saniye zaman", pd.to_datetime(t, unit="ms", utc=True)[0] == pd.Timestamp("2025-01-01", tz="UTC"))
    idx = pd.date_range("2024-01-01", periods=24 * 200, freq="1h", tz="UTC")
    cc = 2000 * np.exp(np.cumsum(np.random.default_rng(1).normal(0, 0.002, len(idx))))
    good = pd.DataFrame({"open": cc, "high": cc * 1.001, "low": cc * 0.999, "close": cc, "volume": 1.0}, index=idx)
    ref = good["close"].resample("1D").last()
    ref.index = ref.index.tz_localize(None)
    D._YF_DAILY["GC=F"] = ref * 1.01
    bad = good.copy()
    bad.loc[bad.index.month == 3, ["open", "high", "low", "close"]] *= 10
    bad.loc[bad.index.month == 5, ["open", "high", "low", "close"]] *= 1.4
    bad.iloc[1000, 3] *= 1.5
    out, rep = D.validate("XAU", "1h", bad)
    check("T2d doğrulama (ölçek düzelt / ay at / sıçrama)", rep["fixed_months"] == 1 and rep["dropped_months"] == 1 and rep["spikes"] == 1
          and np.allclose(out[out.index.month == 3]["close"], good[good.index.month == 3]["close"]), str({k: rep[k] for k in ('fixed_months', 'dropped_months', 'spikes')}))
    D._YF_DAILY.pop("GC=F", None)


# ───────────────────────── T3
def t3():
    idx = pd.date_range("2024-01-01", periods=300, freq="1h", tz="UTC").append(pd.date_range("2024-03-01", periods=300, freq="1h", tz="UTC"))
    c = np.linspace(100, 110, 600)
    c[300:] += 50
    df = pd.DataFrame({"open": c, "high": c + 0.1, "low": c - 0.1, "close": c, "volume": 1.0}, index=idx)
    r = X.simulate(df, pd.Series(0.2, index=idx), 0, C.EXITS["SABIT_2R"])
    bad = np.flatnonzero(~r["valid"][:550])
    check("T3 boşluk koruması", len(bad) and bad.min() >= 250 and bad.max() == 299 and np.nanmax(np.abs(r[1])) < 3)


# ───────────────────────── T4 / T5
def pipeline(dfs: dict, tfs=("4h",)):
    research, ctxs = {}, {}
    for a, base in dfs.items():
        for tf in tfs:
            df = D.resample(base, C.TIMEFRAMES[tf]["rule"])
            res, aux = EV.evaluate(df, C.ASSETS[a]["cost_bps"], FN.TF_MIN[tf], None, "", None)
            res.insert(0, "tf", tf)
            res.insert(0, "asset", a)
            research[(a, tf)] = res
            ctxs[(a, tf)] = FN.DataCtx(a, tf, df, None, "", None)
    fin = FN.run(ctxs, research, log=lambda *a: None)
    port = PF.run(fin["finalists"])
    return fin, port


def t4():
    old_seeds = C.FINAL_SEEDS
    C.FINAL_SEEDS = []
    try:
        fin, port = pipeline({"XAU": trending(11, 24 * 365 * 4), "ETH": trending(12, 24 * 365 * 4)})
        md = "\n".join(FN.render(fin) + PF.render(port))
        check("T4 boru hattı (trend verisi → finalist + portföy)", len(fin["finalists"]) >= 1 and bool(port.get("ok")) and ("Önerilen" in md or "⚠️" in md),
              f"finalist={len(fin['finalists'])} risk={port.get('rec', {}) and port['rec']['risk'] if port.get('ok') else None}")
        json.dumps(FN.to_json(fin["finalists"], 0.005), default=str)
        return fin
    finally:
        C.FINAL_SEEDS = old_seeds


def t5():
    old_seeds = C.FINAL_SEEDS
    C.FINAL_SEEDS = []
    try:
        fin, _ = pipeline({"XAU": random_walk(21, 24 * 365 * 4), "ETH": random_walk(22, 24 * 365 * 4)})
        check("T5 boş hipotez (rastgele yürüyüşte finalist yok)", len(fin["finalists"]) == 0, f"finalist={len(fin['finalists'])}, aday={fin['n_tested']}")
    finally:
        C.FINAL_SEEDS = old_seeds


# ───────────────────────── T6 / T7
def _replay(LV, full, asset, tf, entry, ex, scope, n_trades=20, lag_prob=0.0, skip_prob=0.0):
    """lag_prob: verinin son saati henüz yayımlanmamış gibi davran; skip_prob: iş akışı çalışmamış gibi atla."""
    rng = np.random.default_rng(5)
    df_tf = full if tf == "1h" else D.resample(full, C.TIMEFRAMES[tf]["rule"])
    dc = FN.DataCtx(asset, tf, df_tf, None, "", None)
    bt = FN.run_spec(dc, entry, C.EXITS[ex], scope)["trades"]
    start = bt["exit_time"].iloc[max(0, len(bt) - n_trades - 1)]      # backtest bu anda pozisyonsuz
    end = df_tf.index[-C.HORIZON - 2]
    fz = {"id": f"TEST_{tf}", "asset": asset, "tf": tf, "family": FN.family_of(entry), "entry": entry, "exit": ex, "exit_cfg": C.EXITS[ex],
          "scope": scope, "cost_bps": C.ASSETS[asset]["cost_bps"], "horizon": C.HORIZON, "risk_per_trade": 0.005, "backtest": {"exp": 0.1}}
    for f_ in (LV.POS_FILE, LV.LEDGER):
        if os.path.exists(f_):
            os.remove(f_)
    with open(LV.FIN_FILE, "w") as fh:
        json.dump({"finalistler": [fz]}, fh)
    step = f"{FN.TF_MIN[tf]}min"
    runs = pd.date_range(start.ceil(step) + pd.Timedelta(minutes=7), end, freq=step)
    t0 = time.time()
    for T in list(runs) + [runs[-1] + pd.Timedelta(minutes=FN.TF_MIN[tf])] * 2:
        if T != runs[-1] and T < runs[-1] and rng.random() < skip_prob:
            continue
        lag = pd.Timedelta(hours=2 if (T < runs[-1] and rng.random() < lag_prob) else 1)
        os.environ["ATVS_NOW"] = str(T)
        LV._BASES.clear()
        LV._BASES[asset] = full[full.index + lag <= T]
        LV.SENT.clear()
        LV.main()
    os.environ.pop("ATVS_NOW", None)
    lg = pd.read_csv(LV.LEDGER) if os.path.exists(LV.LEDGER) else pd.DataFrame(columns=LV.LEDGER_COLS)
    sig_bt = bt[(bt["entry_time"] > start) & (bt["exit_time"] <= runs[-1])]
    live_t = dict(zip(pd.to_datetime(lg["signal_time"], utc=True), lg["R"]))
    bt_t = dict(zip(df_tf.index[sig_bt["bar"].to_numpy()], sig_bt["R"]))
    same = set(live_t) == set(bt_t) and all(abs(live_t[k] - bt_t[k]) < 1e-3 for k in bt_t)
    check(f"T6 canlı motor = backtest ({tf} · {ex}{' · gecikmeli/atlanan çalıştırma' if lag_prob or skip_prob else ''})", len(bt_t) > 3 and same,
          f"canlı {len(live_t)} / backtest {len(bt_t)} işlem, ortak sinyal {len(set(live_t) & set(bt_t))} · {len(runs)} çalıştırma {time.time() - t0:.0f}s")


def t6():
    import live as LV
    tmp = tempfile.mkdtemp()
    old_bars, old_base = C.LIVE_BARS, LV.base_1h
    try:
        C.LIVE_BARS = 1200
        LV.STATE = tmp
        LV.POS_FILE, LV.LEDGER, LV.FIN_FILE = (os.path.join(tmp, f) for f in ("positions.json", "ledger.csv", "finalists.json"))
        LV.base_1h = lambda a: LV._BASES[a]
        full = trending(31, 24 * 365 * 3)
        _replay(LV, full, "XAU", "4h", "DONCH · Donchian 20 · filtresiz", "TP1>BE_3R", "both")
        _replay(LV, full, "XAU", "4h", "DONCH · Donchian 20 · filtresiz", "TP1>BE_3R", "both", lag_prob=0.3, skip_prob=0.2)
        _replay(LV, full, "XAU", "1h", "MA · EMA 20/50 kesişimi", "%50@1R>BE_IZ", "long", n_trades=12)
        # T7: META canlı yolu
        LV._BASES["XAU"] = full
        os.environ["ATVS_NOW"] = str(full.index[-1] + pd.Timedelta(hours=1))
        ctx = LV.build("XAU", "4h", "META")
        check("T7 canlı META yolu", any(k.startswith("META") for k in ctx["book"].items) or ctx.get("meta"), f"meta: {ctx.get('meta') or 'tamam'}")
        os.environ.pop("ATVS_NOW", None)
    finally:
        C.LIVE_BARS = old_bars
        LV.base_1h = old_base
        shutil.rmtree(tmp, ignore_errors=True)


# ───────────────────────── T8 endeks motoru: canlı karar = backtest
def t8():
    from lab import index_lab as IL
    rng = np.random.default_rng(8)
    idx = pd.date_range("2021-01-03", periods=int(2.2 * 365 * 24), freq="h", tz="UTC")
    loc = idx.tz_convert("America/New_York")
    idx = idx[~((loc.dayofweek == 5) | ((loc.dayofweek == 4) & (loc.hour >= 17)) | ((loc.dayofweek == 6) & (loc.hour < 18)))]
    c = 4000 * np.exp(np.cumsum(rng.normal(0.00005, 0.003, len(idx))))
    o = np.r_[c[0], c[:-1]]
    sp = np.abs(rng.normal(0, 0.001, len(idx))) * c
    h = pd.DataFrame({"open": o, "high": np.maximum(o, c) + sp, "low": np.minimum(o, c) - sp, "close": c, "volume": 1.0}, index=idx)
    cx = IL.Ctx("SPX", h, cost_bps=0, fund_bps_day=0)
    allok, tot = True, 0
    for spec in ({"asset": "SPX", "fam": "RSI2", "p": {"th": 10}, "trend": False, "exit": "sma5", "k": 1.5, "tmax": 5},
                 {"asset": "SPX", "fam": "IBS", "p": {"th": 0.25}, "trend": False, "exit": "prevhigh", "k": 2.5, "tmax": 10}):
        bt = IL.run_spec(cx, spec)
        _, X = cx.signals(spec)
        a = [(d, w, IL._trade_from(cx, int(d), X, spec["k"], spec["tmax"])["j_end"]) for d, w in zip(bt["d"], bt["why"])]
        rp = IL.replay_live(h, spec)
        b = list(zip(rp["d"], rp["why"], rp["j_end"])) if len(rp) else []
        allok &= len(a) > 5 and a == b[: len(a)]
        tot += len(a)
    check("T8 endeks motoru: canlı karar = backtest (stop/sinyal/zaman çıkışları)", allok, f"{tot} işlem")


def main(fast: bool = False):
    t0 = time.time()
    tests = [t1, t2, t3, t6, t8] if fast else [t1, t2, t3, t4, t5, t6, t8]
    for t in tests:
        try:
            t()
        except Exception:
            check(t.__name__, False, traceback.format_exc()[-1500:])
    ok = all(r[1] for r in RESULTS)
    print(f"\nÖZ-TEST: {'GEÇTİ' if ok else 'BAŞARISIZ'} · {sum(r[1] for r in RESULTS)}/{len(RESULTS)} · {time.time() - t0:.0f}s")
    with open("selftest_sonuc.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(f"{'OK' if r[1] else 'HATA'} {r[0]} {r[2]}" for r in RESULTS))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(fast="--fast" in sys.argv))
