"""ATVS Lab — merkezi yapılandırma. Tüm parametreler burada; kod içinde sihirli sayı yok."""
from __future__ import annotations
import os

# ───────────────────────── VARLIKLAR ─────────────────────────
# source: "binance" (BTC/ETH) | "dukascopy" (CFD: metal + endeks, 23 saat veri)
# price_range: Dukascopy fiyat ölçeği otomatik doğrulama için makul aralık
# cost_bps: gidiş-dönüş toplam maliyet (spread + komisyon), baz puan
ASSETS = {
    "XAU": {"source": "dukascopy", "symbol": "XAUUSD",        "yf": "GC=F",    "price_range": (800, 9000),   "cost_bps": 2.0},
    "XAG": {"source": "dukascopy", "symbol": "XAGUSD",        "yf": "SI=F",    "price_range": (8, 150),       "cost_bps": 5.0},
    "BTC": {"source": "binance",   "symbol": "BTCUSDT",       "yf": "BTC-USD", "price_range": (2000, 10**6),  "cost_bps": 8.0},
    "ETH": {"source": "binance",   "symbol": "ETHUSDT",       "yf": "ETH-USD", "price_range": (60, 50000),    "cost_bps": 8.0},
    "NQ":  {"source": "dukascopy", "symbol": "USATECHIDXUSD", "yf": "NQ=F",    "price_range": (3000, 45000), "cost_bps": 2.0},
    "SPX": {"source": "dukascopy", "symbol": "USA500IDXUSD",  "yf": "ES=F",    "price_range": (1200, 12000),  "cost_bps": 2.0},
}

# ───────────────────────── ZAMAN DİLİMLERİ ─────────────────────────
# base: hangi taban veriden yeniden örnekleneceği ("5m" kısa geçmiş, "1h" uzun geçmiş)
TIMEFRAMES = {
    "5m":  {"base": "5m", "rule": "5min"},
    "15m": {"base": "5m", "rule": "15min"},
    "30m": {"base": "5m", "rule": "30min"},
    "1h":  {"base": "1h", "rule": "1h"},
    "4h":  {"base": "1h", "rule": "4h"},
    "1d":  {"base": "1h", "rule": "1D"},
}
YEARS_INTRADAY = float(os.getenv("ATVS_YEARS_INTRADAY", "2"))   # 5m tabanı geçmişi
YEARS_HOURLY   = float(os.getenv("ATVS_YEARS_HOURLY", "15"))     # kaynakta ne kadar varsa (BTC/ETH ~2017'den)
CACHE_TAG = "v4"              # önbellek sürümü: değişince tüm veri temiz baştan indirilir (v4: eksik-parça yeniden deneme ile temiz indirme)
VALIDATE_TOL = 0.06           # bağımsız kaynakla aylık oran sapma toleransı (CFD/futures baz farkı dahil)

# ODAK MODU: kısa ZD'ler maliyetten dolayı elendi → yalnızca bu ZD ve aileler test edilir
# (daha az test = daha güçlü istatistik; boş bırakılırsa hepsi)
FOCUS_TFS = tuple(x for x in os.getenv("ATVS_TFS", "1h,4h").split(",") if x)
FOCUS_FAMILIES = tuple(x for x in os.getenv("ATVS_FAMILIES", "MA,DONCH,SQZ,RSI2,REJIM,OSC,META").split(",") if x)
SUSPECT_EXP, SUSPECT_WR = 1.5, 0.85   # bunları aşan sonuçlar 'veri şüphesi' sayılır ve seçimden çıkarılır

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
    # v3.1 — daha yüksek RR / farklı BE noktaları / başarısız kırılımda erken çıkış
    "SABIT_2.5R":    {"sl_atr": 1.0, "tp": 2.5},
    "SABIT_4R":      {"sl_atr": 1.0, "tp": 4.0},
    "TP0.5>BE_3R":   {"sl_atr": 1.0, "tp": 3.0, "tp1": 0.5, "part": 0.0},
    "TP1.5>BE_4R":   {"sl_atr": 1.0, "tp": 4.0, "tp1": 1.5, "part": 0.0},
    "%50@1R>BE_4R":  {"sl_atr": 1.0, "tp": 4.0, "tp1": 1.0, "part": 0.5},
    "TP1>BE_3R_ERKEN": {"sl_atr": 1.0, "tp": 3.0, "tp1": 1.0, "part": 0.0, "fail": 3},
}

# ───────────────────────── STRATEJİ PARAMETRELERİ ─────────────────────────
ER_LEN = 20                   # verimlilik oranı (rejim)
REGIME_LEN = 300              # rejim persentil penceresi
RANGE_PCT, TREND_PCT = 40, 60 # ER persentili: altı yatay, üstü trend
DONCHIAN = (20, 55)
RSI2_LO = (5, 10)             # RSI(2) alt eşikleri (üst = 100 − alt)
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

# v3.1 — giriş filtresi katmanı: aşağıdaki ailelerin her girişine filtreler TEK TEK eklenerek yeni girişler üretilir
FILTER_BASE_FAMILIES = ("DONCH", "MA", "SQZ", "RSI2", "REJIM")
HTF_EMA = 50                  # günlük grafik trend EMA'sı (bir önceki tamamlanmış gün)
ADX_MIN = 20                  # trend gücü filtresi
SESSION_UTC = (7, 20)         # Londra + New York seansı (UTC saat, bar başlangıcı)
BODY_MIN = 0.5                # güçlü mum: gövde / aralık oranı

# ───────────────────────── META-MODEL ─────────────────────────
META_ON = True
META_EXIT = "%50@1R>BE_2R"    # meta-modelin öğrendiği etiket bu çıkışla üretilir
META_FOLDS = 4                # IS içinde genişleyen pencere CV (katlama dışı tahmin)
META_KEEP = 0.35              # olasılığı en yüksek %35'lik aday dilimi işlenir

# ───────────────────────── FİNALİST SEÇİMİ (v3) ─────────────────────────
# Adaylar: (a) aşağıdaki tohum listesi (v2.4 analizinden), (b) her varlık × ZD için IS'te en sağlam ilk K ayar.
# Her aday aşağıdaki KAPILARIN HEPSİNİ geçerse finalist olur. Tüm testler çakışmasız (strateji başına tek pozisyon).
FINAL_SEEDS = [
    {"asset": "XAU", "tf": "4h", "entry": "DONCH · Donchian 20 · EMA200 trend", "exit": "TP1>BE_3R", "scope": "long"},
    {"asset": "SPX", "tf": "4h", "entry": "RSI2 · RSI(2) 10/90 · EMA200 trend", "exit": "SABIT_3R", "scope": "long"},
    {"asset": "ETH", "tf": "4h", "entry": "DONCH · Donchian 20 · hacim şoku", "exit": "IZ_SUREN_2.5ATR", "scope": "both"},
    {"asset": "NQ", "tf": "1h", "entry": "META · gradient boosting · tüm adaylar · üst %35", "exit": "IZ_SUREN_2.5ATR", "scope": "long"},
    {"asset": "XAU", "tf": "1h", "entry": "SQZ · BB-Keltner sıkışma çözülmesi · filtresiz", "exit": "IZ_SUREN_2.5ATR", "scope": "both"},
    {"asset": "NQ", "tf": "1h", "entry": "REJIM · anahtar (ikisi) · Stoch · filtresiz", "exit": "IZ_SUREN_2.5ATR", "scope": "long"},
]
FINAL_TOPK = 6                # varlık × ZD başına IS t-istatistiğine göre ek aday
FINAL_MIN_T_IS = 2.0          # ek adaylar için IS t alt sınırı
GATE_OOS_N = 30               # OOS'ta en az işlem (çakışmasız)
GATE_OOS_P = 0.10             # K1: Benjamini–Hochberg yanlış keşif oranı (tüm adaylar birlikte)
GATE_FULL_N = 80              # tüm dönemde en az işlem (çakışmasız)
GATE_COST_MULT = 2.0          # maliyet bu katına çıkınca da beklenti > 0 olmalı
GATE_NEIGHBOR_POS = 0.70      # komşu parametre setlerinin en az bu oranı pozitif olmalı
GATE_YEARS_POS = 0.60         # (≥5 işlemli) yılların en az bu oranı pozitif olmalı
FINAL_PER_ASSET = 2           # varlık başına en fazla finalist
FINAL_MAX = 8                 # toplam en fazla finalist

# ───────────────────────── PORTFÖY (olay tabanlı, v3) ─────────────────────────
CLUSTERS = {"XAU": "METAL", "XAG": "METAL", "BTC": "KRIPTO", "ETH": "KRIPTO", "NQ": "ABD_ENDEKS", "SPX": "ABD_ENDEKS"}
PORT_MAX_OPEN = 4             # aynı anda en fazla açık pozisyon
PORT_CLUSTER_MAX = 1          # aynı kümede (birlikte hareket eden varlıklar) aynı anda en fazla pozisyon
PORT_RISKS = (0.0025, 0.005, 0.0075, 0.01, 0.015, 0.02)
PORT_DAILY_LIMIT = 0.03       # gün içinde gerçekleşen zarar bu orana ulaşınca o gün yeni işlem yok
PORT_TARGET_MDD = 0.15        # Monte Carlo'da %95 olasılıkla aşılmaması istenen maksimum düşüş
PORT_MC_PATHS = 3000

# ───────────────────────── CANLI KÂĞIT İŞLEM ─────────────────────────
LIVE_STATE_DIR = os.getenv("ATVS_STATE", "state")
LIVE_CATCHUP_BARS = 12        # kaçırılan çalıştırmalar için geriye dönük sinyal tarama (bar)
LIVE_DEFAULT_RISK = 0.005     # finalist raporu öneri üretemezse kullanılacak işlem başına risk
LIVE_BARS = 5000              # META dışı stratejilerde canlı hesap için son N mum (göstergelerin ısınması için fazlasıyla yeterli)

# ───────────────────────── İSTATİSTİK ─────────────────────────
IS_FRACTION = 0.70            # ilk %70 seçim (in-sample), son %30 doğrulama (out-of-sample)
MIN_TRADES_IS = 40
MIN_TRADES_OOS = 15
WILSON_Z = 1.96
N_BLOCKS = 4                  # kararlılık: OOS dahil tüm dönem 4 bloğa bölünür

OUT_DIR = os.getenv("ATVS_OUT", "reports")
DATA_DIR = os.getenv("ATVS_DATA", "data")

# ───────────────────────── BITGET GERÇEKÇİ MALİYET (v4) ─────────────────────────
# Laboratuvarın ilk maliyetleri CFD/spot spread'ine göreydi (XAU 2 bps). Bot Bitget USDT-M vadelide piyasa emriyle
# işlem yapar: taker ücreti her iki yönde + spread/kayma + fonlama (funding). v4 bütün kararları bu maliyetle verir.
BITGET_TAKER_BPS = float(os.getenv("ATVS_TAKER_BPS", "6"))        # tek yön taker (standart 0.06%)
BITGET_SPREAD_BPS = {"XAU": 2.0, "XAG": 4.0, "BTC": 1.0, "ETH": 1.0, "NQ": 3.0, "SPX": 3.0}
BITGET_FUNDING_BPS_DAY = float(os.getenv("ATVS_FUNDING_BPS_DAY", "3"))   # ≈ 0.01% / 8 saat (tipik); uzun tutulan işlemleri cezalandırır


def bitget_cost_bps(asset: str) -> float:
    """Gidiş-dönüş toplam: 2 × taker + spread/kayma (baz puan)."""
    return 2 * BITGET_TAKER_BPS + BITGET_SPREAD_BPS.get(asset, 3.0)


# ───────────────────────── ENDEKS MODÜLÜ (v4: NQ/QQQ · SPX/SPY) ─────────────────────────
# Bitget hisse/endeks vadelileri 7/24 fiyatlanır ama ABD piyasası kapalıyken YENİ POZİSYON AÇILAMAZ ve açılışta
# fiyat boşluğu olabilir. Bu yüzden endeks stratejileri ABD nakit seansına göre kurulur:
#   günlük mum = New York 09:00–15:00 arası saatlik mumlar · karar anı = 15:00 ET (seans içi, kapanıştan 1 saat önce)
#   giriş / sinyal çıkışı = 15:00 ET mumunun açılışı · stop borsada (gece/hafta sonu boşluğu doldurulur)
IDX_ASSETS = ("NQ", "SPX")
IDX_TZ = "America/New_York"
IDX_SESSION = (9, 14)                 # günlük mumu oluşturan saatlik mum başlangıçları (ET, dahil)
IDX_WARMUP = 210                      # gösterge ısınması (gün)
IDX_STOP_K = (1.5, 2.5, 3.5)          # felaket stopu: k × günlük ATR(14) — 1R
IDX_TMAX = (5, 10)                    # zaman stopu (işlem günü); trend ailesi için IDX_TMAX_TREND
IDX_TMAX_TREND = (60, 120)
IDX_IS_T_MIN = 2.0                    # IS t ≥ bu değer olan ayarlar OOS'a gider (çoklu testi azaltır)
IDX_POOL_PER_ASSET = 40
IDX_SUSPECT_WR = 0.92                 # ortalamaya dönüşte yüksek isabet normaldir; veri şüphesi eşiği daha yüksek
IDX_PICK_PER_ASSET = 3                # portföy testine giden en iyi aday (farklı aile)
IDX_RISK_GRID = (0.0, 0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02)   # strateji başına işlem riski seçenekleri (0 = kullanma)
IDX_TARGET_MDD = float(os.getenv("ATVS_TARGET_MDD", "0.15"))  # portföy: %95 olasılıkla aşılmaması istenen düşüş
IDX_SYMBOL = {"NQ": "QQQ/USDT:USDT", "SPX": "SPY/USDT:USDT"}


# v4.1 — maliyet modeli: "bitget" (varsayılan; gerçek bot ortamı) ya da "eski" (CFD spread'i, yalnızca karşılaştırma için)
COST_MODEL = os.getenv("ATVS_COST", "bitget")


def fund_bps_bar(tf_min: int) -> float:
    """Pozisyon açık kaldığı her mum için fonlama maliyeti (baz puan)."""
    return BITGET_FUNDING_BPS_DAY * tf_min / 1440.0 if COST_MODEL == "bitget" else 0.0


for _a, _v in ASSETS.items():
    _v["cost_bps_eski"] = _v["cost_bps"]
    if COST_MODEL == "bitget":
        _v["cost_bps"] = bitget_cost_bps(_a)

# ───────────────────────── MACD YÖN (kullanıcının stratejisi, v4.1) ─────────────────────────
# MACD çizgisi sinyal çizgisinin üstündeyse yön LONG, altındaysa SHORT. Tek başına giriş değil, YÖN filtresi.
MACD_DIR = (675, 875, 475)            # hızlı, yavaş, sinyal (EMA) — kullanıcının TradingView ayarı
MACD_DIR_BASE_MIN = 60                # bu ayarların kullanıldığı grafik (1 saat) → "1s eşdeğeri" modunda diğer ZD'lere ölçeklenir
_flt_env = os.getenv("ATVS_FILTERS", "")
FILTERS_ON = tuple(x.strip() for x in _flt_env.split(",") if x.strip())     # boş = hepsi
_ff_env = os.getenv("ATVS_FILTER_FAMILIES", "")
if _ff_env:
    FILTER_BASE_FAMILIES = tuple(x.strip() for x in _ff_env.split(",") if x.strip())
FILTERED_ONLY = tuple(x.strip() for x in os.getenv("ATVS_FILTERED_ONLY", "").split(",") if x.strip())  # bu ailelerin yalnızca filtreli girişleri
