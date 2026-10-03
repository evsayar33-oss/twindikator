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
  ATVS_RISK=0.01                           işlem başına kasa riski
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

STATE_FILE = os.path.join(C.LIVE_STATE_DIR, "trader_state.json")
TRADES_FILE = os.path.join(C.LIVE_STATE_DIR, "trader_trades.csv")
FIN_FILE = os.path.join(C.LIVE_STATE_DIR, "finalists.json")
TF_MIN = {"1h": 60, "4h": 240}
MAX_ENTRY_DELAY = pd.Timedelta(hours=2)


def env(k, d=None):
    v = os.getenv(k)
    return d if v is None or v == "" else v


def log(*a):
    print(f"[{pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M:%S}]", *a, flush=True)


DRY = env("ATVS_DRY", "0") == "1"
RISK = float(env("ATVS_RISK", "0.01"))
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
           "BTC": env("SYM_BTC", "BTC/USDT:USDT"), "XAG": env("SYM_XAG", "XAG/USDT:USDT")}


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


# ───────────────────────── durum ─────────────────────────
def load_state():
    st = LV.load_json(STATE_FILE, {"pos": {}, "last_bar": {}})
    st.setdefault("pos", {})
    st.setdefault("last_bar", {})
    return st


def record(row: dict):
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
                "exit_time": str(now), "reason": "borsada stop/hedef", "stop_last": pos["stop"]})
        return None
    side, e, atr = pos["side"], pos["entry"], pos["atr"]
    risk = cfg["sl_atr"] * atr
    step = pd.Timedelta(minutes=TF_MIN[fz["tf"]])
    sig_t = pd.Timestamp(pos["signal_time"])
    entry_bar = sig_t + step
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
                "exit_time": str(now), "reason": "zaman", "stop_last": pos["stop"]})
        return None
    if abs(new_stop - pos["stop"]) > 1e-12 and side * new_stop > side * pos["stop"]:
        log(f"  {fz['id']}: stop {pos['stop']:.4f} → {new_stop:.4f}")
        old = pos.get("stop_id")
        pos["stop_id"] = br.stop_order(sym, side, live["qty"], new_stop)   # önce yeni stop, sonra eskisini iptal (korumasız an olmaz)
        br.cancel(sym, old, trigger=True)
        pos["stop"] = new_stop
    return pos


def min_equity(br, sym, sl_atr):
    """Borsanın asgari miktarıyla %RISK'te işlem açabilmek için gereken en küçük kasa (güncel fiyat ve ATR ile)."""
    mq, mc = br.min_qty(sym)
    c = br.candles(sym, "4h", int((pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=20)).timestamp() * 1000))
    d = pd.DataFrame(c, columns=["t", "o", "h", "l", "c", "v"])
    tr = pd.concat([d.h - d.l, (d.h - d.c.shift()).abs(), (d.l - d.c.shift()).abs()], axis=1).max(axis=1)
    atr, px = float(tr.tail(14).mean()), float(d.c.iloc[-1])
    dist = sl_atr * atr
    need = max(mq * dist, (mc / px) * dist if mc else 0) / RISK * 1.2
    return need, px, atr, dist, mq


def choose_leverage(br, sym, eq, dist, px):
    """Gereken en düşük kaldıracı seçer. Güvenlik: tasfiye fiyatı stoptan en az LIQ_SAFETY kat uzakta kalmalı.
    Kaldıraç riski artırmaz (risk = stop mesafesi × miktar); yalnızca bağlanan teminatı azaltır."""
    notional = eq * RISK / dist * px
    need = max(1, math.ceil(notional / (eq * MARGIN_SHARE)))
    safe = max(1, math.floor(px / (LIQ_SAFETY * dist)))        # kabaca tasfiye mesafesi ≈ fiyat / kaldıraç
    cap = min(LEV_MAX, br.max_lev(sym), safe)
    if need > cap:
        return None, (f"gereken kaldıraç {need}x, güvenli üst sınır {cap}x "
                      f"(borsa {br.max_lev(sym)}x, tasfiye güvenliği {safe}x) — kasa bu pozisyon için yetersiz")
    return need, f"pozisyon {notional:.0f} USDT · teminat ≈ {notional / need:.1f} USDT · güvenli üst sınır {cap}x"


def open_trade(br: Broker, fz: dict, side: int, atr_sig: float, sig_time, ref_px: float) -> dict | None:
    sym, cfg = SYMBOLS[fz["asset"]], fz["exit_cfg"]
    br.market(sym)
    eq = br.equity()
    dist = cfg["sl_atr"] * atr_sig
    qty = br.amount(sym, eq * RISK / dist)
    if qty <= 0:
        log(f"  {fz['id']}: miktar borsanın asgarisinin altında (kasa {eq:.2f} USDT, stop mesafesi {dist:.4f}) — işlem atlandı")
        return None
    lev, why = choose_leverage(br, sym, eq, dist, ref_px)
    if lev is None:
        log(f"  {fz['id']}: {why} — işlem atlandı")
        return None
    br.prepare(sym, lev)
    log(f"  {fz['id']}: kaldıraç {lev}x ({why})")
    o = br.market_order(sym, side, qty)
    fill = float(o.get("average") or 0) or ref_px
    if not DRY:
        time.sleep(1.0)
        p = br.position(sym)
        if p:
            fill = p["entry"] or fill
    stop = fill - side * dist
    pos = {"symbol": sym, "side": side, "qty": qty, "entry": fill, "entry_time": str(pd.Timestamp.now(tz="UTC")),
           "signal_time": str(sig_time), "atr": atr_sig, "stop": stop, "be": False}
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
        if f is None or asset not in SYMBOLS:
            return float("inf")
        need = min_equity(br, SYMBOLS[asset], f["exit_cfg"]["sl_atr"])[0]
        cache[asset] = {"day": day, "thr": round(2 * need, 2)}
        log(f"{asset} OTO eşik: {2 * need:.0f} USDT (asgari kasa {need:.0f} × 2)")
    return cache[asset]["thr"]


def active_assets(eq: float, st: dict, br=None) -> set:
    """Kasa eşiğine göre otomatik devreye alma. Geri düşüşte %20 tampon: eşik 150 ise 120'nin altında yeni işlem durur."""
    act = st.setdefault("active", {})
    out = set()
    for a, thr in ONLY.items():
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


def run(br: Broker):
    global MARGIN_SHARE
    meta = LV.load_json(FIN_FILE, {})
    st = load_state()
    if ONLY:
        live_set = active_assets(br.equity(), st, br)
        MARGIN_SHARE = 0.80 if len(live_set) == 1 else 0.40
    else:
        live_set = None
    fins = [f for f in meta.get("finalistler", []) if f["asset"] in SYMBOLS and (live_set is None or f["asset"] in live_set)]
    now = LV.now_utc()
    if not fins and not any(st["pos"].values()):
        log("finalist yok — bekleniyor")
        return
    by_id = {f["id"]: f for f in fins}
    for fid, p in st["pos"].items():
        if p and fid not in by_id:
            by_id[fid] = p["spec"]
    for fid, fz in by_id.items():
        try:
            pos = st["pos"].get(fid)
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
            if pos is None and (go_l ^ go_s):
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
