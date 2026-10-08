"""ATVS Bitget emir motoru — finalist stratejileri gerçek (veya demo) hesapta çalıştırır.

Sunucuda (Oracle Cloud, Avrupa) cron ile her saat :10'da çalışır:
    python trader.py            # normal çalışma
    python trader.py --kontrol  # bağlantı / yetki / sembol / bakiye kontrolü (emir açmaz)

Sinyaller: laboratuvarla AYNI veri + gösterge + giriş kodu (live.build). Sinyal mumu kapandıktan sonra
en fazla 2 saat içinde piyasa emriyle girilir (backtest: sonraki mumun açılışı).
Koruma: giriş anında stop emri BORSAYA konur (sunucu kapansa bile pozisyon korunur), hedef varsa
reduce-only limit emir konur. Sonraki çalıştırmalarda kapanmış 4h mumlarına göre:
  • TP1'e ulaşıldıysa stop girişe çekilir (backtest gibi: bir sonraki mumdan itibaren)
  • iz süren stop güncellenir
  • zaman bariyerinde (48 mum) pozisyon kapatılır
  • stop/hedef borsada gerçekleştiyse kalan emirler iptal edilir
Pozisyon büyüklüğü: kasa × risk ÷ stop mesafesi.

Ortam değişkenleri (sunucuda ~/atvs.env):
  BITGET_KEY, BITGET_SECRET, BITGET_PASS   API bilgileri (yalnızca Futures order + Futures holdings yetkisi)
  BITGET_DEMO=1                            1 = demo (sahte para), 0 = gerçek hesap
  ATVS_RISK=0.02                           işlem başına kasa riski (v5.4)
  ATVS_ONLY=XAU                            yalnızca bu varlık(lar) (virgülle; boş = hepsi)
  ATVS_LEVERAGE=50                         kaldıraç ÜST SINIRI (otomatik seçilir; risk stop mesafesiyle belirlenir)
  SYM_XAU=XAU/USDT:USDT  SYM_ETH=ETH/USDT:USDT   borsa sembolleri (ccxt biçimi)
  ATVS_DRY=1                               emir göndermeden yalnızca loga yaz
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import traceback

import numpy as np
import pandas as pd

os.environ.setdefault("ATVS_YEARS_HOURLY", "4")      # canlı için 4 yıl yeterli (göstergelerin ısınması dahil)

import live as LV  # noqa: E402
from lab import config as C  # noqa: E402
from lab import index_lab as IL  # noqa: E402
from lab import kripto as KR  # noqa: E402
from lab import features as FT  # noqa: E402

STATE_FILE = os.path.join(C.LIVE_STATE_DIR, "trader_state.json")
TRADES_FILE = os.path.join(C.LIVE_STATE_DIR, "trader_trades.csv")
FIN_FILE = os.path.join(C.LIVE_STATE_DIR, "finalists.json")
TF_MIN = {"1h": 60, "4h": 240, "1d": 1440}
MAX_ENTRY_DELAY = pd.Timedelta(hours=2)
IDX_MAX_DELAY = pd.Timedelta(minutes=50)     # endeks: 15:00 ET kararı en geç 15:50'de uygulanır (16:00 seans kapanışı)


def env(k, d=None):
    v = os.getenv(k)
    return d if v is None or v == "" else v


def log(*a):
    print(f"[{pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M:%S}]", *a, flush=True)


DRY = env("ATVS_DRY", "0") == "1"
RISK = float(env("ATVS_RISK", "0.02"))   # v5.4: %25 düşüş toleransı satırı (ETH Donchian %2; kripto X %2, EMA %0.5 bununla ölçeklenir)
def _only():
    """Aktif botlar: repodaki aktif_botlar.txt (GitHub'dan telefonla düzenlenir) > ATVS_ONLY > hepsi."""
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aktif_botlar.txt")
    raw = env("ATVS_ONLY", "")
    if os.path.exists(fp):
        raw = ",".join(x.split("#")[0].strip() for x in open(fp, encoding="utf-8"))
    out = {}
    for item in raw.split(","):          # "XAU" ya da "ETH 150" (kasa ≥150 USDT olunca devreye girer)
        parts = item.split()
        if parts:
            v = parts[1].upper() if len(parts) > 1 else "0"
            out[parts[0].upper()] = -1.0 if v == "OTO" else float(v)       # -1 = eşiği bot kendisi hesaplar
    return out


ONLY = _only()   # boş = hepsi
LEV_MAX = int(env("ATVS_LEVERAGE", "50"))   # üst sınır; gerçek kaldıraç her işlemde otomatik seçilir
MARGIN_SHARE = 0.80 if len(ONLY) == 1 else 0.40   # run() içinde aktif bot sayısına göre güncellenir
LIQ_SAFETY = 4.0                            # tasfiye mesafesi ≥ 4 × stop mesafesi olmalı
SYMBOLS = {"XAU": env("SYM_XAU", "XAU/USDT:USDT"), "ETH": env("SYM_ETH", "ETH/USDT:USDT"),
           "BTC": env("SYM_BTC", "BTC/USDT:USDT"), "XAG": env("SYM_XAG", "XAG/USDT:USDT"),
           "NQ": env("SYM_NQ", C.IDX_SYMBOL["NQ"]), "SPX": env("SYM_SPX", C.IDX_SYMBOL["SPX"])}
IDX_FILE = os.path.join(C.LIVE_STATE_DIR, "endeks_finalist.json")
KR_FILE = os.path.join(C.LIVE_STATE_DIR, "kripto_finalist.json")
for _c in KR.COINS:
    SYMBOLS.setdefault(_c, env(f"SYM_{_c}", f"{_c}/USDT:USDT"))
KR_DEFAULT_THR = 300.0
# ── RİSK YÖNETİCİSİ (kasa koruması): zirveden düşüşe göre risk kademeli azalır; günlük zarar limiti
#    "eşik:çarpan" listesi — ör. düşüş ≥ %10 → risk ×0.5, ≥ %20 → ×0.25, ≥ %30 → yeni işlem YOK (açıklar yönetilir)
DD_STEPS = [tuple(float(v) for v in x.split(":")) for x in env("ATVS_DD_STEPS", "0.10:0.5,0.20:0.25,0.30:0").split(",")]
DAILY_LOSS = float(env("ATVS_DAILY_LOSS", "0.03"))     # gün içinde kasa bu oranda düşerse o gün yeni işlem yok
MAX_OPEN_RISK = float(env("ATVS_MAX_OPEN_RISK", "0.10"))   # açık pozisyonların stoplarına kadar toplam risk ≤ kasanın %10u
GOV = {"scale": 1.0, "why": "", "open_risk": 0.0}          # aktif_botlar.txt'de "KRIPTO OTO" yazılırsa kullanılacak kasa eşiği (USDT)


# ───────────────────────── borsa ─────────────────────────
def make_exchange():
    import ccxt
    ex = ccxt.bitget({"apiKey": env("BITGET_KEY"), "secret": env("BITGET_SECRET"), "password": env("BITGET_PASS"),
                      "enableRateLimit": True, "options": {"defaultType": "swap"}})
    if env("BITGET_DEMO", "1") == "1":
        try:
            ex.set_sandbox_mode(True)      # Bitget demo (paptrading) hesabı
        except Exception as e:
            raise RuntimeError(f"Demo modu açılamadı ({e}). requirements güncel mi? (pip install -U ccxt)")
    ex.load_markets()
    return ex


class Broker:
    """Borsa işlemlerini tek yerde toplar; her çağrı hata durumunda açıklayıcı mesaj verir."""

    def __init__(self, ex):
        self.ex = ex

    def equity(self) -> float:
        b = self.ex.fetch_balance({"type": "swap"})
        tot = b.get("total", {}).get("USDT") or b.get("USDT", {}).get("total")
        return float(tot or 0.0)

    def market(self, sym):
        if sym not in self.ex.markets:
            raise RuntimeError(f"Borsada '{sym}' sembolü bulunamadı. ~/atvs.env içinde SYM_... ayarını kontrol et.")
        return self.ex.markets[sym]

    def max_lev(self, sym) -> int:
        m = self.market(sym)
        v = (m.get("limits", {}).get("leverage", {}) or {}).get("max")
        return int(v) if v else 20

    def min_qty(self, sym) -> float:
        """Borsanın kabul ettiği en küçük miktar, dayanak varlık cinsinden (ons, ETH)."""
        m = self.market(sym)
        cs = float(m.get("contractSize") or 1.0)
        mn = float((m.get("limits", {}).get("amount", {}) or {}).get("min") or 0)
        mc = float((m.get("limits", {}).get("cost", {}) or {}).get("min") or 0)
        return mn * cs, mc

    def prepare(self, sym, lev):
        for fn in (lambda: self.ex.set_position_mode(False, sym), lambda: self.ex.set_margin_mode("cross", sym),
                   lambda: self.ex.set_leverage(lev, sym)):
            try:
                fn()
            except Exception as e:          # zaten ayarlıysa borsa hata döndürebilir — engel değil
                log(f"  (ayar uyarısı {sym}: {type(e).__name__}: {str(e)[:120]})")

    def amount(self, sym, qty) -> float:
        """qty: dayanak varlık cinsinden (ör. ons altın, ETH) → borsanın kontrat birimine çevrilir."""
        m = self.market(sym)
        cs = float(m.get("contractSize") or 1.0)
        q = float(self.ex.amount_to_precision(sym, qty / cs))
        mn = (m.get("limits", {}).get("amount", {}) or {}).get("min") or 0
        return q if q >= (mn or 0) and q > 0 else 0.0

    def price(self, sym, p) -> float:
        return float(self.ex.price_to_precision(sym, p))

    def last_price(self, sym) -> float:
        t = self.ex.fetch_ticker(sym)
        return float(t.get("last") or t.get("close") or 0.0)

    def position(self, sym) -> dict | None:
        for p in self.ex.fetch_positions([sym]):
            c = float(p.get("contracts") or 0)
            if c > 0 and p.get("symbol") == sym:
                return {"side": 1 if p.get("side") == "long" else -1, "qty": c, "entry": float(p.get("entryPrice") or 0)}
        return None

    def market_order(self, sym, side, qty, reduce=False):
        if DRY:
            log(f"  [DRY] piyasa {'AL' if side == 1 else 'SAT'} {qty} {sym} reduce={reduce}")
            return {"id": "dry", "average": None}
        return self.ex.create_order(sym, "market", "buy" if side == 1 else "sell", qty, None, {"reduceOnly": reduce} if reduce else {})

    def entry_order(self, sym, side, qty, tries: int = 3, wait_s: float = 20.0):
        """Giriş: post-only LİMİT emir (maker ücreti). En iyi alış/satış fiyatına konur; dolmazsa fiyat güncellenip
        tekrar denenir; `tries` deneme sonunda kalan miktar PİYASA emriyle tamamlanır (sinyal kaçırılmaz)."""
        if DRY or C.ORDER_MODE != "limit":
            return self.market_order(sym, side, qty)
        filled, cost = 0.0, 0.0
        for t in range(tries):
            rem = float(self.ex.amount_to_precision(sym, qty - filled)) if qty - filled > 0 else 0.0
            if rem <= 0:
                break
            try:
                tk = self.ex.fetch_ticker(sym)
                px = float(tk.get("bid") if side == 1 else tk.get("ask") or tk.get("last"))
                o = self.ex.create_order(sym, "limit", "buy" if side == 1 else "sell", rem, self.price(sym, px), {"postOnly": True})
                time.sleep(wait_s)
                st = self.ex.fetch_order(o["id"], sym)
                f = float(st.get("filled") or 0)
                if st.get("status") not in ("closed", "canceled"):
                    try:
                        self.ex.cancel_order(o["id"], sym)
                    except Exception:
                        pass
                    st = self.ex.fetch_order(o["id"], sym)
                    f = float(st.get("filled") or 0)
                if f > 0:
                    filled += f
                    cost += f * float(st.get("average") or px)
                log(f"  limit giriş denemesi {t + 1}/{tries}: {f}/{rem} doldu @ {px}")
            except Exception as e:
                log(f"  (limit giriş denemesi {t + 1} hata: {type(e).__name__}: {str(e)[:100]})")
        rem = float(self.ex.amount_to_precision(sym, qty - filled)) if qty - filled > 0 else 0.0
        mn = float((self.market(sym).get("limits", {}).get("amount", {}) or {}).get("min") or 0)
        if rem > 0 and rem >= mn:
            o = self.market_order(sym, side, rem)
            filled += rem
            cost += rem * float(o.get("average") or 0)
            log(f"  kalan {rem} piyasa emriyle tamamlandı")
        return {"id": "entry", "average": cost / filled if filled and cost else None, "filled": filled}

    def stop_order(self, sym, pos_side, qty, stop):
        """Pozisyonu kapatan tetikli piyasa emri (borsada bekler)."""
        if DRY:
            log(f"  [DRY] STOP {sym} @ {stop}")
            return "dry"
        o = self.ex.create_order(sym, "market", "sell" if pos_side == 1 else "buy", qty, None,
                                 {"triggerPrice": self.price(sym, stop), "reduceOnly": True})
        return o.get("id")

    def limit_close(self, sym, pos_side, qty, px):
        if DRY:
            log(f"  [DRY] HEDEF {sym} @ {px}")
            return "dry"
        o = self.ex.create_order(sym, "limit", "sell" if pos_side == 1 else "buy", qty, self.price(sym, px), {"reduceOnly": True})
        return o.get("id")

    def cancel(self, sym, oid, trigger=False):
        if DRY or not oid or oid == "dry":
            return
        try:
            self.ex.cancel_order(oid, sym, {"trigger": True} if trigger else {})
        except Exception as e:
            log(f"  (iptal uyarısı {oid}: {str(e)[:120]})")

    def candles(self, sym, tf, since_ms):
        return self.ex.fetch_ohlcv(sym, tf, since=since_ms, limit=200)

    def candles_all(self, sym, tf, since_ms, max_pages=12):
        out, cur = [], since_ms
        for _ in range(max_pages):
            rows = self.ex.fetch_ohlcv(sym, tf, since=cur, limit=200)
            rows = [r for r in rows if not out or r[0] > out[-1][0]]
            if not rows:
                break
            out += rows
            cur = rows[-1][0] + 1
            if len(rows) < 150:
                break
        return out


# ───────────────────────── durum ─────────────────────────
def load_state():
    st = LV.load_json(STATE_FILE, {"pos": {}, "last_bar": {}})
    st.setdefault("pos", {})
    st.setdefault("last_bar", {})
    return st


def realized(br, pos) -> dict:
    """İşlem kapandıktan sonra borsadaki gerçekleşen dolumlardan çıkış fiyatı, ücret ve net kâr/zarar."""
    out = {}
    try:
        sym, side = pos["symbol"], pos["side"]
        since = int(pd.Timestamp(pos["entry_time"]).timestamp() * 1000) - 120_000
        fills = br.ex.fetch_my_trades(sym, since=since, limit=100) if not DRY else []
        cs = float(br.market(sym).get("contractSize") or 1.0)
        ex_f = [f for f in fills if (f.get("side") == "sell") == (side == 1)]
        fee = sum(float((f.get("fee") or {}).get("cost") or 0) for f in fills)
        q = sum(float(f["amount"]) for f in ex_f)
        if q > 0:
            px = sum(float(f["amount"]) * float(f["price"]) for f in ex_f) / q
            pnl = side * (px - pos["entry"]) * q * cs - fee
            out = {"exit": px, "fee": fee, "pnl_usdt": pnl}
            if pos.get("risk_usdt"):
                out["R"] = pnl / pos["risk_usdt"]
    except Exception as e:
        log(f"  (gerçekleşen kâr/zarar okunamadı: {type(e).__name__}: {str(e)[:100]})")
    return out


def record(row: dict, br=None, pos=None):
    if br is not None and pos is not None:
        time.sleep(0 if DRY else 2)
        row.update({"qty": pos.get("qty"), "eq_entry": pos.get("eq_entry"), "risk_usdt": pos.get("risk_usdt")})
        row.update(realized(br, pos))
    os.makedirs(C.LIVE_STATE_DIR, exist_ok=True)
    new = not os.path.exists(TRADES_FILE)
    pd.DataFrame([row]).to_csv(TRADES_FILE, mode="a", header=new, index=False)


# ───────────────────────── yönetim ─────────────────────────
def manage(br: Broker, fz: dict, pos: dict, now: pd.Timestamp) -> dict | None:
    """Açık pozisyonu backtest kurallarıyla yönet. Kapandıysa None döner."""
    sym, cfg = pos["symbol"], fz["exit_cfg"]
    live = br.position(sym)
    if live is None:
        log(f"  {fz['id']}: pozisyon borsada kapanmış (stop/hedef gerçekleşti) → kalan emirler iptal")
        br.cancel(sym, pos.get("stop_id"), trigger=True)
        br.cancel(sym, pos.get("tp_id"))
        record({"id": fz["id"], "symbol": sym, "side": pos["side"], "entry_time": pos["entry_time"], "entry": pos["entry"],
                "exit_time": str(now), "reason": "borsada stop/hedef", "stop_last": pos["stop"]}, br, pos)
        return None
    side, e, atr = pos["side"], pos["entry"], pos["atr"]
    risk = cfg["sl_atr"] * atr
    step = pd.Timedelta(minutes=TF_MIN[fz["tf"]])
    sig_t = pd.Timestamp(pos["signal_time"])
    entry_bar = sig_t + step
    if fz["tf"] == "1d":      # günlük: saatlik mumlardan yalnızca TAMAMLANMIŞ UTC günleri (backtest ile aynı)
        rows = br.candles_all(sym, "1h", int(entry_bar.timestamp() * 1000))
        day_end = now.floor("D")
        closed = [r for r in rows if pd.Timestamp(r[0], unit="ms", tz="UTC") >= entry_bar
                  and pd.Timestamp(r[0], unit="ms", tz="UTC") + pd.Timedelta(hours=1) <= day_end]
    else:
        rows = br.candles(sym, fz["tf"], int(entry_bar.timestamp() * 1000))
        closed = [r for r in rows if pd.Timestamp(r[0], unit="ms", tz="UTC") + step <= now and pd.Timestamp(r[0], unit="ms", tz="UTC") >= entry_bar]
    bars_held = int((now - entry_bar) / step)
    new_stop = pos["stop"]
    if closed:
        hi = max(r[2] for r in closed) if side == 1 else -min(r[3] for r in closed)
        e_s = side * e
        if cfg.get("tp1") is not None and not pos["be"] and hi >= e_s + cfg["tp1"] * risk:
            pos["be"] = True
            log(f"  {fz['id']}: TP1 (+{cfg['tp1']}R) görüldü → stop girişe")
            if cfg.get("part"):
                q = br.amount(sym, live["qty"] * cfg["part"])
                if q > 0:
                    br.market_order(sym, -side, q, reduce=True)
        cand = side * new_stop
        if pos["be"]:
            cand = max(cand, e_s)
        if cfg.get("trail") is not None and (pos["be"] or cfg.get("trail_mode", "always") != "be"):
            cand = max(cand, max(e_s, hi) - cfg["trail"] * atr)
        new_stop = side * cand
    if bars_held >= fz.get("horizon", C.HORIZON):
        log(f"  {fz['id']}: zaman bariyeri ({bars_held} mum) → piyasadan kapat")
        br.cancel(sym, pos.get("stop_id"), trigger=True)
        br.cancel(sym, pos.get("tp_id"))
        br.market_order(sym, -side, live["qty"], reduce=True)
        record({"id": fz["id"], "symbol": sym, "side": side, "entry_time": pos["entry_time"], "entry": e,
                "exit_time": str(now), "reason": "zaman", "stop_last": pos["stop"]}, br, pos)
        return None
    if abs(new_stop - pos["stop"]) > 1e-12 and side * new_stop > side * pos["stop"]:
        log(f"  {fz['id']}: stop {pos['stop']:.4f} → {new_stop:.4f}")
        old = pos.get("stop_id")
        pos["stop_id"] = br.stop_order(sym, side, live["qty"], new_stop)   # önce yeni stop, sonra eskisini iptal (korumasız an olmaz)
        br.cancel(sym, old, trigger=True)
        pos["stop"] = new_stop
    return pos


def min_equity(br, sym, sl_atr, tf="4h", risk=None):
    """Borsanın asgari miktarıyla %RISK'te işlem açabilmek için gereken en küçük kasa (güncel fiyat ve ATR ile)."""
    risk = risk or RISK
    mq, mc = br.min_qty(sym)
    c = br.candles(sym, tf, int((pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=20 if tf == "4h" else 60)).timestamp() * 1000))
    d = pd.DataFrame(c, columns=["t", "o", "h", "l", "c", "v"])
    tr = pd.concat([d.h - d.l, (d.h - d.c.shift()).abs(), (d.l - d.c.shift()).abs()], axis=1).max(axis=1)
    atr, px = float(tr.tail(14).mean()), float(d.c.iloc[-1])
    dist = sl_atr * atr
    need = max(mq * dist, (mc / px) * dist if mc else 0) / risk * 1.2
    return need, px, atr, dist, mq


def choose_leverage(br, sym, eq, dist, px, risk=None):
    """Gereken en düşük kaldıracı seçer. Güvenlik: tasfiye fiyatı stoptan en az LIQ_SAFETY kat uzakta kalmalı.
    Kaldıraç riski artırmaz (risk = stop mesafesi × miktar); yalnızca bağlanan teminatı azaltır."""
    notional = eq * (risk or RISK) / dist * px
    need = max(1, math.ceil(notional / (eq * MARGIN_SHARE)))
    safe = max(1, math.floor(px / (LIQ_SAFETY * dist)))        # kabaca tasfiye mesafesi ≈ fiyat / kaldıraç
    cap = min(LEV_MAX, br.max_lev(sym), safe)
    if need > cap:
        return None, (f"gereken kaldıraç {need}x, güvenli üst sınır {cap}x "
                      f"(borsa {br.max_lev(sym)}x, tasfiye güvenliği {safe}x) — kasa bu pozisyon için yetersiz")
    return need, f"pozisyon {notional:.0f} USDT · teminat ≈ {notional / need:.1f} USDT · güvenli üst sınır {cap}x"


def open_trade(br: Broker, fz: dict, side: int, atr_sig: float, sig_time, ref_px: float,
               risk: float | None = None, sl_mult: float | None = None) -> dict | None:
    """atr_sig ve ref_px VERİ kaynağının biriminde (ör. NQ endeks puanı); borsa fiyatına oranla ölçeklenir (QQQ)."""
    sym, cfg = SYMBOLS[fz["asset"]], fz.get("exit_cfg", {})
    risk = (risk or RISK) * GOV["scale"]
    if risk <= 0:
        log(f"  {fz['id']}: sinyal var ama risk yöneticisi yeni işlemi durdurdu ({GOV['why']})")
        return None
    br.market(sym)
    eq = br.equity()
    if GOV["open_risk"] + risk > MAX_OPEN_RISK:
        log(f"  {fz['id']}: sinyal var ama açık toplam risk %{100 * GOV['open_risk']:.1f} + %{100 * risk:.2f} > tavan %{100 * MAX_OPEN_RISK:.0f} — atlandı")
        return None
    px_x = ref_px if DRY else (br.last_price(sym) or ref_px)
    scale = px_x / ref_px if ref_px > 0 else 1.0
    if not 0.2 < scale < 5 and fz["asset"] not in C.IDX_SYMBOL:
        scale = 1.0
    atr_x = atr_sig * scale
    dist = (sl_mult if sl_mult is not None else cfg["sl_atr"]) * atr_x
    qty = br.amount(sym, eq * risk / dist)
    if qty <= 0:
        log(f"  {fz['id']}: miktar borsanın asgarisinin altında (kasa {eq:.2f} USDT, stop mesafesi {dist:.4f}) — işlem atlandı")
        return None
    lev, why = choose_leverage(br, sym, eq, dist, px_x, risk)
    if lev is None:
        log(f"  {fz['id']}: {why} — işlem atlandı")
        return None
    br.prepare(sym, lev)
    log(f"  {fz['id']}: kaldıraç {lev}x ({why})")
    o = br.entry_order(sym, side, qty)
    fill = float(o.get("average") or 0) or px_x
    if not DRY:
        time.sleep(1.0)
        p = br.position(sym)
        if p:
            fill = p["entry"] or fill
    stop = fill - side * dist
    pos = {"symbol": sym, "side": side, "qty": qty, "entry": fill, "entry_time": str(pd.Timestamp.now(tz="UTC")),
           "eq_entry": eq, "risk_usdt": eq * risk, "dist": dist,
           "signal_time": str(sig_time), "atr": atr_x, "stop": stop, "be": False}
    GOV["open_risk"] += risk
    pos["stop_id"] = br.stop_order(sym, side, qty, stop)
    pos["tp_id"] = br.limit_close(sym, side, qty, fill + side * cfg["tp"] * dist) if cfg.get("tp") is not None else None
    log(f"  {fz['id']}: {'LONG' if side == 1 else 'SHORT'} {qty} {sym} @ {fill:.4f} · stop {stop:.4f}"
        + (f" · hedef {fill + side * cfg['tp'] * dist:.4f}" if cfg.get("tp") is not None else "") + f" · kasa {eq:.2f} USDT")
    return pos


def auto_threshold(br, asset, st) -> float:
    """OTO eşik = 2 × güncel asgari kasa. Günde bir yeniden hesaplanır (fiyat/volatilite değiştikçe eşik de değişir)."""
    cache = st.setdefault("oto_esik", {})
    day = str(pd.Timestamp.now(tz="UTC").date())
    if cache.get(asset, {}).get("day") != day:
        meta = LV.load_json(FIN_FILE, {})
        f = next((x for x in meta.get("finalistler", []) if x["asset"] == asset), None)
        fi = next((x for x in idx_finalists() if x["asset"] == asset), None)
        if (f is None and fi is None) or asset not in SYMBOLS:
            return float("inf")
        if f is not None:
            need = min_equity(br, SYMBOLS[asset], f["exit_cfg"]["sl_atr"])[0]
        else:
            need = min_equity(br, SYMBOLS[asset], fi["spec"]["k"], "1d", idx_risk(fi))[0]
        cache[asset] = {"day": day, "thr": round(2 * need, 2)}
        log(f"{asset} OTO eşik: {2 * need:.0f} USDT (asgari kasa {need:.0f} × 2)")
    return cache[asset]["thr"]


def idx_finalists() -> list:
    return [f for f in LV.load_json(IDX_FILE, {}).get("finalistler", []) if f.get("engine") == "idx"]


def idx_risk(fz) -> float:
    """Endeks stratejisinin riski: araştırmanın önerdiği risk × (ATVS_RISK / %1). ATVS_RISK yarıya inerse bu da yarıya iner."""
    return float(fz.get("risk", 0.01)) * (RISK / 0.01)


def run_idx(br: Broker, fz: dict, pos: dict | None, st: dict, now: pd.Timestamp) -> dict | None:
    """Endeks motoru (lab/index_lab.py ile birebir aynı kurallar; selftest T8)."""
    fid, s, sym = fz["id"], fz["spec"], SYMBOLS[fz["asset"]]
    if pos and br.position(sym) is None:
        log(f"  {fid}: pozisyon borsada kapanmış (stop) → kalan emirler iptal")
        br.cancel(sym, pos.get("stop_id"), trigger=True)
        record({"id": fid, "symbol": sym, "side": 1, "entry_time": pos["entry_time"], "entry": pos["entry"],
                "exit_time": str(now), "reason": "borsada stop", "stop_last": pos["stop"]}, br, pos)
        pos = None
    dec = IL.live_decision(LV.base_1h(fz["asset"]), s, now)
    if dec is None:
        log(f"  {fid}: yeterli veri yok")
        return pos
    if st["last_bar"].get(fid) == dec["day"]:
        return pos
    st["last_bar"][fid] = dec["day"]
    if now - dec["t_dec"] > IDX_MAX_DELAY:
        log(f"  {fid}: {dec['day']} kararı geç görüldü ({now - dec['t_dec']}) — ABD seansı kapanmış olabilir, atlandı")
        return pos
    if pos:
        if dec["day"] <= pos["entry_day"]:
            return pos
        pos["held"] = pos.get("held", 0) + 1
        if dec["exit"] or pos["held"] >= s["tmax"]:
            why = "sinyal" if dec["exit"] else "zaman"
            live = br.position(sym)
            log(f"  {fid}: çıkış ({why}, {pos['held']}. gün) → piyasadan kapat")
            br.cancel(sym, pos.get("stop_id"), trigger=True)
            if live:
                br.market_order(sym, -1, live["qty"], reduce=True)
            record({"id": fid, "symbol": sym, "side": 1, "entry_time": pos["entry_time"], "entry": pos["entry"],
                    "exit_time": str(now), "reason": why, "stop_last": pos["stop"]}, br, pos)
            return None
        log(f"  {fid}: {dec['day']} — pozisyon açık ({pos['held']}/{s['tmax']} gün)")
        return pos
    if dec["entry"]:
        try:
            newp = open_trade(br, fz, 1, dec["atr"], dec["t_dec"], dec["close"], risk=idx_risk(fz), sl_mult=s["k"])
        except Exception as e:      # ABD tatili / seans dışı: borsa yeni pozisyonu reddedebilir
            log(f"  {fid}: emir reddedildi ({type(e).__name__}: {str(e)[:120]}) — bugün atlandı")
            return None
        if newp:
            newp.update(spec=fz, entry_day=dec["day"], held=0, engine="idx")
        return newp
    log(f"  {fid}: {dec['day']} — sinyal yok")
    return None


def kr_finalists() -> dict:
    return LV.load_json(KR_FILE, {})


def kr_daily(coin: str, interval: str = "1d") -> pd.DataFrame:
    """Binance mumları (son 1000 mum; EMA/ATR için fazlasıyla yeterli ısınma). Yalnızca KAPANMIŞ mumlar."""
    import requests
    step = pd.Timedelta(interval.replace("d", "D"))
    for host in ("https://data-api.binance.vision", "https://api.binance.com"):
        try:
            r = requests.get(f"{host}/api/v3/klines", params={"symbol": f"{coin}USDT", "interval": interval, "limit": 1000}, timeout=20)
            if r.status_code == 200 and r.json():
                a = np.array([[float(x) for x in b[:6]] for b in r.json()])
                df = pd.DataFrame(a[:, 1:6], index=pd.to_datetime(a[:, 0].astype("int64"), unit="ms", utc=True),
                                  columns=["open", "high", "low", "close", "volume"])
                return df[df.index + step <= LV.now_utc()]
        except Exception:
            continue
    return pd.DataFrame()


def run_kripto(br: Broker, st: dict, now: pd.Timestamp, live_set) -> None:
    """Kripto günlük kuralları: günde bir kez (UTC gün kapanışından sonraki ilk çalıştırma). Coin başına tek pozisyon,
    toplam en fazla max_acik açık pozisyon (diğer stratejiler dahil)."""
    meta = kr_finalists()
    fins = meta.get("finalistler", [])
    if not fins:
        return
    on = live_set is not None and "KRIPTO" in live_set
    # açık kripto pozisyonlarını yönet (her çalıştırmada; yeni gün yoksa iz süren stop değişmez)
    for key, pos in list(st["pos"].items()):
        if pos and pos.get("engine") == "kripto1d":
            try:
                st["pos"][key] = manage(br, pos["spec"], pos, now)
            except Exception:
                log(f"  {key}: HATA\n{traceback.format_exc()}")
    if not on:
        return
    max_open = int(meta.get("max_acik", 6))
    busy = {p["symbol"] for p in st["pos"].values() if p}
    n_open = sum(1 for p in st["pos"].values() if p)
    for fz in fins:                                         # dosyadaki sıra = öncelik
        tf = fz.get("tf", "1d")
        step = pd.Timedelta(minutes=TF_MIN[tf])
        last_close = now.floor("D") if tf == "1d" else now.floor(step)       # son kapanan mumun bitişi
        bar = str(last_close - step)
        bkey = f"KRIPTO:{fz['id']}"
        if st["last_bar"].get(bkey) == bar:
            continue
        st["last_bar"][bkey] = bar
        if now - last_close > MAX_ENTRY_DELAY:
            log(f"  {fz['id']}: {bar} mumu geç görüldü — kovalamamak için girişler atlandı")
            continue
        for coin in fz["coins"]:
            sym = SYMBOLS.get(coin)
            key = f"{fz['id']}:{coin}"
            if not sym or st["pos"].get(key):
                continue
            try:
                df = kr_daily(coin, tf)
                if len(df) < 300 or str(df.index[-1]) != bar:
                    continue
                L, S = KR.entries(df, tf_min=TF_MIN[tf])[fz["rule"]]
                go_l, go_s = bool(L[-1]) and fz["scope"] in ("long", "both"), bool(S[-1]) and fz["scope"] in ("short", "both")
                if not (go_l ^ go_s):
                    continue
                if sym in busy:
                    log(f"  {key}: sinyal var ama {coin}'de zaten pozisyon var — atlandı")
                    continue
                if n_open >= max_open:
                    log(f"  {key}: sinyal var ama açık pozisyon sınırı ({max_open}) dolu — atlandı")
                    continue
                atr = float(FT.compute(df)["atr"].iloc[-1])
                spec = {**fz, "asset": coin, "id": key}
                newp = open_trade(br, spec, 1 if go_l else -1, atr, df.index[-1], float(df["close"].iloc[-1]),
                                  risk=float(fz["risk"]) * (RISK / 0.01))
                if newp:
                    newp.update(spec=spec, engine="kripto1d")
                    st["pos"][key] = newp
                    busy.add(sym)
                    n_open += 1
            except Exception:
                log(f"  {key}: HATA\n{traceback.format_exc()}")
        log(f"  {fz['id']}: {bar} mumu tarandı · açık pozisyon {n_open}/{max_open}")


def active_assets(eq: float, st: dict, br=None) -> set:
    """Kasa eşiğine göre otomatik devreye alma. Geri düşüşte %20 tampon: eşik 150 ise 120'nin altında yeni işlem durur."""
    act = st.setdefault("active", {})
    out = set()
    for a, thr in ONLY.items():
        if a == "KRIPTO" and thr < 0:
            thr = KR_DEFAULT_THR
        if thr < 0:
            try:
                thr = auto_threshold(br, a, st)
            except Exception as e:
                log(f"{a} OTO eşik hesaplanamadı ({type(e).__name__}) — önceki durum korunuyor")
                if act.get(a):
                    out.add(a)
                continue
        was = act.get(a, False)
        on = eq >= thr if not was else eq >= 0.8 * thr
        if on != was:
            log(f"{'🟢 ' + a + ' botu DEVREYE GİRDİ' if on else '⏸ ' + a + ' botu yeni işlemleri durdurdu'} "
                f"(kasa {eq:.2f} USDT, eşik {thr:.0f})")
        act[a] = on
        if on:
            out.add(a)
    return out


EQUITY_FILE = os.path.join(C.LIVE_STATE_DIR, "kasa_log.csv")


def log_equity(br, st):
    """Her çalıştırmada kasa + o aradaki para giriş/çıkışı (transfer) kaydı → panel için zaman ağırlıklı getiri."""
    try:
        eq = br.equity()
        now = pd.Timestamp.now(tz="UTC")
        last = st.get("ledger_ms") or int((now - pd.Timedelta(hours=2)).timestamp() * 1000)
        flow, newest = 0.0, last
        try:
            for x in (br.ex.fetch_ledger("USDT", since=last + 1, limit=100, params={"productType": "USDT-FUTURES"}) if not DRY else []):
                ts = int(x.get("timestamp") or 0)
                newest = max(newest, ts)
                typ = str(x.get("type") or "") + " " + str((x.get("info") or {}).get("businessType") or "")
                if "trans" in typ.lower():          # cüzdanlar arası transfer = yatırım / çekim
                    amt = float(x.get("amount") or 0)
                    flow += amt if x.get("direction") != "out" else -amt
        except Exception as e:
            log(f"  (transfer kaydı okunamadı — panelde yatirimlar.csv kullanılabilir: {type(e).__name__})")
        st["ledger_ms"] = newest
        os.makedirs(C.LIVE_STATE_DIR, exist_ok=True)
        new = not os.path.exists(EQUITY_FILE)
        opn = sum(1 for p in st["pos"].values() if p)
        pd.DataFrame([{"time": str(now.floor("min")), "equity": round(eq, 4), "flow": round(flow, 4), "open_positions": opn}]) \
          .to_csv(EQUITY_FILE, mode="a", header=new, index=False)
    except Exception as e:
        log(f"  (kasa kaydı yazılamadı: {type(e).__name__}: {str(e)[:100]})")


def governor(eq: float, st: dict, now: pd.Timestamp) -> None:
    """Kasa koruması: zirve kasa ve gün başı kasası durum dosyasında tutulur."""
    g = st.setdefault("gov", {})
    g["peak"] = max(float(g.get("peak", 0.0)), eq)
    day = str(now.date())
    if g.get("day") != day:
        g["day"], g["day_start"] = day, eq
    dd = 1 - eq / g["peak"] if g["peak"] > 0 else 0.0
    scale, why = 1.0, ""
    for thr, mult in sorted(DD_STEPS):
        if dd >= thr:
            scale, why = mult, f"zirveden düşüş %{100 * dd:.1f} ≥ %{100 * thr:.0f} → risk ×{mult:g}"
    if g["day_start"] > 0 and eq <= g["day_start"] * (1 - DAILY_LOSS):
        scale, why = 0.0, f"günlük zarar limiti (%{100 * DAILY_LOSS:.0f}) doldu — yarına kadar yeni işlem yok"
    open_risk = 0.0
    for p in st.get("pos", {}).values():           # stop girişe/kâra çekilmiş pozisyonlar artık risk taşımaz
        if p and p.get("risk_usdt") and eq > 0:
            at_risk = p["side"] * (p["entry"] - p["stop"]) > 0
            open_risk += (p["risk_usdt"] / eq) if at_risk else 0.0
    GOV.update(scale=scale, why=why, dd=dd, open_risk=open_risk)
    if why:
        log(f"  RİSK YÖNETİCİSİ: {why}")


def run(br: Broker):
    global MARGIN_SHARE
    meta = LV.load_json(FIN_FILE, {})
    st = load_state()
    _eq = br.equity()
    governor(_eq, st, LV.now_utc())
    if ONLY:
        live_set = active_assets(_eq, st, br)
        MARGIN_SHARE = 0.25 if "KRIPTO" in live_set else (0.80 if len(live_set) == 1 else (0.40 if len(live_set) == 2 else 0.30))
    else:
        live_set = None
    fins = [f for f in meta.get("finalistler", []) if f["asset"] in SYMBOLS and (live_set is None or f["asset"] in live_set)]
    # endeks stratejileri yalnızca aktif_botlar.txt'de AÇIKÇA yazılıysa çalışır
    fins += [f for f in idx_finalists() if f["asset"] in SYMBOLS and live_set is not None and f["asset"] in live_set]
    now = LV.now_utc()
    run_kripto(br, st, now, live_set)
    if not fins and not any(p for p in st["pos"].values() if p and p.get("engine") != "kripto1d"):
        log_equity(br, st)
        LV.save_json(STATE_FILE, st)
        log("finalist yok — bekleniyor")
        return
    by_id = {f["id"]: f for f in fins}
    for fid, p in st["pos"].items():
        if p and fid not in by_id and p.get("engine") != "kripto1d":
            by_id[fid] = p["spec"]
    for fid, fz in by_id.items():
        try:
            pos = st["pos"].get(fid)
            if fz.get("engine") == "idx" or (pos and pos.get("engine") == "idx"):
                st["pos"][fid] = run_idx(br, fz if fz.get("engine") == "idx" else pos["spec"], pos, st, now)
                continue
            if pos:
                pos = manage(br, fz, pos, now)
                st["pos"][fid] = pos
            ctx = LV.build(fz["asset"], fz["tf"], fz["family"])
            df, book = ctx["df"], ctx["book"]
            if fz["entry"] not in book.items:
                raise RuntimeError(f"giriş defterde yok: {fz['entry']}")
            _, L, S = book.items[fz["entry"]]
            j = len(df) - 1
            bar_t = df.index[j]
            if st["last_bar"].get(fid) == str(bar_t):
                continue
            st["last_bar"][fid] = str(bar_t)
            go_l = bool(L[j]) and fz["scope"] in ("both", "long")
            go_s = bool(S[j]) and fz["scope"] in ("both", "short")
            if pos is None and (go_l ^ go_s) and any(p and p.get("symbol") == SYMBOLS[fz["asset"]] for k, p in st["pos"].items() if k != fid):
                log(f"  {fid}: sinyal var ama {fz['asset']}'de başka stratejinin pozisyonu açık — atlandı (coin başına tek pozisyon)")
            elif pos is None and (go_l ^ go_s):
                close_t = bar_t + pd.Timedelta(minutes=TF_MIN[fz["tf"]])
                if now - close_t > MAX_ENTRY_DELAY:
                    log(f"  {fid}: sinyal geç görüldü ({now - close_t}) — kovalamamak için atlandı")
                    continue
                atr = float(ctx["f"]["atr"].iloc[j])
                newp = open_trade(br, fz, 1 if go_l else -1, atr, bar_t, float(df["close"].iloc[j]))
                if newp:
                    newp["spec"] = fz
                st["pos"][fid] = newp
            else:
                log(f"  {fid}: {bar_t:%Y-%m-%d %H:%M} mumu — {'pozisyon açık' if pos else 'sinyal yok'}")
        except Exception:
            log(f"  {fid}: HATA\n{traceback.format_exc()}")
    log_equity(br, st)
    LV.save_json(STATE_FILE, st)


def kontrol(br: Broker):
    log(f"Bağlantı: {'DEMO' if env('BITGET_DEMO', '1') == '1' else 'GERÇEK'} hesap · DRY={DRY} · risk %{100 * RISK:.2g} · kaldıraç otomatik (üst sınır {LEV_MAX}x)")
    eq = br.equity()
    log(f"Kasa: {eq:.2f} USDT")
    meta = LV.load_json(FIN_FILE, {})
    if ONLY:
        log("Botlar: " + ", ".join((f"{a} (kasa ≥ OTO)" if t < 0 else f"{a} (kasa ≥ {t:.0f})") if t else a for a, t in ONLY.items()))
    for f in meta.get("finalistler", []):
        if ONLY and f["asset"] not in ONLY:
            continue
        sym = SYMBOLS.get(f["asset"])
        if not sym:
            log(f"  {f['id']}: bu varlık için sembol tanımlı değil — atlanacak")
            continue
        m = br.market(sym)
        log(f"  {f['id']}: {sym} bulundu · pozisyon: {br.position(sym)}")
        try:
            need, px, atr, dist, mq = min_equity(br, sym, f["exit_cfg"]["sl_atr"])
            lev, why = choose_leverage(br, sym, max(eq, need), dist, px)
            log(f"     fiyat {px:.2f} · ATR(4h) {atr:.2f} · stop mesafesi {dist:.2f} · asgari miktar {mq}")
            log(f"     ➜ ASGARİ KASA (risk %{100 * RISK:.2g}): {need:.0f} USDT · OTO eşik (2×): {2 * need:.0f} USDT · "
                f"o kasada kaldıraç: {lev if lev else 'YETERSİZ'}x")
        except Exception as e:
            log(f"     asgari kasa hesaplanamadı: {type(e).__name__}: {str(e)[:100]}")
    for f in idx_finalists():
        sym = SYMBOLS.get(f["asset"])
        act = bool(ONLY) and f["asset"] in ONLY
        log(f"  {f['id']} (endeks, {'AKTİF' if act else 'kapalı — aktif_botlar.txt’ye ' + f['asset'] + ' eklenirse çalışır'}): {sym}")
        try:
            br.market(sym)
            need, px, atr, dist, mq = min_equity(br, sym, f["spec"]["k"], "1d", idx_risk(f))
            log(f"     fiyat {px:.2f} · günlük ATR {atr:.2f} · stop mesafesi {dist:.2f} · asgari miktar {mq} · "
                f"risk %{100 * idx_risk(f):.2g} → ASGARİ KASA {need:.0f} USDT · OTO eşik {2 * need:.0f} USDT")
        except Exception as e:
            log(f"     kontrol edilemedi: {type(e).__name__}: {str(e)[:120]}")
    km = kr_finalists()
    for f in km.get("finalistler", []):
        act = bool(ONLY) and "KRIPTO" in ONLY
        log(f"  {f['id']} (kripto günlük, risk %{100 * f['risk'] * RISK / 0.01:.2g}, {len(f['coins'])} coin): "
            f"{'AKTİF' if act else 'kapalı — aktif_botlar.txt’ye KRIPTO eklenirse çalışır'}")
    if km.get("finalistler"):
        miss = []
        for coin in KR.COINS:
            try:
                br.market(SYMBOLS[coin])
            except Exception:
                miss.append(coin)
        log(f"     Bitget'te bulunamayan kripto sembolleri: {', '.join(miss) if miss else 'yok — hepsi tamam'}")
    log("Kontrol tamam.")


def main():
    ex = make_exchange()
    br = Broker(ex)
    if "--kontrol" in sys.argv:
        kontrol(br)
    else:
        run(br)


if __name__ == "__main__":
    main()
