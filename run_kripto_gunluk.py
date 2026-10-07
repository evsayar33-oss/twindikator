"""ATVS v4.2 — KRİPTO GÜNLÜK MACD KOMBİNASYONLARI: daha fazla veriyle yeniden sınama

Neden? v4.1'de günlük grafikte ETH/BTC MACD kombinasyonları OOS'ta pozitifti ama yalnızca 20–26 işlem vardı.
Tek coinde geçmiş uzatılamaz (ETH 2017'de başlıyor). Örneklemi büyütmenin dürüst yolu:
  1) AYNI kuralı birçok büyük coinde test etmek (havuzlanmış örneklem: yüzlerce işlem)
  2) BTC'yi yfinance ile 2014'e kadar uzatmak

Ön-kayıt (hipotezler veriye bakmadan sabitlendi, çoklu test küçük kalsın diye):
  • Girişler: yalnızca MACDYON ailesi (5 kombinasyon × 2 MACD ölçeği = 10)
  • Çıkışlar: 6 · Yönler: LONG / SHORT / iki yön → 180 kombinasyon
  • IS = 2023-01-01 öncesi · OOS = 2023-01-01 ve sonrası (tarih sabit)
  • Seçim: IS'te havuzlanmış t-istatistiğine göre ilk 10 → OOS'ta Benjamini–Hochberg (q=0.10)
  • Ek şartlar: coinlerin ≥ %60'ında tüm dönem pozitif · maliyet ×2'de pozitif · BTC 2014+ uzun testte pozitif
Maliyet: Bitget taker × 2 + spread + günlük fonlama. Karşılaştırma için aynı coinlerde DONCH ve RSI2 (filtresiz) de raporlanır.

Kullanım: python run_kripto_gunluk.py [--sentetik]
"""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

from lab import config as C
from lab import data as D
from lab import exits as X
from lab import features as FT
from lab import finalists as FN
from lab import portfolio as PF
from lab import strategies as ST

UNIVERSE = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "DOGEUSDT", "LTCUSDT", "LINKUSDT",
            "TRXUSDT", "DOTUSDT", "AVAXUSDT", "BCHUSDT", "ETCUSDT", "XLMUSDT"]
EXITS = ["SABIT_2.5R", "SABIT_4R", "TP0.5>BE_3R", "IZ_SUREN_2.5ATR", "GENIS_%50@1R>BE_3R", "%50@1R>BE_4R"]
SCOPES = ("long", "short", "both")
OOS_START = pd.Timestamp("2023-01-01", tz="UTC")
TOP_K = 10
MIN_COINS_POS = 0.60
MIN_POOLED_N = 150
TF_MIN = 1440
OUT = os.path.join(C.OUT_DIR, "kripto_gunluk")
LOG: list[str] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def cost_of(sym: str) -> float:
    a = sym.replace("USDT", "")
    return 2 * C.BITGET_TAKER_BPS + C.BITGET_SPREAD_BPS.get(a, 3.0)


# ───────────────────────── veri ─────────────────────────
def load_daily(sym: str, synth: bool, seed: int) -> pd.DataFrame:
    if synth:
        rng = np.random.default_rng(seed)
        n = 3000
        c = 100 * np.exp(np.cumsum(rng.standard_t(4, n) * 0.03))
        o = np.r_[c[0], c[:-1]]
        sp = np.abs(rng.normal(0, 0.02, n)) * c
        idx = pd.date_range(end="2026-10-01", periods=n, freq="1D", tz="UTC")
        return pd.DataFrame({"open": o, "high": np.maximum(o, c) + sp, "low": np.minimum(o, c) - sp, "close": c,
                             "volume": np.exp(rng.normal(10, 0.5, n))}, index=idx)
    os.makedirs(C.DATA_DIR, exist_ok=True)
    path = os.path.join(C.DATA_DIR, f"kripto_1d_{sym}.csv.gz")
    end = datetime.now(timezone.utc)
    if os.path.exists(path):
        old = pd.read_csv(path, index_col=0, parse_dates=True)
        old.index = pd.to_datetime(old.index, utc=True)
        new = D._binance_monthly_zips(sym, "1d", (old.index[-1] - timedelta(days=40)).to_pydatetime(), end)
        df = D._finish(pd.concat([old, new]))
    else:
        df = D._binance_monthly_zips(sym, "1d", datetime(2017, 7, 1, tzinfo=timezone.utc), end)
    df = df[df.index + pd.Timedelta(days=1) <= pd.Timestamp(end)]          # yalnızca kapanmış günler
    if len(df):
        df.to_csv(path, compression="gzip")
    return df


def load_btc_long(synth: bool) -> pd.DataFrame:
    if synth:
        return load_daily("BTCUSDT", True, 999)
    try:
        import yfinance as yf
        d = yf.download("BTC-USD", period="max", interval="1d", progress=False, auto_adjust=False)
        if isinstance(d.columns, pd.MultiIndex):
            d.columns = d.columns.get_level_values(0)
        d = d.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
        d.index = pd.to_datetime(d.index, utc=True)
        return D._finish(d)
    except Exception as e:
        log(f"  BTC uzun geçmiş alınamadı: {e}")
        return pd.DataFrame()


# ───────────────────────── backtest ─────────────────────────
def coin_trades(df: pd.DataFrame, cost: float, entries: list[str], cost_mult: float = 1.0) -> dict:
    """Her (giriş, çıkış, yön) için çakışmasız işlemler. Dönen: {(entry, exit, scope): DataFrame}"""
    f = FT.compute(df)
    book = ST.build_all(df, f, TF_MIN, np.zeros(len(df), bool), None, "", None, families=("MACDYON", "DONCH", "RSI2"))
    out = {}
    idx = df.index
    for ex in EXITS:
        sm = X.simulate(df, f["atr"], cost * cost_mult, C.EXITS[ex], fund_bps_bar=C.fund_bps_bar(TF_MIN))
        valid = sm["valid"]
        for name in entries:
            if name not in book.items:
                continue
            _, L, S = book.items[name]
            for scope in SCOPES:
                ev = []
                if scope in ("long", "both"):
                    ev += [(int(i), 1) for i in np.flatnonzero(L & valid)]
                if scope in ("short", "both"):
                    ev += [(int(i), -1) for i in np.flatnonzero(S & valid)]
                ev.sort()
                seen, rows, last = {}, [], -1
                for i, _ in ev:
                    seen[i] = seen.get(i, 0) + 1
                for i, side in ev:
                    if seen[i] > 1 or i < last:
                        continue
                    k, R = sm[(side, "k")][i], sm[side][i]
                    if not (np.isfinite(k) and np.isfinite(R)):
                        continue
                    k = int(k)
                    rows.append((idx[i + 1], idx[i + k] + pd.Timedelta(days=1), side, float(R)))
                    last = i + k
                out[(name, ex, scope)] = pd.DataFrame(rows, columns=["entry_time", "exit_time", "side", "R"])
    return out


def entry_names(df_any: pd.DataFrame) -> tuple[list[str], list[str]]:
    f = FT.compute(df_any)
    book = ST.build_all(df_any, f, TF_MIN, np.zeros(len(df_any), bool), None, "", None, families=("MACDYON", "DONCH", "RSI2"))
    macd = [k for k, v in book.items.items() if v[0] == "MACDYON"]
    base = [k for k, v in book.items.items() if v[0] in ("DONCH", "RSI2") and " + " not in k]
    return macd, base


def pooled(per_coin: dict, key) -> dict:
    parts = [t.assign(coin=c) for c, d in per_coin.items() if key in d and len(d[key]) for t in [d[key]]]
    if not parts:
        return {"trades": pd.DataFrame(columns=["entry_time", "exit_time", "side", "R", "coin"])}
    t = pd.concat(parts, ignore_index=True)
    ins, oos = t[t["entry_time"] < OOS_START], t[t["entry_time"] >= OOS_START]
    by = t.groupby("coin")["R"].agg(["size", "mean"])
    by = by[by["size"] >= 5]
    return {"trades": t, "full": FN.trade_stats(t["R"]), "ins": FN.trade_stats(ins["R"]), "oos": FN.trade_stats(oos["R"]),
            "coins_pos": float((by["mean"] > 0).mean()) if len(by) else np.nan, "n_coins": len(by)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sentetik", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    log(f"═══ KRİPTO GÜNLÜK MACD · {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · Bitget maliyeti (taker {C.BITGET_TAKER_BPS:g} bps) ═══")
    data = {}
    for i, s in enumerate(UNIVERSE):
        df = load_daily(s, a.sentetik, i)
        if len(df) > 400:
            data[s] = df
            log(f"  {s}: {len(df)} gün · {df.index[0]:%Y-%m} → {df.index[-1]:%Y-%m}")
        else:
            log(f"  {s}: yetersiz veri ({len(df)})")
    macd_entries, base_entries = entry_names(next(iter(data.values())))
    log(f"  hipotezler: {len(macd_entries)} MACD girişi × {len(EXITS)} çıkış × {len(SCOPES)} yön = {len(macd_entries) * len(EXITS) * 3}")

    per_coin = {s: coin_trades(df, cost_of(s), macd_entries + base_entries) for s, df in data.items()}
    rows = []
    for name in macd_entries + base_entries:
        for ex in EXITS:
            for sc in SCOPES:
                p = pooled(per_coin, (name, ex, sc))
                if "full" not in p:
                    continue
                rows.append({"key": (name, ex, sc), "giriş": name, "çıkış": ex, "yön": sc, "macd": name in macd_entries, **{
                    "n": p["full"]["n"], "exp": p["full"]["exp"], "is_n": p["ins"]["n"], "is_exp": p["ins"]["exp"], "is_t": p["ins"]["t"],
                    "oos_n": p["oos"]["n"], "oos_exp": p["oos"]["exp"], "oos_p": p["oos"]["p"], "wr": p["full"]["wr"],
                    "coins_pos": p["coins_pos"], "n_coins": p["n_coins"]}, "_p": p})
    res = pd.DataFrame(rows)
    mres = res[res["macd"] & (res["is_n"] >= MIN_POOLED_N)].sort_values("is_t", ascending=False)
    top = mres.head(TOP_K).copy()
    bh = FN.bh_pass([p if (e > 0) else 1.0 for p, e in zip(top["oos_p"], top["oos_exp"])], C.GATE_OOS_P)
    top["K1_OOS"] = bh
    # sağlamlık: maliyet ×2, coin genişliği, BTC uzun geçmiş
    btc = load_btc_long(a.sentetik)
    if len(btc):
        log(f"  BTC uzun geçmiş (yfinance): {len(btc)} gün · {btc.index[0]:%Y-%m} → {btc.index[-1]:%Y-%m}")
    btc_tr = coin_trades(btc, cost_of("BTCUSDT"), list(top["giriş"].unique())) if len(btc) > 400 else {}
    c2_cache = {}
    k3, k_btc, k_coin = [], [], []
    for _, r in top.iterrows():
        key = r["key"]
        c2 = []
        for s, df in data.items():
            ck = (s, key[0])
            if ck not in c2_cache:
                c2_cache[ck] = coin_trades(df, cost_of(s), [key[0]], cost_mult=C.GATE_COST_MULT)
            t = c2_cache[ck].get(key)
            if t is not None and len(t):
                c2.append(t["R"])
        e2 = float(pd.concat(c2).mean()) if c2 else np.nan
        k3.append(bool(np.isfinite(e2) and e2 > 0))
        bt = btc_tr.get(key)
        bstat = FN.trade_stats(bt[bt["entry_time"] < pd.Timestamp("2017-08-01", tz="UTC")]["R"]) if bt is not None and len(bt) else FN.trade_stats([])
        bfull = FN.trade_stats(bt["R"]) if bt is not None and len(bt) else FN.trade_stats([])
        k_btc.append(bool(np.isfinite(bfull["exp"]) and bfull["exp"] > 0))
        k_coin.append(bool(np.isfinite(r["coins_pos"]) and r["coins_pos"] >= MIN_COINS_POS))
        top.loc[_, "maliyet2_exp"] = e2
        top.loc[_, "btc_2014_exp"] = bfull["exp"]
        top.loc[_, "btc_2014_n"] = bfull["n"]
        top.loc[_, "btc_2017_oncesi_exp"] = bstat["exp"]
        top.loc[_, "btc_2017_oncesi_n"] = bstat["n"]
    top["K3_maliyet2"] = k3
    top["K_coin"] = k_coin
    top["K_btc_uzun"] = k_btc
    top["K_tüm_dönem"] = top["exp"] > 0
    top["GEÇTİ"] = top["K1_OOS"] & top["K3_maliyet2"] & top["K_coin"] & top["K_btc_uzun"] & top["K_tüm_dönem"]
    passed = top[top["GEÇTİ"]]
    log(f"  IS'te en iyi {len(top)} hipotezden geçen: {len(passed)}")

    # portföy önizlemesi: geçen en iyi kural, bütün coinlerde, işlem başına %0.5 risk, en fazla 4 açık pozisyon
    port = None
    best = passed.iloc[0] if len(passed) else (top.iloc[0] if len(top) else None)
    if best is not None:
        t = best["_p"]["trades"].copy()
        tr = pd.DataFrame({"entry_time": t["entry_time"], "exit_time": t["exit_time"], "R": t["R"], "sid": t["coin"],
                           "asset": t["coin"], "cluster": t["coin"]}).sort_values("entry_time").reset_index(drop=True)
        sim = PF.simulate(tr, 0.005, max_open=4, cluster_max=1)
        if not sim["equity"].empty:
            m = PF.metrics(sim["equity"], sim["taken"])
            mc = PF.monte_carlo(sim["equity"])
            port = {"m": m, "mc": mc}
            sim["equity"].to_csv(os.path.join(OUT, "kasa_onizleme.csv"))
    # çıktılar
    res.drop(columns=["key", "_p"]).to_csv(os.path.join(OUT, "tum_hipotezler.csv.gz"), index=False)
    top.drop(columns=["key", "_p"]).to_csv(os.path.join(OUT, "secilenler.csv"), index=False)
    if best is not None:
        best["_p"]["trades"].to_csv(os.path.join(OUT, "en_iyi_islemler.csv.gz"), index=False)
    render(res, top, passed, best, port, data, btc, time.time() - t0, a.sentetik)
    json.dump({"olusturma": datetime.now(timezone.utc).isoformat(timespec="minutes"), "gecen": [
        {"giriş": r["giriş"], "çıkış": r["çıkış"], "yön": r["yön"], "exp": r["exp"], "oos_exp": r["oos_exp"], "n": int(r["n"])}
        for _, r in passed.iterrows()]}, open(os.path.join(OUT, "sonuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    log(f"süre {time.time() - t0:.0f}s")


def r_(x):
    return "—" if x is None or not np.isfinite(x) else f"{x:+.3f}R"


def p_(x, d=0):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.{d}f}"


def render(res, top, passed, best, port, data, btc, dur, synth):
    L = ["# Kripto günlük — MACD kombinasyonları (havuzlanmış yeniden sınama)", "",
         f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · {'**SENTETİK (test)**' if synth else 'gerçek veri'} · {len(data)} coin · "
         f"Bitget maliyeti (taker {C.BITGET_TAKER_BPS:g} bps × 2 + spread, fonlama {C.BITGET_FUNDING_BPS_DAY:g} bps/gün) · süre {dur / 60:.0f} dk", "",
         f"IS = {OOS_START:%Y-%m-%d} öncesi · OOS = sonrası · seçim IS'te havuzlanmış t'ye göre ilk {TOP_K} · OOS'ta BH q={C.GATE_OOS_P}", ""]
    L += ["## Sonuç", ""]
    if len(passed):
        b = passed.iloc[0]
        L += [f"**{len(passed)} kural bütün şartları geçti.** En iyisi: **{b['giriş']} · {b['çıkış']} · {b['yön']}** — "
              f"tüm dönem {r_(b['exp'])} ({int(b['n'])} işlem), OOS {r_(b['oos_exp'])} ({int(b['oos_n'])}), coinlerin {p_(b['coins_pos'])}'ında pozitif.", ""]
    else:
        L += ["**Hiçbir MACD kombinasyonu bütün şartları geçemedi.** Günlük grafikteki ETH/BTC sonuçları büyük olasılıkla küçük örneklem şansıydı.", ""]
    if port:
        m, mc = port["m"], port["mc"]
        L += [f"Portföy önizlemesi ({'geçen' if len(passed) else 'IS en iyi (geçmedi)'} kural, tüm coinler, işlem başına %0.5 risk, en fazla 4 açık): "
              f"CAGR {p_(m['cagr'], 1)} · maks. düşüş {p_(m['mdd'], 1)} · MC %95 düşüş {p_(mc.get('p95_mdd'), 1)} · ayda {m['per_month']:.1f} işlem", ""]
    L += ["## IS'te seçilen ilk hipotezler ve şartlar", "",
          "| Giriş | Çıkış | Yön | IS t | IS (n) | OOS (n) | tüm dönem (n) | coin pozitif | maliyet×2 | BTC 2014+ (n) | K1 | geçti |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in top.iterrows():
        L.append(f"| {r['giriş']} | {r['çıkış']} | {r['yön']} | {r['is_t']:.1f} | {r_(r['is_exp'])} ({int(r['is_n'])}) | {r_(r['oos_exp'])} ({int(r['oos_n'])}) | "
                 f"{r_(r['exp'])} ({int(r['n'])}) | {p_(r['coins_pos'])} ({int(r['n_coins'])}) | {r_(r.get('maliyet2_exp'))} | "
                 f"{r_(r.get('btc_2014_exp'))} ({int(r.get('btc_2014_n') or 0)}) | {'✓' if r['K1_OOS'] else '✗'} | {'✅' if r['GEÇTİ'] else '❌'} |")
    if best is not None:
        t = best["_p"]["trades"]
        by = t.groupby("coin")["R"].agg(["size", "mean", "sum"]).sort_values("mean", ascending=False)
        L += ["", f"### Coin bazında — {best['giriş']} · {best['çıkış']} · {best['yön']}", "", "| Coin | işlem | ort. R | toplam R |", "|---|---|---|---|"]
        L += [f"| {c} | {int(r['size'])} | {r['mean']:+.3f} | {r['sum']:+.1f} |" for c, r in by.iterrows()]
        yt = t.groupby(t["entry_time"].dt.year)["R"].agg(["size", "mean"])
        L += ["", "| Yıl | işlem | ort. R |", "|---|---|---|"] + [f"| {y} | {int(r['size'])} | {r['mean']:+.3f} |" for y, r in yt.iterrows()]
    base = res[~res["macd"]].sort_values("is_t", ascending=False).head(5)
    L += ["", "## Karşılaştırma — aynı coinlerde filtresiz DONCH / RSI2 (IS'e göre ilk 5)", "",
          "| Giriş | Çıkış | Yön | IS (n) | OOS (n) | coin pozitif |", "|---|---|---|---|---|---|"]
    for _, r in base.iterrows():
        L.append(f"| {r['giriş']} | {r['çıkış']} | {r['yön']} | {r_(r['is_exp'])} ({int(r['is_n'])}) | {r_(r['oos_exp'])} ({int(r['oos_n'])}) | {p_(r['coins_pos'])} |")
    L += ["", "## Notlar", "",
          "- Coin listesi bugünün büyük coinleridir (hayatta kalma yanlılığı: batan coinler listede yok) — sonuçları biraz iyimser yapar.",
          "- BTC 2014+ testi yfinance spot verisiyledir; 2017 öncesi dönem hiç seçimde kullanılmadı (bağımsız sınav).",
          "- Bot bugün yalnızca BTC/ETH/XAU/XAG ve endeksleri işleyebilir; diğer coinler için sembol desteği gerekir."]
    open(os.path.join(OUT, "RAPOR.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    open(os.path.join(OUT, "logu.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
