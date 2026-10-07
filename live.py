"""ATVS canlı KÂĞIT İŞLEM motoru (GitHub Actions'ta saatlik çalışır).

• Finalistleri state/finalists.json'dan okur (araştırma iş akışı üretir).
• Veriyi araştırmayla AYNI kaynak, doğrulama ve sinyal kodundan geçirir (lab.evaluate.build_context).
• Her finalist aynı anda tek pozisyon; giriş = sinyal mumundan sonraki mumun açılışı; çıkış kuralları
  lab.exits.simulate_one ile — backtest'teki vektörize simülatörle birebir aynı (selftest doğrular).
• Kaçırılan çalıştırmalar için son LIVE_CATCHUP_BARS mum geriye dönük işlenir.
• Telegram: yeni sinyal, giriş gerçekleşti, TP1 (stop girişe), iz süren stop güncellemesi, kapanış, haftalık karne.
  Gizli değişkenler: TELEGRAM_TOKEN (veya TELEGRAM_BOT_TOKEN) ve TELEGRAM_CHAT_ID. Yoksa mesajlar yalnızca loga yazılır.
Durum dosyaları (iş akışı depoya geri yazar): state/positions.json, state/ledger.csv, state/last_run.txt
"""
from __future__ import annotations

import html
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import requests

from lab import config as C
from lab import data as D
from lab import evaluate as EV
from lab import exits as X

TF_MIN = {"5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": 1440}
DEC = {"XAU": 2, "XAG": 3, "BTC": 1, "ETH": 2, "NQ": 1, "SPX": 1}
SIDE_TR = {1: "LONG 🟢", -1: "SHORT 🔴"}
STATE = C.LIVE_STATE_DIR
POS_FILE = os.path.join(STATE, "positions.json")
LEDGER = os.path.join(STATE, "ledger.csv")
FIN_FILE = os.path.join(STATE, "finalists.json")
LEDGER_COLS = ["id", "asset", "tf", "side", "signal_time", "entry_time", "entry", "exit_time", "reason", "R", "backtest_exp"]
DRY = os.getenv("ATVS_DRY", "") == "1"


# ───────────────────────── yardımcılar ─────────────────────────
def now_utc() -> pd.Timestamp:
    t = os.getenv("ATVS_NOW")                       # test için sabit zaman
    return pd.Timestamp(t, tz="UTC") if t else pd.Timestamp.now(tz="UTC")


def px(asset: str, x) -> str:
    return "—" if x is None or not np.isfinite(x) else f"{x:,.{DEC.get(asset, 2)}f}"


def load_json(path: str, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: str, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, default=str)
    os.replace(tmp, path)


SENT: list[str] = []


def tg(text: str):
    """Telegram mesajı (HTML). Başarısız olursa iş akışını durdurmaz."""
    SENT.append(text)
    print("\n── TELEGRAM ──\n" + text + "\n──────────────")
    token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if DRY or not token or not chat:
        return
    for k in range(3):
        try:
            r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                              data={"chat_id": chat, "text": text[:4000], "parse_mode": "HTML", "disable_web_page_preview": "true"}, timeout=20)
            if r.status_code == 200:
                return
            if r.status_code == 429:
                time.sleep(int(r.json().get("parameters", {}).get("retry_after", 5)) + 1)
                continue
            print(f"telegram hata {r.status_code}: {r.text[:200]}")
            return
        except requests.RequestException as ex:
            print(f"telegram ağ hatası: {ex}")
            time.sleep(3)


def append_ledger(row: dict):
    os.makedirs(STATE, exist_ok=True)
    new = not os.path.exists(LEDGER)
    pd.DataFrame([row], columns=LEDGER_COLS).to_csv(LEDGER, mode="a", header=new, index=False)


# ───────────────────────── veri ─────────────────────────
_BASES: dict = {}


def base_1h(asset: str) -> pd.DataFrame:
    if asset not in _BASES:
        raw, _ = D.load(asset, "1h", refresh=True)
        df, rep = D.validate(asset, "1h", raw)
        _BASES[asset] = df
    return _BASES[asset]


def frame(asset: str, tf: str) -> pd.DataFrame:
    """Yalnızca TAMAMEN kapanmış mumlar: (1) henüz bitmemiş saatlik mum atılır, (2) üst ZD mumu ancak içindeki
    son saatlik mum da veride varsa alınır (geciken veri yüzünden eksik 4h mumu işlenmez)."""
    base = base_1h(asset)
    if base.empty:
        return base
    now = now_utc()
    base = base[base.index + pd.Timedelta(hours=1) <= now]
    if base.empty:
        return base
    df = base if tf == "1h" else D.resample(base, C.TIMEFRAMES[tf]["rule"])
    end = df.index + pd.Timedelta(minutes=TF_MIN[tf])
    return df[(end <= now) & (end <= base.index[-1] + pd.Timedelta(hours=1))]


def build(asset: str, tf: str, family: str) -> dict:
    df = frame(asset, tf)
    if len(df) < C.DYN_LEN * 3:
        raise RuntimeError(f"{asset} {tf}: yetersiz veri ({len(df)} mum)")
    if family != "META":
        df = df.iloc[-C.LIVE_BARS:]                  # göstergeler için yeterli ısınma; META tüm geçmişle eğitilir
    partner = None
    pa = C.PARTNER.get(asset)
    if pa and any(f in (C.FOCUS_FAMILIES or ()) for f in ("PAIR", "LEADLAG")) and family in ("PAIR", "LEADLAG", "META"):
        pb = frame(pa, tf)
        partner = pb["close"] if len(pb) else None
    ctx = EV.build_context(df, C.ASSETS[asset]["cost_bps"], TF_MIN[tf], partner, pa or "", None, split=len(df),
                           families=None if family == "META" else (family,), all_exits=False)
    ctx["df"] = df
    return ctx


# ───────────────────────── mesajlar ─────────────────────────
def msg_signal(fz: dict, pos: dict, df: pd.DataFrame, i: int, late: bool) -> str:
    a, cfg = fz["asset"], fz["exit_cfg"]
    side, atr = pos["side"], pos["atr"]
    ref = float(df["close"].iloc[i])
    risk = cfg["sl_atr"] * atr
    lines = [f"<b>{'⏰ GECİKMELİ ' if late else ''}YENİ SİNYAL — {a} {fz['tf']} {SIDE_TR[side]}</b>",
             f"Strateji: {html.escape(fz['id'])} · {html.escape(fz['entry'])} · {html.escape(fz['exit'])}",
             f"Sinyal mumu: {pd.Timestamp(pos['signal_time']):%Y-%m-%d %H:%M} UTC · kapanış {px(a, ref)}",
             "Giriş: bir sonraki mumun açılışı" + (" (gerçekleşmiş olabilir — aşağıdaki seviyeleri kendi giriş fiyatına göre uygula)" if late else f" (≈ {px(a, ref)})"),
             f"Stop: {px(a, ref - side * risk)}  (mesafe {px(a, risk)} = {cfg['sl_atr']}×ATR)"]
    if cfg.get("tp1") is not None:
        lines.append(f"TP1: {px(a, ref + side * cfg['tp1'] * risk)} (+{cfg['tp1']}R) → " + (f"%{int(cfg['part'] * 100)} kapat, " if cfg.get("part") else "") + "stop girişe")
    if cfg.get("tp") is not None:
        lines.append(f"Hedef: {px(a, ref + side * cfg['tp'] * risk)} (+{cfg['tp']}R)")
    if cfg.get("trail") is not None:
        lines.append(f"İz süren stop: en uç fiyattan {cfg['trail']}×ATR = {px(a, cfg['trail'] * atr)}" + (" (TP1 sonrası)" if cfg.get("trail_mode") == "be" else ""))
    lines.append(f"Zaman çıkışı: {fz.get('horizon', C.HORIZON)} mum")
    rk = fz.get("risk_per_trade", C.LIVE_DEFAULT_RISK)
    lines.append(f"Risk: kasanın %{100 * rk:.2g}'i → miktar = kasa × {rk:g} ÷ {px(a, risk)}")
    bt = fz.get("backtest", {})
    if bt:
        lines.append(f"Backtest: işlem başına {bt.get('exp', 0):+.2f}R · isabet %{100 * bt.get('wr', 0):.0f} · yılda ~{bt.get('per_year', 0):.0f} işlem")
    lines.append("<i>Kâğıt işlem / ileri test — yatırım tavsiyesi değildir.</i>")
    return "\n".join(lines)


def msg_entry(fz: dict, pos: dict, r: dict) -> str:
    a, cfg, side = fz["asset"], fz["exit_cfg"], pos["side"]
    risk = cfg["sl_atr"] * pos["atr"]
    e = r["entry"]
    s = [f"📍 <b>GİRİŞ GERÇEKLEŞTİ — {a} {fz['tf']} {SIDE_TR[side]}</b> @ {px(a, e)}", f"Stop: {px(a, e - side * risk)}"]
    if r.get("tp1_px") is not None:
        s.append(f"TP1: {px(a, r['tp1_px'])}")
    if r.get("tp_px") is not None:
        s.append(f"Hedef: {px(a, r['tp_px'])}")
    return "\n".join(s)


# ───────────────────────── çekirdek ─────────────────────────
def process(fz: dict, ctx: dict, state: dict) -> None:
    fid = fz["id"]
    df, book, f = ctx["df"], ctx["book"], ctx["f"]
    if fz["entry"] not in book.items:
        raise RuntimeError(f"giriş defterde yok: {fz['entry']} (meta: {ctx.get('meta')})")
    _, L, S = book.items[fz["entry"]]
    if fz["scope"] == "long":
        S = np.zeros_like(S)
    elif fz["scope"] == "short":
        L = np.zeros_like(L)
    o, h, l, c = (df[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    atr = f["atr"].to_numpy(float)
    idx = df.index
    n = len(df)
    cfg, cost = fz["exit_cfg"], fz["cost_bps"]
    H = int(fz.get("horizon", C.HORIZON))
    last = state["last_bar"].get(fid)
    if last is None:
        new = [n - 1]                                 # ilk çalıştırma: geçmiş sinyaller için mesaj yağmuru yok
    else:
        lt = pd.Timestamp(last)
        new = [j for j in range(max(0, n - C.LIVE_CATCHUP_BARS), n) if idx[j] > lt]
    pos = state["positions"].get(fid)

    def update(pos, j):
        """Pozisyonu bar j'ye kadar ilerlet; yeni olaylar için mesaj gönder. Kapanırsa None döner."""
        try:
            i = idx.get_loc(pd.Timestamp(pos["signal_time"]))
        except KeyError:
            tg(f"⚠️ {fid}: açık pozisyonun sinyal mumu veride bulunamadı ({pos['signal_time']}). Pozisyon takipten çıkarıldı.")
            return None
        r = X.simulate_one(o[: j + 1], h[: j + 1], l[: j + 1], c[: j + 1], pos["atr"], i, pos["side"], cfg, cost, H,
                           C.fund_bps_bar(TF_MIN[fz["tf"]]))
        if r["entry"] is not None and "entry" not in pos["sent"]:
            pos["entry"] = r["entry"]
            pos["entry_time"] = str(idx[i + 1])
            pos["sent"].append("entry")
            tg(msg_entry(fz, pos, r))
        if r.get("tp1_k") is not None and "tp1" not in pos["sent"]:
            pos["sent"].append("tp1")
            tg(f"🔒 <b>TP1 (+{cfg['tp1']}R) — {fz['asset']} {fz['tf']} {SIDE_TR[pos['side']]}</b>\n"
               + (f"Pozisyonun %{int(cfg['part'] * 100)}'ini kapat. " if cfg.get("part") else "")
               + f"Stopu girişe çek: {px(fz['asset'], pos['entry'])}")
        if r["status"] == "open" and cfg.get("trail") is not None and r.get("stop") is not None:
            prev = pos.get("last_stop")
            if prev is None or abs(r["stop"] - prev) >= 0.5 * pos["atr"]:
                if prev is not None:
                    tg(f"↗️ İz süren stop güncellendi — {fz['asset']} {fz['tf']} {SIDE_TR[pos['side']]}: yeni stop {px(fz['asset'], r['stop'])}")
                pos["last_stop"] = r["stop"]
        if r["status"] == "closed":
            exit_time = idx[i + r["exit_k"]] + pd.Timedelta(minutes=TF_MIN[fz["tf"]])
            tg(f"{'✅' if r['R'] > 0 else '❌'} <b>KAPANDI — {fz['asset']} {fz['tf']} {SIDE_TR[pos['side']]}</b>\n"
               f"Sebep: {r.get('reason')} · Sonuç: <b>{r['R']:+.2f}R</b> (maliyet dahil)\n"
               f"Giriş {px(fz['asset'], pos.get('entry'))} · {exit_time:%Y-%m-%d %H:%M} UTC")
            append_ledger({"id": fid, "asset": fz["asset"], "tf": fz["tf"], "side": pos["side"], "signal_time": pos["signal_time"],
                           "entry_time": pos.get("entry_time"), "entry": pos.get("entry"), "exit_time": str(exit_time), "reason": r.get("reason"),
                           "R": round(r["R"], 4), "backtest_exp": fz.get("backtest", {}).get("exp")})
            return None
        return pos

    for j in new:
        if pos is not None:
            pos = update(pos, j)
        if pos is None and (L[j] or S[j]) and not (L[j] and S[j]):
            side = 1 if L[j] else -1
            pos = {"id": fid, "asset": fz["asset"], "tf": fz["tf"], "side": side, "signal_time": str(idx[j]),
                   "atr": float(atr[j]), "entry": None, "sent": ["signal"], "last_stop": None, "spec": fz}
            tg(msg_signal(fz, pos, df, j, late=(j < n - 1)))   # gecikmeliyse sonraki mumlarda döngü pozisyonu ilerletir
    state["positions"][fid] = pos
    state["last_bar"][fid] = str(idx[n - 1])


def weekly(state: dict, fins: list[dict]):
    t = now_utc()
    key = f"{t.isocalendar().year}-W{t.isocalendar().week:02d}"
    if t.weekday() != 0 or t.hour < 6 or state.get("weekly") == key:
        return
    state["weekly"] = key
    lines = [f"<b>📊 Haftalık karne — {key}</b>"]
    if os.path.exists(LEDGER):
        lg = pd.read_csv(LEDGER)
        for fz in fins:
            g = lg[lg["id"] == fz["id"]]
            bt = fz.get("backtest", {}).get("exp", np.nan)
            if len(g):
                lines.append(f"{fz['id']}: {len(g)} işlem · ort. {g['R'].mean():+.2f}R (backtest {bt:+.2f}R) · toplam {g['R'].sum():+.1f}R")
            else:
                lines.append(f"{fz['id']}: henüz kapanan işlem yok (backtest {bt:+.2f}R)")
        if len(lg):
            last7 = lg[pd.to_datetime(lg["exit_time"], utc=True) >= t - pd.Timedelta(days=7)]
            lines.append(f"<b>Toplam:</b> {len(lg)} işlem · {lg['R'].sum():+.1f}R · son 7 gün {last7['R'].sum():+.1f}R ({len(last7)} işlem)")
    else:
        lines.append("Henüz kapanan işlem yok.")
    op = [p for p in state["positions"].values() if p]
    lines.append(f"Açık pozisyon: {len(op)}" + ("" if not op else " — " + ", ".join(f"{p['asset']} {p['tf']} {SIDE_TR[p['side']]}" for p in op)))
    tg("\n".join(lines))


def main() -> int:
    t0 = time.time()
    meta = load_json(FIN_FILE, {})
    fins = meta.get("finalistler", [])
    state = load_json(POS_FILE, {"positions": {}, "last_bar": {}, "errors": "", "weekly": None})
    state.setdefault("positions", {})
    state.setdefault("last_bar", {})
    # finalist listesinden çıkmış ama açık pozisyonu olan stratejiler kapanana kadar yönetilmeye devam eder
    by_id = {f["id"]: f for f in fins}
    for fid, p in state["positions"].items():
        if p and fid not in by_id:
            by_id[fid] = p["spec"]
    if not by_id:
        print("Finalist yok — canlı motor beklemede.")
        save_json(POS_FILE, state)
        return 0
    # hızlı çıkış: hiçbir finalistin zaman diliminde son işlemden beri yeni mum kapanmadıysa veri indirme
    now = now_utc()
    due = []
    for fid, fz in by_id.items():
        step = pd.Timedelta(minutes=TF_MIN[fz["tf"]])
        latest_closed = (now - step).floor(step)
        last = state["last_bar"].get(fid)
        if last is None or pd.Timestamp(last) < latest_closed:
            due.append(fid)
    if not due and os.getenv("ATVS_FORCE", "") != "1":
        print(f"Yeni kapanmış mum yok ({now:%Y-%m-%d %H:%M} UTC) — çıkılıyor.")
        return 0
    errors = []
    ctx_cache: dict = {}
    for fid, fz in by_id.items():
        key = (fz["asset"], fz["tf"], fz["family"])
        try:
            if key not in ctx_cache:
                ctx_cache[key] = build(*key)
            process(fz, ctx_cache[key], state)
        except Exception as ex:
            errors.append(f"{fid}: {type(ex).__name__}: {ex}")
            print(traceback.format_exc())
    try:
        weekly(state, fins)
    except Exception as ex:
        errors.append(f"haftalık: {ex}")
    err_txt = "\n".join(errors)
    if err_txt and err_txt != state.get("errors"):
        tg("⚠️ <b>ATVS canlı motor hatası</b>\n" + html.escape(err_txt[:3000]))
    state["errors"] = err_txt
    save_json(POS_FILE, state)
    with open(os.path.join(STATE, "last_run.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"{now_utc():%Y-%m-%d %H:%M} UTC · {len(by_id)} strateji · {len(SENT)} mesaj · {len(errors)} hata · {time.time() - t0:.0f}s\n")
    print(f"bitti: {len(SENT)} mesaj, {len(errors)} hata, {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
