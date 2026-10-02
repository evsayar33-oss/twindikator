"""Ücretsiz veri katmanı: Binance Vision (kripto), Dukascopy (metal/endeks CFD), yfinance (son çare).

Her varlık için iki taban seri tutulur: 5m (kısa geçmiş) ve 1h (uzun geçmiş).
Önbellek: data/<VARLIK>_<taban>.csv.gz — sonraki çalıştırmalar yalnızca eksik kısmı indirir.
"""
from __future__ import annotations

import io
import lzma
import os
import struct
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import requests

from . import config as C

COLS = ["open", "high", "low", "close", "volume"]
UA = {"User-Agent": "Mozilla/5.0 (atvs-lab research)"}
_session = requests.Session()
_session.headers.update(UA)


def _get(url: str, params: dict | None = None, tries: int = 4, timeout: int = 30) -> requests.Response | None:
    for k in range(tries):
        try:
            r = _session.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code in (404, 400):
                return r
            if r.status_code in (418, 429, 451, 403):
                time.sleep(2.0 * (k + 1))
                if r.status_code in (451, 403):
                    return r
        except requests.RequestException:
            time.sleep(1.5 * (k + 1))
    return None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _finish(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=COLS)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df[COLS].astype(float)
    df = df[(df["high"] >= df["low"]) & (df["close"] > 0)]
    return df


# ═════════════════════════ BINANCE ═════════════════════════
_BINANCE_HOSTS = ["https://data-api.binance.vision", "https://api.binance.com"]


def _binance_klines(symbol: str, interval: str, start: datetime, end: datetime) -> pd.DataFrame:
    step_ms = {"5m": 300_000, "1h": 3_600_000}[interval]
    for host in _BINANCE_HOSTS:
        rows, cur, ok = [], int(start.timestamp() * 1000), True
        end_ms = int(end.timestamp() * 1000)
        while cur < end_ms:
            r = _get(f"{host}/api/v3/klines", {"symbol": symbol, "interval": interval, "startTime": cur, "limit": 1000})
            if r is None or r.status_code != 200:
                ok = False
                break
            batch = r.json()
            if not batch:
                break
            rows.extend(batch)
            cur = batch[-1][0] + step_ms
            if len(batch) < 1000:
                break
        if ok and rows:
            a = np.array([[float(x) for x in b[:6]] for b in rows])
            idx = pd.to_datetime(a[:, 0].astype("int64"), unit="ms", utc=True)
            return _finish(pd.DataFrame(a[:, 1:6], index=idx, columns=COLS))
        print(f"    [binance] {host} başarısız, sonraki kaynak deneniyor")
    return _binance_monthly_zips(symbol, interval, start, end)


def _binance_monthly_zips(symbol: str, interval: str, start: datetime, end: datetime) -> pd.DataFrame:
    """data.binance.vision aylık/günlük zip arşivi (ABD IP'lerinden de erişilebilir)."""
    frames = []
    y, m = start.year, start.month
    months = []
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1

    def fetch(ym):
        yy, mm = ym
        url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{yy}-{mm:02d}.zip"
        r = _get(url)
        if r is None or r.status_code != 200:
            return None
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            raw = z.read(z.namelist()[0])
        df = pd.read_csv(io.BytesIO(raw), header=None, usecols=range(6))
        if not str(df.iloc[0, 0]).isdigit():
            df = df.iloc[1:]
        ts = df.iloc[:, 0].astype("int64")
        ts = np.where(ts > 10**14, ts // 1000, ts)  # 2025+ dosyaları mikro-saniye
        out = pd.DataFrame(df.iloc[:, 1:6].astype(float).values, index=pd.to_datetime(ts, unit="ms", utc=True), columns=COLS)
        return out

    with ThreadPoolExecutor(6) as ex:
        for f in ex.map(fetch, months):
            if f is not None:
                frames.append(f)
    # son (henüz arşivlenmemiş) ay: günlük zipler
    last = end.replace(day=1)
    d = last
    days = []
    while d.date() <= end.date():
        days.append(d)
        d += timedelta(days=1)

    def fetch_day(dd):
        url = f"https://data.binance.vision/data/spot/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{dd:%Y-%m-%d}.zip"
        r = _get(url, tries=2)
        if r is None or r.status_code != 200:
            return None
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            raw = z.read(z.namelist()[0])
        df = pd.read_csv(io.BytesIO(raw), header=None, usecols=range(6))
        ts = df.iloc[:, 0].astype("int64")
        ts = np.where(ts > 10**14, ts // 1000, ts)
        return pd.DataFrame(df.iloc[:, 1:6].astype(float).values, index=pd.to_datetime(ts, unit="ms", utc=True), columns=COLS)

    with ThreadPoolExecutor(6) as ex:
        for f in ex.map(fetch_day, days):
            if f is not None:
                frames.append(f)
    if not frames:
        return pd.DataFrame(columns=COLS)
    df = _finish(pd.concat(frames))
    return df[(df.index >= start) & (df.index <= end)]


# ═════════════════════════ DUKASCOPY ═════════════════════════
_DK = "https://datafeed.dukascopy.com/datafeed"


def _bi5_records(blob: bytes) -> np.ndarray | None:
    if not blob:
        return None
    try:
        raw = lzma.decompress(blob)
    except lzma.LZMAError:
        return None
    n = len(raw) // 24
    if n == 0:
        return None
    return np.array(struct.unpack(">" + "iiiiif" * n, raw[: n * 24]), dtype=float).reshape(n, 6)


def _dk_day_1m(symbol: str, day: datetime) -> np.ndarray | None:
    url = f"{_DK}/{symbol}/{day.year}/{day.month - 1:02d}/{day.day:02d}/BID_candles_min_1.bi5"
    r = _get(url, tries=3)
    if r is None or r.status_code != 200:
        return None
    rec = _bi5_records(r.content)
    if rec is None:
        return None
    rec[:, 0] = rec[:, 0] + day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    return rec


def _dk_month_1h(symbol: str, y: int, m: int) -> np.ndarray | None:
    url = f"{_DK}/{symbol}/{y}/{m - 1:02d}/BID_candles_hour_1.bi5"
    r = _get(url, tries=3)
    if r is None or r.status_code != 200:
        return None
    rec = _bi5_records(r.content)
    if rec is None:
        return None
    rec[:, 0] = rec[:, 0] + datetime(y, m, 1, tzinfo=timezone.utc).timestamp()
    return rec


def _dk_frame(rec: np.ndarray, price_range: tuple[float, float]) -> pd.DataFrame:
    """Dukascopy kaydı: [t, p1, p2, p3, p4, hacim]. Sütun sırası ve ölçek veriden otomatik doğrulanır."""
    p = rec[:, 1:5]
    hi, lo = p.max(axis=1), p.min(axis=1)
    # kapanış hangi sütun? sonraki barın açılışına (sütun 0) en iyi uyan aday
    best, best_err = 1, np.inf
    for k in (1, 2, 3):
        err = np.nanmedian(np.abs(p[:-1, k] - p[1:, 0]) / np.maximum(hi[:-1] - lo[:-1], 1e-9))
        if err < best_err:
            best, best_err = k, err
    o, c = p[:, 0], p[:, best]
    # ölçek: medyan fiyat makul aralığa düşene kadar 10'un kuvvetleri
    med = np.nanmedian(c)
    lo_r, hi_r = price_range
    scale = 1.0
    for e in range(0, 8):
        if lo_r <= med / 10**e <= hi_r:
            scale = 10**e
            break
    idx = pd.to_datetime(rec[:, 0].astype("int64"), unit="s", utc=True)
    df = pd.DataFrame({"open": o / scale, "high": hi / scale, "low": lo / scale, "close": c / scale, "volume": rec[:, 5]}, index=idx)
    return _finish(df)


def _dukascopy(symbol: str, base: str, start: datetime, end: datetime, price_range) -> pd.DataFrame:
    recs = []
    if base == "1h":
        months = []
        y, m = start.year, start.month
        while (y, m) <= (end.year, end.month):
            months.append((y, m))
            m += 1
            if m == 13:
                y, m = y + 1, 1
        # içinde bulunulan ay için saatlik dosya henüz yok → 1 dk günlükten tamamla
        cur = (end.year, end.month)
        with ThreadPoolExecutor(6) as ex:
            for r in ex.map(lambda ym: _dk_month_1h(symbol, *ym), [x for x in months if x != cur]):
                if r is not None:
                    recs.append(r)
        tail_start = datetime(end.year, end.month, 1, tzinfo=timezone.utc)
        tail = _dukascopy_days(symbol, max(tail_start, start), end)
        if tail is not None:
            recs.append(tail)
        if not recs:
            return pd.DataFrame(columns=COLS)
        df = _dk_frame(np.vstack(recs), price_range)
        return _resample(df, "1h")
    rec = _dukascopy_days(symbol, start, end)
    if rec is None:
        return pd.DataFrame(columns=COLS)
    return _resample(_dk_frame(rec, price_range), "5min")


def _dukascopy_days(symbol: str, start: datetime, end: datetime) -> np.ndarray | None:
    days, d = [], start.replace(hour=0, minute=0, second=0, microsecond=0)
    while d <= end:
        if d.weekday() != 5:  # cumartesi kapalı
            days.append(d)
        d += timedelta(days=1)
    out = []
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(lambda dd: _dk_day_1m(symbol, dd), days):
            if r is not None:
                out.append(r)
    return np.vstack(out) if out else None


# ═════════════════════════ YFINANCE (son çare) ═════════════════════════
def _yfinance(ticker: str, base: str) -> pd.DataFrame:
    try:
        import yfinance as yf
    except ImportError:
        return pd.DataFrame(columns=COLS)
    period, interval = ("59d", "5m") if base == "5m" else ("729d", "1h")
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
    except Exception:
        return pd.DataFrame(columns=COLS)
    if df is None or df.empty:
        return pd.DataFrame(columns=COLS)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)[COLS]
    df.index = pd.to_datetime(df.index, utc=True)
    return _finish(df)


# ═════════════════════════ ORTAK ═════════════════════════
def _resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    if df.empty:
        return df
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    out = df.resample(rule, label="left", closed="left").agg(agg)
    return out.dropna(subset=["open", "close"])


def resample(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    return _resample(df, rule)


def _fetch(asset: str, base: str, start: datetime, end: datetime) -> pd.DataFrame:
    a = C.ASSETS[asset]
    df = pd.DataFrame(columns=COLS)
    if a["source"] == "binance":
        df = _binance_klines(a["symbol"], base, start, end)
    elif a["source"] == "dukascopy":
        df = _dukascopy(a["symbol"], base, start, end, a["price_range"])
    return df


def load(asset: str, base: str, refresh: bool = True) -> tuple[pd.DataFrame, str]:
    """Önbellekli yükleme. Dönen: (veri, kaynak açıklaması)."""
    os.makedirs(C.DATA_DIR, exist_ok=True)
    path = os.path.join(C.DATA_DIR, f"{asset}_{base}.csv.gz")
    years = C.YEARS_INTRADAY if base == "5m" else C.YEARS_HOURLY
    end = _now()
    start = end - timedelta(days=int(365.25 * years))
    cached = pd.DataFrame(columns=COLS)
    if os.path.exists(path):
        cached = pd.read_csv(path, index_col=0, parse_dates=True)
        cached.index = pd.to_datetime(cached.index, utc=True)
    src = C.ASSETS[asset]["source"]
    if refresh:
        fetch_from = start if cached.empty or cached.index[0] > start + timedelta(days=7) else cached.index[-1] - timedelta(days=2)
        new = _fetch(asset, base, fetch_from, end)
        df = _finish(pd.concat([cached, new])) if not new.empty else cached
    else:
        df = cached
    if df.empty or len(df) < 2000:
        yf_df = _yfinance(C.ASSETS[asset]["yf"], base)
        if len(yf_df) > len(df):
            df, src = yf_df, f"yfinance:{C.ASSETS[asset]['yf']} (yedek, kısa geçmiş)"
    df = df[df.index >= start]
    if not df.empty:
        df.to_csv(path, compression="gzip")
    return df, src


# ═════════════════════════ FONLAMA ORANI (kripto, ücretsiz) ═════════════════════════
def load_funding(asset: str, refresh: bool = True) -> pd.Series | None:
    """Binance USDⓈ-M fonlama oranı geçmişi. Önce data.binance.vision arşivi, sonra fapi."""
    a = C.ASSETS[asset]
    if a["source"] != "binance":
        return None
    os.makedirs(C.DATA_DIR, exist_ok=True)
    path = os.path.join(C.DATA_DIR, f"{asset}_funding.csv.gz")
    if not refresh and os.path.exists(path):
        s = pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]
        s.index = pd.to_datetime(s.index, utc=True)
        return s
    sym, end = a["symbol"], _now()
    start = end - timedelta(days=int(365.25 * max(C.YEARS_HOURLY, C.YEARS_INTRADAY)))
    months, y, m = [], start.year, start.month
    while (y, m) <= (end.year, end.month):
        months.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1

    def fetch(ym):
        yy, mm = ym
        r = _get(f"https://data.binance.vision/data/futures/um/monthly/fundingRate/{sym}/{sym}-fundingRate-{yy}-{mm:02d}.zip", tries=2)
        if r is None or r.status_code != 200:
            return None
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            d = pd.read_csv(io.BytesIO(z.read(z.namelist()[0])))
        tcol = [c for c in d.columns if "time" in c.lower()][0]
        rcol = [c for c in d.columns if "rate" in c.lower()][-1]
        ts = d[tcol].astype("int64")
        ts = np.where(ts > 10**14, ts // 1000, ts)
        return pd.Series(d[rcol].astype(float).values, index=pd.to_datetime(ts, unit="ms", utc=True))

    parts = []
    with ThreadPoolExecutor(6) as ex:
        for s in ex.map(fetch, months):
            if s is not None:
                parts.append(s)
    # son ay(lar) ve arşiv yoksa: fapi (ABD IP'lerinde engelli olabilir)
    last = max((p.index[-1] for p in parts), default=start)
    cur = int(last.timestamp() * 1000) + 1
    for _ in range(200):
        r = _get("https://fapi.binance.com/fapi/v1/fundingRate", {"symbol": sym, "startTime": cur, "limit": 1000}, tries=2)
        if r is None or r.status_code != 200:
            break
        js = r.json()
        if not js:
            break
        parts.append(pd.Series([float(x["fundingRate"]) for x in js], index=pd.to_datetime([x["fundingTime"] for x in js], unit="ms", utc=True)))
        cur = js[-1]["fundingTime"] + 1
        if len(js) < 1000:
            break
    if not parts:
        return None
    s = pd.concat(parts).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    s.rename("funding").to_csv(path, compression="gzip")
    return s
