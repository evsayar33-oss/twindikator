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


def _get(url: str, params: dict | None = None, tries: int = 6, timeout: int = 30) -> requests.Response | None:
    """Kalıcı hata (404/400/403/451) hemen döner; diğer her hata (429, 5xx, ağ) üstel bekleme ile yeniden denenir."""
    for k in range(tries):
        try:
            r = _session.get(url, params=params, timeout=timeout)
            if r.status_code in (200, 404, 400, 403, 451):
                return r
        except requests.RequestException:
            pass
        time.sleep(min(30.0, 1.5 * 2 ** k))
    return None


def _fetch_complete(keys: list, fn, threads: int = 4, rounds: int = 4, label: str = "") -> dict:
    """Tüm parçaları indir; eksik kalanları (ağ hatası / kısıtlama / boş yanıt) azalan eşzamanlılıkla tekrar dene.
    Sessizce eksik veri = backtest'te sahte fiyat boşlukları → bu yüzden eksikler raporlanır."""
    out = {}
    todo = list(keys)
    for rnd in range(rounds):
        if not todo:
            break
        if rnd:
            time.sleep(5 * rnd)
        with ThreadPoolExecutor(max(1, threads // (rnd + 1))) as ex:
            for k_, r in zip(todo, ex.map(fn, todo)):
                if r is not None:
                    out[k_] = r
        todo = [k_ for k_ in todo if k_ not in out]
    if todo and label:
        print(f"    [eksik] {label}: {len(todo)}/{len(keys)} parça indirilemedi")
    MISSING[label] = (len(todo), len(keys))
    return out


MISSING: dict[str, tuple[int, int]] = {}


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
    r = _get(url, tries=4)
    if r is None or r.status_code not in (200, 404):
        return None                      # geçici hata → yeniden denenecek
    if r.status_code == 200 and len(r.content) > 0:
        rec = _bi5_records(r.content)
        if rec is None:
            return None                  # bozuk/yarım yanıt → yeniden dene
    else:
        rec = None
    if rec is None:
        return np.empty((0, 6))          # kesin boş (tatil / veri yok) → yeniden denenmez
    rec[:, 0] = rec[:, 0] + day.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    return rec


def _dk_month_1h(symbol: str, y: int, m: int) -> np.ndarray | None:
    url = f"{_DK}/{symbol}/{y}/{m - 1:02d}/BID_candles_hour_1.bi5"
    r = _get(url, tries=4)
    if r is None or r.status_code not in (200, 404):
        return None
    if r.status_code == 200 and len(r.content) > 0:
        rec = _bi5_records(r.content)
        if rec is None:
            return None                  # bozuk/yarım yanıt → yeniden dene
    else:
        rec = None
    if rec is None:
        return np.empty((0, 6))
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
    # ölçek: AY BLOKLARI halinde belirlenir. Önce makul aralık, birden çok aday varsa önceki bloğa süreklilik.
    lo_r, hi_r = price_range
    ts = rec[:, 0].astype("int64")
    month = (pd.to_datetime(ts, unit="s", utc=True).year * 12 + pd.to_datetime(ts, unit="s", utc=True).month).to_numpy()
    order = np.argsort(ts, kind="stable")
    scale = np.ones(len(c))
    prev = None
    for mth in np.unique(month[order]):
        m = month == mth
        med = np.nanmedian(c[m])
        if not np.isfinite(med) or med <= 0:
            continue
        cands = [10.0 ** e for e in range(0, 9) if lo_r <= med / 10.0 ** e <= hi_r]
        if not cands:
            cands = [10.0 ** e for e in range(0, 9)]
        if prev is not None:
            sc = min(cands, key=lambda k: abs(np.log(med / k) - np.log(prev)))
        else:
            sc = cands[0]
        scale[m] = sc
        prev = med / sc
    idx = pd.to_datetime(rec[:, 0].astype("int64"), unit="s", utc=True)
    df = pd.DataFrame({"open": o / scale, "high": hi / scale, "low": lo / scale, "close": c / scale, "volume": rec[:, 5]}, index=idx)
    df = df[(df["volume"] > 0) | (df["high"] > df["low"])]   # piyasa kapalı (işlemsiz, düz) dakikaları at
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
        got = _fetch_complete([x for x in months if x != cur], lambda ym: _dk_month_1h(symbol, *ym), threads=4, label=f"{symbol} 1h ay")
        recs.extend(got[k] for k in sorted(got) if len(got[k]))
        empty = sum(1 for k in got if not len(got[k]))
        if empty:
            print(f"    [bilgi] {symbol}: {empty} ay için kaynakta veri yok (enstrüman geçmişi daha kısa olabilir)")
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
    got = _fetch_complete(days, lambda dd: _dk_day_1m(symbol, dd), threads=6, label=f"{symbol} 1m gün")
    out = [got[k] for k in sorted(got) if len(got[k])]
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
    path = os.path.join(C.DATA_DIR, f"{C.CACHE_TAG}_{asset}_{base}.csv.gz")
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


# ═════════════════════════ VERİ DOĞRULAMA ═════════════════════════
_YF_DAILY: dict[str, pd.Series] = {}


def _yf_daily(ticker: str) -> pd.Series | None:
    if ticker in _YF_DAILY:
        return _YF_DAILY[ticker]
    try:
        import yfinance as yf
        d = yf.download(ticker, period="max", interval="1d", progress=False, auto_adjust=False)
        if isinstance(d.columns, pd.MultiIndex):
            d.columns = d.columns.get_level_values(0)
        s = d["Close"].dropna()
        s.index = pd.to_datetime(s.index).tz_localize(None).normalize()
    except Exception:
        s = None
    _YF_DAILY[ticker] = s
    return s


def validate(asset: str, base: str, df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Bağımsız kaynakla (yfinance günlük kapanış) ay ay karşılaştırma.
    • Oran 10'un kuvvetine yakınsa (ölçek hatası) → o ay düzeltilir
    • Oran %{tol} dışında ve düzeltilemiyorsa → o ay verisi ATILIR
    • Ayrıca: aşırı bar sıçramaları (medyan mutlak getirinin 25 katı ve > %4) sayılır ve atılır"""
    rep = {"asset": asset, "base": base, "rows_in": len(df), "fixed_months": 0, "dropped_months": 0,
           "spikes": 0, "ref": C.ASSETS[asset]["yf"], "status": "doğrulanamadı (yfinance yok)", "median_dev": np.nan}
    if df.empty:
        rep["status"] = "veri yok"
        return df, rep
    df = df.copy()
    # 1) sıçrama temizliği
    lr = np.log(df["close"]).diff().abs()
    med = lr.rolling(500, min_periods=50).median()
    spike = (lr > 25 * med) & (lr > 0.04)
    # yalnızca geri dönen (tek bar) sıçramalar: sonraki bar da büyük ters hareket yapıyorsa
    back = np.log(df["close"]).diff().shift(-1).abs() > 0.5 * lr
    bad = spike & back
    rep["spikes"] = int(bad.sum())
    df = df[~bad]
    # kapsama: beklenen aylar içinde bar sayısı medyanın %20'sinin altında olan (eksik) aylar
    cnt = df["close"].resample("ME").size()
    rep["gap_months"] = int((cnt < 0.2 * cnt.median()).sum()) if len(cnt) else 0
    rep["span"] = f"{df.index[0]:%Y-%m} → {df.index[-1]:%Y-%m}" if len(df) else "—"
    # 2) bağımsız referansla ay ay oran
    ref = _yf_daily(C.ASSETS[asset]["yf"])
    if ref is None or ref.empty:
        rep["rows_out"] = len(df)
        return df, rep
    dclose = df["close"].resample("1D").last().dropna()
    dclose.index = dclose.index.tz_localize(None).normalize()
    j = pd.concat([dclose.rename("x"), ref.rename("r")], axis=1, join="inner").dropna()
    if len(j) < 20:
        rep["status"] = "referansla örtüşme yok"
        rep["rows_out"] = len(df)
        return df, rep
    ratio = (j["x"] / j["r"]).groupby(j.index.to_period("M")).median()
    tol = C.VALIDATE_TOL
    pm = df.index.tz_localize(None).to_period("M")
    keep = np.ones(len(df), bool)
    for per, rt in ratio.items():
        if abs(np.log(rt)) <= np.log(1 + tol):
            continue
        k = round(np.log10(rt))
        m = (pm == per)
        if k != 0 and abs(np.log(rt / 10.0 ** k)) <= np.log(1 + tol):
            df.loc[m, ["open", "high", "low", "close"]] /= 10.0 ** k
            rep["fixed_months"] += 1
        else:
            keep &= ~np.asarray(m)
            rep["dropped_months"] += 1
    df = df[keep]
    after = ratio.where(np.abs(np.log(ratio)) <= np.log(1 + tol))
    rep["median_dev"] = float(np.nanmedian(np.abs(after - 1))) if after.notna().any() else np.nan
    rep["months"] = int(len(ratio))
    rep["rows_out"] = len(df)
    rep["status"] = "temiz" if rep["fixed_months"] == rep["dropped_months"] == rep["spikes"] == 0 else "düzeltildi"
    return df, rep


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
