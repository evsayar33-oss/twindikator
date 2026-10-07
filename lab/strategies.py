"""Strateji aileleri. Her aile LONG/SHORT olay maskeleri üretir (sinyal barı kapanışında bilinir).

Aileler:
  OSC      RSI/Stoch/WaveTrend dönüşü (7 alt küme × sabit/dinamik × 16 filtre)
  REJIM    Rejim anahtarı: yatayda dönüş, trendde geri çekilme, ikisinin birleşimi
  RSI2     Connors tipi kısa vadeli aşırılık
  DONCH    Donchian kırılımı (20/55) + filtreler
  MA       Hareketli ortalama kesişimi, zaman serisi momentumu
  SQZ      Bollinger-Keltner sıkışma çözülmesi
  VWAP     Seans VWAP sapma dönüşü / VWAP trend
  ORB      Açılış aralığı kırılımı (New York 09:30, Londra 08:00)
  IMOM     Gün içi momentum (Gao vd. 2018): sabah getirisi → 15:30 yönü
  SEZON    Saat etkisi (yalnızca IS'te öğrenilir)
  PAIR     Eş varlığa göre göreli değer dönüşü (XAU/XAG, BTC/ETH, NQ/SPX)
  LEADLAG  Eş varlıktaki ani hareketi takip
  FUNDING  Kripto fonlama oranı uç değerleri (kalabalığa karşı)
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd

from . import config as C
from . import features as FT

OSC = ("R", "S", "W")
OSC_NAME = {"R": "RSI", "S": "Stoch", "W": "WaveTrend"}
FILTERS = ("VOL", "VTY", "TREND", "CONF")
FILTER_NAME = {"VOL": "hacim şoku", "VTY": "volatilite şoku", "TREND": "EMA200 trend", "CONF": "onay mumu"}
SUBSETS = [tuple(s) for k in (1, 2, 3) for s in itertools.combinations(OSC, k)]
FSETS = [tuple(s) for k in range(0, len(FILTERS) + 1) for s in itertools.combinations(FILTERS, k)]


# ─────────────── yardımcılar
def _a(x) -> np.ndarray:
    return np.asarray(x, dtype=float)


def rollmax(b: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(np.asarray(b).astype(np.int8)).rolling(n, min_periods=1).max().to_numpy().astype(bool)


def cooldown(e: np.ndarray, n: int) -> np.ndarray:
    """Aynı yönde önceki n bar içinde olay varsa yenisini yok say (kümenin yalnızca ilki)."""
    if n <= 1:
        return e
    prev = pd.Series(e.astype(np.int8)).shift(1).rolling(n, min_periods=1).max().fillna(0).to_numpy().astype(bool)
    return e & ~prev


def _prev(x):
    return np.r_[np.nan, x[:-1]]


def cross_up(x: np.ndarray, thr) -> np.ndarray:
    """x, thr'yi aşağıdan yukarı keser."""
    pt = thr if np.isscalar(thr) else _prev(thr)
    with np.errstate(invalid="ignore"):
        return (_prev(x) <= pt) & (x > thr)


def cross_dn(x: np.ndarray, thr) -> np.ndarray:
    """x, thr'yi yukarıdan aşağı keser."""
    pt = thr if np.isscalar(thr) else _prev(thr)
    with np.errstate(invalid="ignore"):
        return (_prev(x) >= pt) & (x < thr)


def _bands(x: pd.Series):
    up = x.rolling(C.DYN_LEN, min_periods=C.DYN_LEN // 2).quantile(C.DYN_PUP / 100).shift(1).clip(*C.DYN_UP_CLIP)
    dn = x.rolling(C.DYN_LEN, min_periods=C.DYN_LEN // 2).quantile(C.DYN_PDN / 100).shift(1).clip(*C.DYN_DN_CLIP)
    return up, dn


class Book:
    """Olay deposu: ad → (aile, long maskesi, short maskesi)."""

    def __init__(self):
        self.items: dict[str, tuple[str, np.ndarray, np.ndarray]] = {}

    def add(self, family: str, name: str, L: np.ndarray, S: np.ndarray, cool: int):
        L = np.nan_to_num(L.astype(float)).astype(bool)
        S = np.nan_to_num(S.astype(float)).astype(bool)
        self.items[f"{family} · {name}"] = (family, cooldown(L, cool), cooldown(S, cool))


# ─────────────── aileler
def fam_osc(book: Book, f: dict):
    c, o = _a(f["c"]), _a(f["o"])
    prev_c = np.r_[np.nan, c[:-1]]
    ev, zones = {}, {}
    for mode in ("sabit", "dinamik"):
        tob, tos, xob, xos = {}, {}, {}, {}
        for k in OSC:
            x = f[k]
            if mode == "sabit":
                up = pd.Series(C.STATIC_UP, index=x.index)
                dn = pd.Series(C.STATIC_DN, index=x.index)
            else:
                up, dn = _bands(x)
            ob = (x > up).to_numpy() & up.notna().to_numpy()
            os_ = (x < dn).to_numpy() & dn.notna().to_numpy()
            tob[k], tos[k] = rollmax(ob, C.ARM_BARS), rollmax(os_, C.ARM_BARS)
            xob[k], xos[k] = np.r_[False, ob[:-1] & ~ob[1:]], np.r_[False, os_[:-1] & ~os_[1:]]
        for s in SUBSETS:
            S_ = np.logical_and.reduce([tob[k] for k in s]) & np.logical_or.reduce([xob[k] for k in s])
            L_ = np.logical_and.reduce([tos[k] for k in s]) & np.logical_or.reduce([xos[k] for k in s])
            ev[(s, mode)] = (L_, S_)
    volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, C.ARM_BARS) if f["has_vol"] else np.ones(len(c), bool)
    vtyS = rollmax(_a(f["vtyZ"]) >= C.SHOCK_Z, C.ARM_BARS)
    ema = _a(f["ema200"])
    fl = {"VOL": volS, "VTY": vtyS, "TREND": c > ema, "CONF": (c > o) & (c > prev_c)}
    fs = {"VOL": volS, "VTY": vtyS, "TREND": c < ema, "CONF": (c < o) & (c < prev_c)}
    for (s, mode), (L, S) in ev.items():
        for fset in FSETS:
            l2, s2 = L.copy(), S.copy()
            for k in fset:
                l2 &= fl[k]
                s2 &= fs[k]
            flt = "+".join(FILTER_NAME[k] for k in fset) if fset else "filtresiz"
            book.add("OSC", f"{'+'.join(OSC_NAME[k] for k in s)} · {mode} · {flt}", l2, s2, C.ARM_BARS)
    f["_osc_ev"] = ev
    f["_vtyS"] = vtyS


def fam_regime(book: Book, f: dict):
    ev = f["_osc_ev"]
    c, ema, er = _a(f["c"]), _a(f["ema200"]), _a(f["er"])
    lo, hi = _a(f["er_lo"]), _a(f["er_hi"])
    with np.errstate(invalid="ignore"):
        rng = er < lo
        tup = (er > hi) & (c > ema)
        tdn = (er > hi) & (c < ema)
    for s in (("R",), ("S",), ("W",), ("R", "S", "W")):
        L, S = ev[(s, "dinamik")]
        nm = "+".join(OSC_NAME[k] for k in s)
        for flt, m in (("filtresiz", np.ones(len(c), bool)), ("volatilite şoku", f["_vtyS"])):
            book.add("REJIM", f"yatayda dönüş · {nm} · {flt}", L & rng & m, S & rng & m, C.ARM_BARS)
            book.add("REJIM", f"trendde geri çekilme · {nm} · {flt}", L & tup & m, S & tdn & m, C.ARM_BARS)
            book.add("REJIM", f"anahtar (ikisi) · {nm} · {flt}", (L & (rng | tup)) & m, (S & (rng | tdn)) & m, C.ARM_BARS)


def fam_rsi2(book: Book, f: dict):
    r2, c, ema = _a(f["rsi2"]), _a(f["c"]), _a(f["ema200"])
    for lo in C.RSI2_LO:
        L, S = cross_dn(r2, float(lo)), cross_up(r2, float(100 - lo))
        book.add("RSI2", f"RSI(2) {lo}/{100 - lo} · filtresiz", L, S, C.ARM_BARS)
        book.add("RSI2", f"RSI(2) {lo}/{100 - lo} · EMA200 trend", L & (c > ema), S & (c < ema), C.ARM_BARS)


def fam_donchian(book: Book, f: dict):
    h, l, c, ema = f["h"], f["l"], _a(f["c"]), _a(f["ema200"])
    volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, 2) if f["has_vol"] else np.ones(len(c), bool)
    sqz = rollmax(_a(f["bbw_pct"].shift(1)) < 0.2, 10)
    for n in C.DONCHIAN:
        hh, ll = _a(h.rolling(n).max().shift(1)), _a(l.rolling(n).min().shift(1))
        with np.errstate(invalid="ignore"):
            L, S = c > hh, c < ll
        L = L & ~np.r_[False, L[:-1]]
        S = S & ~np.r_[False, S[:-1]]
        for nm, ml, ms in (("filtresiz", 1, 1), ("hacim şoku", volS, volS), ("EMA200 trend", c > ema, c < ema), ("sıkışma sonrası", sqz, sqz)):
            book.add("DONCH", f"Donchian {n} · {nm}", L & ml, S & ms, 12)


def fam_ma(book: Book, f: dict):
    c = f["c"]
    for a, b in C.MA_PAIRS:
        d = _a(c.ewm(span=a, adjust=False).mean() - c.ewm(span=b, adjust=False).mean())
        book.add("MA", f"EMA {a}/{b} kesişimi", cross_up(d, 0.0), cross_dn(d, 0.0), 1)
    for n in C.TSMOM:
        r = _a(np.log(c / c.shift(n)))
        book.add("MA", f"zaman serisi momentumu {n} bar", cross_up(r, 0.0), cross_dn(r, 0.0), 12)


def fam_squeeze(book: Book, f: dict):
    on = ((f["bb_up"] < f["kc_up"]) & (f["bb_dn"] > f["kc_dn"])).to_numpy()
    run = pd.Series(on.astype(int)).groupby((~on).cumsum()).cumsum().to_numpy()
    release = np.r_[False, (run[:-1] >= C.SQZ_MIN) & ~on[1:]]
    c, mid = _a(f["c"]), _a(f["bb_mid"])
    volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, 3) if f["has_vol"] else np.ones(len(c), bool)
    L, S = release & (c > mid), release & (c < mid)
    book.add("SQZ", "BB-Keltner sıkışma çözülmesi · filtresiz", L, S, 12)
    book.add("SQZ", "BB-Keltner sıkışma çözülmesi · hacim şoku", L & volS, S & volS, 12)


def fam_vwap(book: Book, f: dict, df: pd.DataFrame, tf_min: int):
    if tf_min > 60:
        return
    from .features import session_vwap
    vw = session_vwap(df)
    dev = f["c"] - vw
    z = _a(dev / dev.rolling(100, min_periods=50).std().shift(1))
    er, lo = _a(f["er"]), _a(f["er_lo"])
    with np.errstate(invalid="ignore"):
        rng = er < lo
    for k in C.VWAP_K:
        L, S = cross_up(z, -k), cross_dn(z, k)
        book.add("VWAP", f"sapma dönüşü ±{k}σ · filtresiz", L, S, C.ARM_BARS)
        book.add("VWAP", f"sapma dönüşü ±{k}σ · yatay rejim", L & rng, S & rng, C.ARM_BARS)
    c, v = _a(f["c"]), _a(vw)
    volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, 2) if f["has_vol"] else np.ones(len(c), bool)
    book.add("VWAP", "VWAP kırılımı · hacim şoku", cross_up(c - v, 0.0) & volS, cross_dn(c - v, 0.0) & volS, 12)


def fam_orb(book: Book, f: dict, df: pd.DataFrame, tf_min: int):
    if tf_min > 30:
        return
    c = _a(f["c"])
    volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, 2) if f["has_vol"] else np.ones(len(c), bool)
    for sess, tz, open_min in (("New York", "America/New_York", 9 * 60 + 30), ("Londra", "Europe/London", 8 * 60)):
        loc = df.index.tz_convert(tz)
        mod = np.asarray(loc.hour * 60 + loc.minute)
        day = np.asarray(loc.normalize().asi8)
        wkday = np.asarray(loc.weekday) < 5
        for M in C.ORB_MIN:
            if M < tf_min or M % tf_min:
                continue
            inr = (mod >= open_min) & (mod < open_min + M) & wkday
            win = (mod >= open_min + M) & (mod < open_min + M + C.ORB_WINDOW_MIN) & wkday
            s_day = pd.Series(day)
            orh = s_day.map(pd.Series(_a(f["h"])[inr]).groupby(day[inr]).max()).to_numpy()
            orl = s_day.map(pd.Series(_a(f["l"])[inr]).groupby(day[inr]).min()).to_numpy()
            with np.errstate(invalid="ignore"):
                bl, bs = win & (c > orh), win & (c < orl)
            first_l = bl & (pd.Series(bl.astype(int)).groupby(day).cumsum().to_numpy() == 1)
            first_s = bs & (pd.Series(bs.astype(int)).groupby(day).cumsum().to_numpy() == 1)
            book.add("ORB", f"{sess} açılış {M}dk · filtresiz", first_l, first_s, 1)
            book.add("ORB", f"{sess} açılış {M}dk · hacim şoku", first_l & volS, first_s & volS, 1)


def fam_imom(book: Book, f: dict, df: pd.DataFrame, tf_min: int):
    if tf_min > 30:
        return
    loc = df.index.tz_convert("America/New_York")
    end = np.asarray((loc + pd.Timedelta(minutes=tf_min)).hour * 60 + (loc + pd.Timedelta(minutes=tf_min)).minute)
    wk = np.asarray(loc.weekday) < 5
    c = f["c"].to_numpy()
    c16 = pd.Series(np.where(end == 16 * 60, c, np.nan)).ffill().to_numpy()
    c10 = pd.Series(np.where(end == 10 * 60, c, np.nan)).ffill().to_numpy()
    ev = (end == 15 * 60 + 30) & wk
    r = c10 - c16
    with np.errstate(invalid="ignore"):
        book.add("IMOM", "sabah getirisi → 15:30 NY yönü", ev & (r > 0), ev & (r < 0), 1)


def fam_season(book: Book, f: dict, df: pd.DataFrame, tf_min: int, is_mask: np.ndarray):
    if tf_min > 60:
        return
    c, a = f["c"], f["atr"]
    fwd = _a((c.shift(-C.SEASON_FWD) - c) / a)
    hr = np.asarray(df.index.hour)
    first = np.asarray(df.index.minute) == 0
    m = is_mask & first & np.isfinite(fwd)
    L, S = np.zeros(len(c), bool), np.zeros(len(c), bool)
    learned = []
    for h_ in range(24):
        x = fwd[m & (hr == h_)]
        if len(x) < 60:
            continue
        t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
        if t > C.SEASON_T:
            L |= first & (hr == h_)
            learned.append(f"{h_:02d}↑")
        elif t < -C.SEASON_T:
            S |= first & (hr == h_)
            learned.append(f"{h_:02d}↓")
    if learned:
        book.add("SEZON", f"saat etkisi UTC {' '.join(learned)}", L, S, 1)


def fam_pair(book: Book, f: dict, partner: pd.Series | None, pname: str):
    if partner is None:
        return
    c = f["c"]
    p = partner.reindex(c.index, method="ffill", limit=3)
    lr = np.log(c) - np.log(p)
    z = _a((lr - lr.rolling(C.GSR_LEN, min_periods=C.GSR_LEN // 2).mean()) / lr.rolling(C.GSR_LEN, min_periods=C.GSR_LEN // 2).std())
    for t in C.GSR_Z:
        book.add("PAIR", f"{pname}'e göre göreli değer dönüşü ±{t}σ", cross_up(z, -t), cross_dn(z, t), C.ARM_BARS)
    pr = np.log(p).diff()
    pz = _a(pr / pr.rolling(100, min_periods=50).std().shift(1))
    oz = _a(f["ret_z"])
    with np.errstate(invalid="ignore"):
        L = (pz > C.LEADLAG_Z) & (oz < 1.0)
        S = (pz < -C.LEADLAG_Z) & (oz > -1.0)
    book.add("LEADLAG", f"{pname} ani hareketini takip", L, S, C.ARM_BARS)


def fam_funding(book: Book, f: dict, funding: pd.Series | None):
    if funding is None or funding.empty:
        return
    z = (funding - funding.rolling(C.FUNDING_LEN, min_periods=30).mean()) / funding.rolling(C.FUNDING_LEN, min_periods=30).std()
    zz = _a(z.reindex(f["c"].index, method="ffill"))
    for t in C.FUNDING_Z:
        # kalabalık LONG (yüksek funding) → SHORT; kalabalık SHORT → LONG
        book.add("FUNDING", f"fonlama uç değeri ±{t}σ (kalabalığa karşı)", cross_dn(zz, -t), cross_up(zz, t), 12)


def fam_macdyon(book: Book, f: dict):
    """Kullanıcının MACD yön stratejisi ve kombinasyonları (yön = yavaş MACD > sinyal)."""
    c, h, l = f["c"], f["h"], f["l"]
    for key, lab in (("macd_dir", "bar"), ("macd_dir_1s", "1s eşdeğeri")):
        d = f[key]
        up, dn = _a(d) > 0, _a(d) < 0
        pu, pd_ = np.r_[False, up[:-1]], np.r_[False, dn[:-1]]
        book.add("MACDYON", f"yön dönüşü ({lab})", up & ~pu, dn & ~pd_, 1)
        fm = FT.ema(c, 12) - FT.ema(c, 26)
        fs = FT.ema(fm, 9)
        xu, xd = cross_up(_a(fm - fs), 0.0), cross_dn(_a(fm - fs), 0.0)
        book.add("MACDYON", f"yön + hızlı MACD(12,26,9) kesişimi ({lab})", up & xu, dn & xd, 3)
        hist = _a(fm - fs)
        hp, hpp = _prev(hist), _prev(_prev(hist))
        with np.errstate(invalid="ignore"):
            book.add("MACDYON", f"yön + histogram dönüşü ({lab})", up & (hist < 0) & (hist > hp) & (hp <= hpp),
                     dn & (hist > 0) & (hist < hp) & (hp >= hpp), 3)
            e20 = _a(FT.ema(c, 20))
            book.add("MACDYON", f"yön + EMA20'ye geri çekilme ({lab})", up & (_a(l) <= e20) & (_a(c) > e20),
                     dn & (_a(h) >= e20) & (_a(c) < e20), 6)
            r2 = _a(f["rsi2"])
            book.add("MACDYON", f"yön + RSI(2) aşırı ({lab})", up & (r2 < 10), dn & (r2 > 90), 3)


def fam_filters(book: Book, f: dict, df: pd.DataFrame):
    """Mevcut girişlere tek tek filtre ekleyerek daha seçici yeni girişler üretir (aile adı korunur)."""
    c, o, h, l = _a(f["c"]), _a(f["o"]), _a(f["h"]), _a(f["l"])
    rng_ = np.where(h - l > 0, h - l, np.nan)
    with np.errstate(invalid="ignore"):
        body = (c - o) / rng_
        htf = _a(f["htf"])
        adx_ok = _a(f["adx"]) >= C.ADX_MIN
        sqz = rollmax(_a(f["bbw_pct"].shift(1)) < 0.25, 10)
        hr = np.asarray(df.index.hour)
        sess = (hr >= C.SESSION_UTC[0]) & (hr < C.SESSION_UTC[1])
        volS = rollmax(_a(f["volZ"]) >= C.SHOCK_Z, 2) if f["has_vol"] else np.ones(len(c), bool)
    flt = {
        "günlük trend": (htf > 0, htf < 0),
        f"ADX≥{C.ADX_MIN}": (adx_ok, adx_ok),
        "önceden sıkışma": (sqz, sqz),
        "güçlü mum": (body >= C.BODY_MIN, body <= -C.BODY_MIN),
        "seans": (sess, sess),
        "hacim": (volS, volS),
        "MACD yön": (_a(f["macd_dir"]) > 0, _a(f["macd_dir"]) < 0),
        "MACD yön 1s": (_a(f["macd_dir_1s"]) > 0, _a(f["macd_dir_1s"]) < 0),
    }
    if C.FILTERS_ON:
        flt = {k: v for k, v in flt.items() if k in C.FILTERS_ON}
    base = [(k, v) for k, v in book.items.items() if v[0] in C.FILTER_BASE_FAMILIES]
    for name, (fam, L, S) in base:
        for fn, (fl, fs) in flt.items():
            if fn in name:
                continue
            book.items[f"{name} + {fn}"] = (fam, L & np.nan_to_num(fl).astype(bool), S & np.nan_to_num(fs).astype(bool))


def build_all(df: pd.DataFrame, f: dict, tf_min: int, is_mask: np.ndarray, partner: pd.Series | None, pname: str,
              funding: pd.Series | None, families: tuple | None = None) -> Book:
    """families: yalnızca bu aileleri üret (None = FOCUS_FAMILIES / tümü). META ayrıca meta.add_meta ile eklenir."""
    want = set(families) if families else (set(C.FOCUS_FAMILIES) if C.FOCUS_FAMILIES else None)

    def on(fam):
        return want is None or fam in want

    book = Book()
    if on("OSC") or on("REJIM") or on("META"):
        fam_osc(book, f)          # REJIM bu ailenin olaylarını kullanır
    if on("REJIM"):
        fam_regime(book, f)
    if on("RSI2"):
        fam_rsi2(book, f)
    if on("DONCH"):
        fam_donchian(book, f)
    if on("MA"):
        fam_ma(book, f)
    if on("SQZ"):
        fam_squeeze(book, f)
    if on("VWAP"):
        fam_vwap(book, f, df, tf_min)
    if on("ORB"):
        fam_orb(book, f, df, tf_min)
    if on("IMOM"):
        fam_imom(book, f, df, tf_min)
    if on("SEZON"):
        fam_season(book, f, df, tf_min, is_mask)
    if on("PAIR") or on("LEADLAG"):
        fam_pair(book, f, partner, pname)
    if on("FUNDING"):
        fam_funding(book, f, funding)
    if on("MACDYON"):
        fam_macdyon(book, f)
    fam_filters(book, f, df)
    if C.FILTERED_ONLY:
        book.items = {k: v for k, v in book.items.items() if v[0] not in C.FILTERED_ONLY or " + " in k}
    if want is not None:
        book.items = {k: v for k, v in book.items.items() if v[0] in want}
    return book
