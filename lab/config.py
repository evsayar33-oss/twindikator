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

# ───────────────────────── ÇIKIŞ YÖNTEMLERİ ─────────────────────────
# Tüm sonuçlar R cinsinden: 1R = ilk stop mesafesi (sl_atr × ATR). Maliyet düşülür.
#   sl_atr : ilk stop (ATR)
#   tp     : son hedef (R) — None ise hedef yok (iz süren / zaman çıkışı)
#   tp1    : ara hedef (R) — ulaşılınca stop GİRİŞE çekilir (break-even)
#   part   : tp1'de kapatılan oran (0 = kısmi yok, yalnızca stop girişe)
#   trail  : iz süren stop (ATR, en yüksek/düşük fiyattan); "be" ise yalnızca tp1 sonrası devreye girer
ATR_LEN = 14
HORIZON = 48                  # zaman bariyeri (bar)
ENTRY = "next_open"           # sinyal barı kapanışı → sonraki bar açılışında giriş
EXITS = {
    "SABIT_1R":      {"sl_atr": 1.0, "tp": 1.0},
    "SABIT_1.5R":    {"sl_atr": 1.0, "tp": 1.5},
    "SABIT_2R":      {"sl_atr": 1.0, "tp": 2.0},
    "SABIT_3R":      {"sl_atr": 1.0, "tp": 3.0},
    "TP1>BE_2R":     {"sl_atr": 1.0, "tp": 2.0, "tp1": 1.0, "part": 0.0},
    "TP1>BE_3R":     {"sl_atr": 1.0, "tp": 3.0, "tp1": 1.0, "part": 0.0},
    "%50@1R>BE_2R":  {"sl_atr": 1.0, "tp": 2.0, "tp1": 1.0, "part": 0.5},
    "%50@1R>BE_3R":  {"sl_atr": 1.0, "tp": 3.0, "tp1": 1.0, "part": 0.5},
    "%50@1R>BE_IZ":  {"sl_atr": 1.0, "tp": None, "tp1": 1.0, "part": 0.5, "trail": 2.0, "trail_mode": "be"},
    "GENIS_%50@1R>BE_3R": {"sl_atr": 1.5, "tp": 3.0, "tp1": 1.0, "part": 0.5},
    "IZ_SUREN_2.5ATR": {"sl_atr": 1.0, "tp": None, "trail": 2.5, "trail_mode": "always"},
}

# ───────────────────────── STRATEJİ PARAMETRELERİ ─────────────────────────
ER_LEN = 20                   # verimlilik oranı (rejim)
REGIME_LEN = 300              # rejim persentil penceresi
RANGE_PCT, TREND_PCT = 40, 60 # ER persentili: altı yatay, üstü trend
DONCHIAN = (20, 55)
MA_PAIRS = ((9, 21), (20, 50), (50, 200))
TSMOM = (24, 72)
BB_LEN, BB_K, KC_K, SQZ_MIN = 20, 2.0, 1.5, 6
VWAP_K = (2.0, 2.5)
ORB_MIN = (15, 30)
ORB_WINDOW_MIN = 120
SEASON_FWD, SEASON_T = 6, 2.5
GSR_LEN, GSR_Z = 300, (1.5, 2.0)
LEADLAG_Z = 2.0
FUNDING_LEN, FUNDING_Z = 90, (1.5, 2.0)
PARTNER = {"BTC": "ETH", "ETH": "BTC", "NQ": "SPX", "SPX": "NQ", "XAU": "XAG", "XAG": "XAU"}

# ───────────────────────── META-MODEL ─────────────────────────
META_ON = True
META_EXIT = "%50@1R>BE_2R"    # meta-modelin öğrendiği etiket bu çıkışla üretilir
META_FOLDS = 4                # IS içinde genişleyen pencere CV (katlama dışı tahmin)
META_KEEP = 0.35              # olasılığı en yüksek %35'lik aday dilimi işlenir

# ───────────────────────── İSTATİSTİK ─────────────────────────
IS_FRACTION = 0.70            # ilk %70 seçim (in-sample), son %30 doğrulama (out-of-sample)
MIN_TRADES_IS = 40
MIN_TRADES_OOS = 15
WILSON_Z = 1.96
N_BLOCKS = 4                  # kararlılık: OOS dahil tüm dönem 4 bloğa bölünür

OUT_DIR = os.getenv("ATVS_OUT", "reports")
DATA_DIR = os.getenv("ATVS_DATA", "data")
