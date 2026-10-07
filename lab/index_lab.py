"""ENDEKS MODÜLÜ (v4) — NQ (QQQ) ve SPX (SPY) için ABD nakit seansına göre günlük stratejiler.

Neden ayrı bir motor?
  Endekslerde literatürde en dayanıklı bilinen etkiler GÜNLÜK ortalamaya dönüştür (RSI(2), IBS, N-gün dibi, ardışık
  düşüş ...) ve bunlar ATR hedefleriyle değil GÖSTERGE ÇIKIŞIYLA (kapanış > SMA5 vb.) çalışır. v3 motoru bunu
  ifade edemiyordu: SPX 4h RSI2 IS ve OOS'ta pozitif olduğu halde istatistik kapısında kalmıştı.

Kurallar (canlı bot birebir aynısını uygular — selftest T8 doğrular)
  • Günlük mum: New York 09:00–14:59 saatlik mumları (C.IDX_SESSION). Karar anı t_dec = 15:00 ET.
  • Sinyal günü d'nin karar anında: giriş = 15:00 ET saatlik mumunun açılışı (yalnızca LONG).
  • 1R = k × günlük ATR(14). Felaket stopu borsada; saatlik veride stop ya da altında açılış → min(açılış, stop).
  • Sonraki her karar gününde: çıkış koşulu doğruysa ya da tutulan gün = tmax ise 15:00 ET açılışında kapat.
  • Maliyet: Bitget gidiş-dönüş (taker×2 + spread) + günlük fonlama. R ∈ [−3, 20] kırpılır, sonra maliyet düşülür.
  • İşlem içinde 4 günden uzun veri boşluğu → işlem geçersiz (eksik veri).
"""
from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd

from . import config as C
from . import features as FT

R_CAP, R_FLOOR, GAP_DAYS = 20.0, -3.0, 4

# ───────────────────────── aileler ─────────────────────────
# her aile: test edilen parametre değerleri (grid), komşu değerler için tam ızgara (nb), çıkış seçenekleri
FAMILIES = {
    "RSI2":  {"desc": "RSI(2) < eşik", "grid": {"th": (5, 10, 15)}, "nb": {"th": (3, 5, 7, 10, 12, 15, 20)},
              "trend": (False, True), "exits": ("sma5", "rsi70")},
    "CRSI":  {"desc": "2 günlük RSI(2) toplamı < eşik", "grid": {"th": (20, 35, 50)}, "nb": {"th": (15, 20, 28, 35, 42, 50, 60)},
              "trend": (False, True), "exits": ("sma5", "rsi70")},
    "IBS":   {"desc": "IBS (kapanışın gün aralığındaki yeri) < eşik", "grid": {"th": (0.1, 0.2, 0.25)},
              "nb": {"th": (0.05, 0.1, 0.15, 0.2, 0.25, 0.3)}, "trend": (False, True), "exits": ("prevhigh", "sma5")},
    "NDLOW": {"desc": "kapanış N günün en düşüğü (Double Seven)", "grid": {"n": (5, 7, 10)}, "nb": {"n": (4, 5, 6, 7, 8, 10, 12)},
              "trend": (False, True), "exits": ("ndhigh", "sma5")},
    "DOWN":  {"desc": "art arda k düşüş kapanışı", "grid": {"k": (3, 4, 5)}, "nb": {"k": (2, 3, 4, 5, 6)},
              "trend": (False, True), "exits": ("sma5", "prevhigh")},
    "BB":    {"desc": "kapanış alt Bollinger bandının altında (20, z)", "grid": {"z": (1.5, 2.0, 2.5)},
              "nb": {"z": (1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75)}, "trend": (False, True), "exits": ("sma5", "bbmid")},
    # ── MACD kombinasyonları (kullanıcının MACD stratejisinin uyarlamaları)
    "MACDDIP": {"desc": "MACD histogramı sıfır altında, k gün düştükten sonra yukarı döndü", "grid": {"k": (2, 3, 4)},
                "nb": {"k": (1, 2, 3, 4, 5)}, "trend": (False, True), "exits": ("macd_dn", "sma5")},
    "MACDX":   {"desc": "MACD, sinyal çizgisini sıfırın ALTINDA yukarı kesti", "grid": {"fast": (12,)}, "nb": {"fast": (8, 10, 12, 14)},
                "trend": (False, True), "exits": ("macd_x", "sma5")},
    "MACDRSI": {"desc": "MACD histogramı yükselişe döndü + RSI(2) < eşik", "grid": {"th": (10, 20, 30)},
                "nb": {"th": (5, 10, 15, 20, 25, 30, 40)}, "trend": (False, True), "exits": ("sma5", "rsi70")},
    # ── trend (yavaş, az işlem; portföyde getiri sürükleyicisi olabilir)
    "TREND": {"desc": "kapanış SMA(N)'i yukarı kesti", "grid": {"n": (100, 150, 200)}, "nb": {"n": (80, 100, 125, 150, 175, 200, 230)},
              "trend": (False,), "exits": ("trend_dn",)},
}
EXIT_DESC = {"sma5": "kapanış > SMA(5)", "rsi70": "RSI(2) > 70", "prevhigh": "kapanış > önceki günün yükseği",
             "ndhigh": "kapanış N günün en yükseği", "bbmid": "kapanış > SMA(20)", "macd_dn": "MACD histogramı düşüşe döndü",
             "macd_x": "MACD sinyal çizgisinin altına indi", "trend_dn": "kapanış < SMA(N)"}


# ───────────────────────── veri ─────────────────────────
def session_daily(h: pd.DataFrame) -> pd.DataFrame:
    """Saatlik (UTC) → ABD seansı günlük mum. Sütunlar: open high low close p_last (14:00 ET mumunun konumu)
    t_dec (karar anı, UTC) e_pos (15:00 ET giriş mumunun konumu; yoksa −1)."""
    if h.empty:
        return pd.DataFrame()
    loc = h.index.tz_convert(C.IDX_TZ)
    hr = np.asarray(loc.hour)
    a, b = C.IDX_SESSION
    m = (hr >= a) & (hr <= b)
    pos = np.arange(len(h))
    day = pd.Index(loc.date)
    sub = pd.DataFrame({"open": h["open"].to_numpy(), "high": h["high"].to_numpy(), "low": h["low"].to_numpy(),
                        "close": h["close"].to_numpy(), "hr": hr, "pos": pos})[m]
    sub["day"] = day[m]
    g = sub.groupby("day", sort=True)
    d = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(), "close": g["close"].last(),
                      "last_hr": g["hr"].last(), "p_last": g["pos"].last(), "nbar": g.size()})
    d = d[(d["last_hr"] == b) & (d["nbar"] >= 4)].copy()           # seans tamam (14:00 ET mumu var)
    idx = h.index
    p_last = d["p_last"].to_numpy().astype(int)
    t_dec = idx[p_last] + pd.Timedelta(hours=1)
    nxt = p_last + 1
    ok = nxt < len(h)
    e_pos = np.full(len(d), -1, int)
    e_pos[ok] = nxt[ok]
    same = np.zeros(len(d), bool)
    same[ok] = idx[nxt[ok]] == t_dec[ok]                            # giriş mumu tam 15:00 ET'de başlamalı
    e_pos[~same] = -1
    d["t_dec"] = t_dec
    d["e_pos"] = e_pos
    d.index = pd.DatetimeIndex(pd.to_datetime(d.index))
    return d.drop(columns=["last_hr", "nbar"])


def daily_features(d: pd.DataFrame) -> dict:
    c, h, l = d["close"], d["high"], d["low"]
    tr = FT.true_range(h, l, c)
    macd = FT.ema(c, 12) - FT.ema(c, 26)
    sig = FT.ema(macd, 9)
    rng = (h - l).replace(0, np.nan)
    f = {"c": c, "h": h, "l": l, "atr": FT.rma(tr, 14), "rsi2": FT.rsi(c, 2), "sma5": c.rolling(5).mean(),
         "sma20": c.rolling(20).mean(), "sd20": c.rolling(20).std(), "ibs": ((c - l) / rng).fillna(0.5),
         "macd": macd, "sig": sig, "hist": macd - sig}
    f["crsi"] = f["rsi2"] + f["rsi2"].shift(1)
    dn = (c < c.shift(1)).astype(int)
    f["down_run"] = dn.groupby((dn == 0).cumsum()).cumsum()
    hist = f["hist"]
    hd = (hist < hist.shift(1)).astype(int)
    f["hist_fall_run"] = hd.groupby((hd == 0).cumsum()).cumsum()
    return f


def _sma(f, n):
    key = f"sma{n}"
    if key not in f:
        f[key] = f["c"].rolling(n).mean()
    return f[key]


def entry_signal(f: dict, fam: str, p: dict, trend: bool) -> np.ndarray:
    c = f["c"]
    if fam == "RSI2":
        s = f["rsi2"] < p["th"]
    elif fam == "CRSI":
        s = f["crsi"] < p["th"]
    elif fam == "IBS":
        s = f["ibs"] < p["th"]
    elif fam == "NDLOW":
        s = c <= c.rolling(int(p["n"])).min()
    elif fam == "DOWN":
        s = f["down_run"] >= int(p["k"])
    elif fam == "BB":
        s = c < f["sma20"] - p["z"] * f["sd20"]
    elif fam == "MACDDIP":
        hist = f["hist"]
        s = (hist < 0) & (hist > hist.shift(1)) & (f["hist_fall_run"].shift(1) >= int(p["k"]))
    elif fam == "MACDX":
        fast = int(p["fast"])
        mac = FT.ema(c, fast) - FT.ema(c, int(round(fast * 26 / 12)))
        sg = FT.ema(mac, 9)
        s = (mac > sg) & (mac.shift(1) <= sg.shift(1)) & (mac < 0)
    elif fam == "MACDRSI":
        hist = f["hist"]
        s = (hist > hist.shift(1)) & (hist.shift(1) <= hist.shift(2)) & (f["rsi2"].shift(1) < p["th"])
    elif fam == "TREND":
        sm = _sma(f, int(p["n"]))
        s = (c > sm) & (c.shift(1) <= sm.shift(1))
    else:
        raise KeyError(fam)
    if trend:
        s = s & (c > _sma(f, 200))
    return s.fillna(False).to_numpy(bool)


def exit_signal(f: dict, rule: str, fam: str, p: dict) -> np.ndarray:
    c = f["c"]
    if rule == "sma5":
        x = c > f["sma5"]
    elif rule == "rsi70":
        x = f["rsi2"] > 70
    elif rule == "prevhigh":
        x = c > f["h"].shift(1)
    elif rule == "ndhigh":
        x = c >= c.rolling(int(p.get("n", 7))).max()
    elif rule == "bbmid":
        x = c > f["sma20"]
    elif rule == "macd_dn":
        x = f["hist"] < f["hist"].shift(1)
    elif rule == "macd_x":
        fast = int(p.get("fast", 12))
        mac = FT.ema(c, fast) - FT.ema(c, int(round(fast * 26 / 12)))
        x = mac < FT.ema(mac, 9)
    elif rule == "trend_dn":
        x = c < _sma(f, int(p["n"]))
    else:
        raise KeyError(rule)
    return x.fillna(False).to_numpy(bool)


# ───────────────────────── bağlam ─────────────────────────
class Ctx:
    """Bir varlığın saatlik + seans günlük verisi; simülasyon için diziler."""

    def __init__(self, asset: str, h: pd.DataFrame, cost_bps: float | None = None, fund_bps_day: float | None = None):
        self.asset = asset
        self.h = h
        self.o, self.hi, self.lo = (h[k].to_numpy(float) for k in ("open", "high", "low"))
        self.ts = h.index.values.astype("datetime64[s]").astype(np.int64)
        self.d = session_daily(h)
        self.f = daily_features(self.d) if len(self.d) else {}
        self.e_pos = self.d["e_pos"].to_numpy(int) if len(self.d) else np.zeros(0, int)
        self.atr = self.f["atr"].to_numpy(float) if len(self.d) else np.zeros(0)
        self.cost = C.bitget_cost_bps(asset) if cost_bps is None else cost_bps
        self.fund = C.BITGET_FUNDING_BPS_DAY if fund_bps_day is None else fund_bps_day
        n = len(self.d)
        self.split = int(n * C.IS_FRACTION)
        self.tradeable = (self.e_pos >= 0) & np.isfinite(self.atr) & (self.atr > 0)
        self.tradeable[: min(n, C.IDX_WARMUP)] = False
        self.dec_days = np.flatnonzero(self.e_pos >= 0)      # çıkış kararı verilebilen günler
        self._sig: dict = {}

    def signals(self, spec: dict):
        key = (spec["fam"], tuple(sorted(spec["p"].items())), spec["trend"], spec["exit"])
        if key not in self._sig:
            self._sig[key] = (entry_signal(self.f, spec["fam"], spec["p"], spec["trend"]),
                              exit_signal(self.f, spec["exit"], spec["fam"], spec["p"]))
        return self._sig[key]


def _trade_from(cx: Ctx, d: int, X: np.ndarray, k: float, tmax: int, cost_mult: float = 1.0) -> dict | None:
    """Gün d karar anında açılan tek işlemin sonucu (None = geçersiz/yetersiz veri)."""
    i0 = int(cx.e_pos[d])
    e = cx.o[i0]
    dist = k * cx.atr[d]
    if not (np.isfinite(e) and dist > 0):
        return None
    stop = e - dist
    later = cx.dec_days[cx.dec_days > d]
    if len(later) == 0:
        return None
    cand = later[: tmax]
    hit = np.flatnonzero(X[cand])
    if len(hit):
        dx, why = int(cand[hit[0]]), "sinyal"
    elif len(cand) == tmax:
        dx, why = int(cand[-1]), "zaman"
    else:
        return None                                   # veri sonu: işlem tamamlanmadı
    jx = int(cx.e_pos[dx])
    seg = cx.lo[i0:jx]
    sh = np.flatnonzero(seg <= stop)
    if len(sh):
        j = i0 + int(sh[0])
        px, why = min(cx.o[j], stop), "stop"
        t_exit = cx.ts[j] + 3600
        j_end = j
    else:
        px, t_exit, j_end = cx.o[jx], cx.ts[jx], jx
    if len(cx.ts[i0:j_end + 1]) > 1 and np.diff(cx.ts[i0:j_end + 1]).max() > GAP_DAYS * 86400:
        return {"invalid": True, "j_end": j_end}
    days = (t_exit - cx.ts[i0]) / 86400.0
    R = float(np.clip((px - e) / dist, R_FLOOR, R_CAP))
    R -= cost_mult * (cx.cost / 1e4) * e / dist + (cx.fund / 1e4) * days * e / dist
    return {"d": d, "dx": dx, "i0": i0, "j_end": j_end, "entry": e, "exit": px, "stop": stop, "R": R, "why": why,
            "t_in": cx.ts[i0], "t_out": t_exit, "days": days}


def tmax_options(fam: str):
    return C.IDX_TMAX_TREND if fam == "TREND" else C.IDX_TMAX


def run_spec(cx: Ctx, spec: dict, cost_mult: float = 1.0) -> pd.DataFrame:
    """Çakışmasız backtest (tek pozisyon)."""
    L, X = cx.signals(spec)
    cand = np.flatnonzero(L & cx.tradeable)
    rows, busy_until = [], -1                       # busy_until: son işlemin bittiği saatlik konum
    for d in cand:
        if cx.e_pos[d] <= busy_until:
            continue
        t = _trade_from(cx, int(d), X, spec["k"], spec["tmax"], cost_mult)
        if t is None:
            break
        busy_until = t["j_end"]
        if t.get("invalid"):
            continue
        t["oos"] = d >= cx.split
        rows.append(t)
    cols = ["d", "dx", "entry", "exit", "stop", "R", "why", "days", "oos", "entry_time", "exit_time"]
    if not rows:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame(rows)
    df["entry_time"] = pd.to_datetime(df["t_in"], unit="s", utc=True)
    df["exit_time"] = pd.to_datetime(df["t_out"], unit="s", utc=True)
    return df[cols]


def random_base(cx: Ctx, spec: dict, oos_only: bool = True) -> float:
    """Alfa tabanı: aynı çıkış kuralı/stop/tmax ile OOS'taki HER işlem gününde girişin ortalama R'si."""
    _, X = cx.signals(spec)
    days = np.flatnonzero(cx.tradeable)
    if oos_only:
        days = days[days >= cx.split]
    Rs = []
    for d in days:
        t = _trade_from(cx, int(d), X, spec["k"], spec["tmax"])
        if t is None:
            break
        if not t.get("invalid"):
            Rs.append(t["R"])
    return float(np.mean(Rs)) if Rs else np.nan


# ───────────────────────── ayar uzayı ─────────────────────────
def spec_name(s: dict) -> str:
    fam = FAMILIES[s["fam"]]
    par = ", ".join(f"{k}={v}" for k, v in s["p"].items())
    return (f"{s['asset']} · {s['fam']}({par}){' + SMA200 trend' if s['trend'] else ''} → çıkış {s['exit']}"
            f" · stop {s['k']}ATR · en çok {s['tmax']} gün")


def all_specs(asset: str) -> list[dict]:
    out = []
    for fam, F in FAMILIES.items():
        keys = list(F["grid"])
        for vals in itertools.product(*(F["grid"][k] for k in keys)):
            p = dict(zip(keys, vals))
            for trend, ex, k, tm in itertools.product(F["trend"], F["exits"], C.IDX_STOP_K, tmax_options(fam)):
                out.append({"asset": asset, "fam": fam, "p": p, "trend": trend, "exit": ex, "k": k, "tmax": tm})
    return out


def neighbors(s: dict) -> list[tuple[str, dict]]:
    F = FAMILIES[s["fam"]]
    out = []
    for key, full in F["nb"].items():
        full = list(full)
        v = s["p"][key]
        if v in full:
            i = full.index(v)
            for j in (i - 1, i + 1):
                if 0 <= j < len(full):
                    out.append((f"{key}={full[j]}", {**s, "p": {**s["p"], key: full[j]}}))
    ks = sorted(set(C.IDX_STOP_K) | {s["k"] - 0.5, s["k"] + 0.5})
    for k in (s["k"] - 0.5, s["k"] + 0.5):
        if k > 0.5:
            out.append((f"stop {k}ATR", {**s, "k": k}))
    for tm in (max(2, int(round(s["tmax"] * 0.7))), int(round(s["tmax"] * 1.4))):
        if tm != s["tmax"]:
            out.append((f"tmax {tm}", {**s, "tmax": tm}))
    del ks
    other = [e for e in F["exits"] if e != s["exit"]]
    for e in other:
        out.append((f"çıkış {e}", {**s, "exit": e}))
    return out


def stats(R) -> dict:
    from .finalists import trade_stats
    return trade_stats(np.asarray(R, float))


def year_pos(t: pd.DataFrame) -> float:
    if t.empty:
        return np.nan
    g = t.groupby(t["entry_time"].dt.year)["R"].agg(["size", "mean"])
    g = g[g["size"] >= 5]
    return float((g["mean"] > 0).mean()) if len(g) else np.nan


# ───────────────────────── canlı karar (trader.py kullanır) ─────────────────────────
def live_decision(h: pd.DataFrame, spec: dict, now: pd.Timestamp) -> dict | None:
    """Yalnızca TAMAMLANMIŞ saatlik mumlarla, karar anı geçmiş son seans günü için giriş/çıkış kararı."""
    h = h[h.index + pd.Timedelta(hours=1) <= now]
    if len(h) < 24 * 30:
        return None
    d = session_daily(h)
    if d.empty:
        return None
    d = d[d["t_dec"] <= now]
    if d.empty:
        return None
    f = daily_features(d)
    L = entry_signal(f, spec["fam"], spec["p"], spec["trend"])
    X = exit_signal(f, spec["exit"], spec["fam"], spec["p"])
    j = len(d) - 1
    return {"day": str(d.index[j].date()), "t_dec": d["t_dec"].iloc[j], "entry": bool(L[j]) and len(d) > C.IDX_WARMUP,
            "exit": bool(X[j]), "atr": float(f["atr"].iloc[j]), "close": float(d["close"].iloc[j]),
            "decidable": bool(d["e_pos"].iloc[j] >= 0) or d["t_dec"].iloc[j] == h.index[-1] + pd.Timedelta(hours=1)}


def replay_live(h: pd.DataFrame, spec: dict) -> pd.DataFrame:
    """Selftest T8: botun her gün karar anından 10 dk sonra çalıştığını varsayıp aynı kuralları canlı mantıkla oynatır.
    Stop, borsadaki gibi saatlik mumlarla kontrol edilir. Backtest ile aynı işlemleri üretmelidir."""
    cx = Ctx(spec["asset"], h, cost_bps=0.0, fund_bps_day=0.0)
    d = cx.d
    rows, pos = [], None
    for di in range(len(d)):
        if d["e_pos"].iloc[di] < 0:
            continue
        now = d["t_dec"].iloc[di] + pd.Timedelta(minutes=10)
        j_now = int(d["e_pos"].iloc[di])
        if pos is not None:                                  # borsa stopu: giriş mumundan bu ana kadar
            seg = cx.lo[pos["i0"]:j_now]
            sh = np.flatnonzero(seg <= pos["stop"])
            if len(sh):
                j = pos["i0"] + int(sh[0])
                rows.append({"d": pos["d"], "why": "stop", "j_end": j})
                pos = None
        dec = live_decision(h, spec, now)
        if dec is None or di < C.IDX_WARMUP:
            continue
        if pos is not None:
            pos["held"] += 1
            if dec["exit"] or pos["held"] >= spec["tmax"]:
                rows.append({"d": pos["d"], "why": "sinyal" if dec["exit"] else "zaman", "j_end": j_now})
                pos = None
            continue
        if dec["entry"] and np.isfinite(dec["atr"]) and dec["atr"] > 0:
            e = cx.o[j_now]
            pos = {"d": di, "i0": j_now, "stop": e - spec["k"] * dec["atr"], "held": 0}
    return pd.DataFrame(rows)
