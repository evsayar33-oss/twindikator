"""ATVS Lab — merkezi yapılandırma. Tüm parametreler burada; kod içinde sihirli sayı yok."""
from __future__ import annotations
import os

# ───────────────────────── VARLIKLAR ─────────────────────────
# source: "binance" (BTC/ETH) | "dukascopy" (CFD: metal + endeks, 23 saat veri)
# price_range: Dukascopy fiyat ölçeği otomatik doğrulama için makul aralık
# cost_bps: gidiş-dönüş toplam maliyet (spread + komisyon), baz puan
ASSETS = {
    "XAU": {"source": "dukascopy", "symbol": "XAUUSD",        "yf": "GC=F",    "price_range": (500, 20000),   "cost_bps": 2.0},
    "XAG": {"source": "dukascopy", "symbol": "XAGUSD",        "yf": "SI=F",    "price_range": (5, 500),       "cost_bps": 5.0},
    "BTC": {"source": "binance",   "symbol": "BTCUSDT",       "yf": "BTC-USD", "price_range": (1000, 10**7),  "cost_bps": 8.0},
    "ETH": {"source": "binance",   "symbol": "ETHUSDT",       "yf": "ETH-USD", "price_range": (50, 10**6),    "cost_bps": 8.0},
    "NQ":  {"source": "dukascopy", "symbol": "USATECHIDXUSD", "yf": "NQ=F",    "price_range": (3000, 200000), "cost_bps": 2.0},
    "SPX": {"source": "dukascopy", "symbol": "USA500IDXUSD",  "yf": "ES=F",    "price_range": (1000, 50000),  "cost_bps": 2.0},
}

# ───────────────────────── ZAMAN DİLİMLERİ ─────────────────────────
# base: hangi taban veriden yeniden örnekleneceği ("5m" kısa geçmiş, "1h" uzun geçmiş)
TIMEFRAMES = {
    "5m":  {"base": "5m", "rule": "5min"},
    "15m": {"base": "5m", "rule": "15min"},
    "30m": {"base": "5m", "rule": "30min"},
    "1h":  {"base": "1h", "rule": "1h"},
    "4h":  {"base": "1h", "rule": "4h"},
}
YEARS_INTRADAY = float(os.getenv("ATVS_YEARS_INTRADAY", "2"))   # 5m tabanı geçmişi
YEARS_HOURLY   = float(os.getenv("ATVS_YEARS_HOURLY", "6"))     # 1h tabanı geçmişi

# ───────────────────────── GÖSTERGELER (Pine ile birebir) ─────────────────────────
RSI_LEN = 14
STOCH_LEN, STOCH_SMOOTH = 14, 3
WT_N1, WT_N2, WT_SCALE = 10, 21, 75.0

STATIC_UP, STATIC_DN = 80.0, 20.0                 # sabit eşik
DYN_LEN, DYN_PUP, DYN_PDN = 300, 90.0, 10.0       # dinamik eşik: kayan persentil
DYN_UP_CLIP, DYN_DN_CLIP = (65.0, 92.0), (8.0, 35.0)

ARM_BARS = 6            # eşik temasından sonra tetik penceresi ve şok geriye bakışı
SHOCK_LEN = 50          # robust z referans penceresi
SHOCK_Z = 1.5           # hacim / volatilite şok eşiği (σ, robust)
TREND_EMA = 200

# ───────────────────────── İŞLEM ETİKETLEME (üçlü bariyer) ─────────────────────────
ATR_LEN = 14
TP_ATR, SL_ATR = 1.5, 1.0     # başabaş isabet = SL/(TP+SL) = %40 (maliyet hariç)
HORIZON = 24                  # bar
ENTRY = "next_open"           # sinyal barı kapanışında alarm → sonraki bar açılışında giriş

# ───────────────────────── İSTATİSTİK ─────────────────────────
IS_FRACTION = 0.70            # ilk %70 seçim (in-sample), son %30 doğrulama (out-of-sample)
MIN_TRADES_IS = 50
MIN_TRADES_OOS = 20
WILSON_Z = 1.96
N_BLOCKS = 4                  # kararlılık: OOS dahil tüm dönem 4 bloğa bölünür

OUT_DIR = os.getenv("ATVS_OUT", "reports")
DATA_DIR = os.getenv("ATVS_DATA", "data")
