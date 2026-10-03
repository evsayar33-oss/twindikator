"""v3 FİNALİST SEÇİMİ — adaylar çakışmasız backtest + sağlamlık kapılarından geçer.

Akış
  1) Aday toplama: FINAL_SEEDS + her varlık × ZD için IS t-istatistiğine göre ilk FINAL_TOPK (yalnızca IS bilgisi).
  2) Çakışmasız backtest (strateji başına aynı anda tek pozisyon, gerçek çıkış zamanı).
  3) Kapılar (hepsi geçilmeli):
       K1 OOS: n ≥ GATE_OOS_N, beklenti > 0, p < GATE_OOS_P, alfa > 0 (aynı çıkışla rastgele girişe göre)
       K2 Tüm dönem: n ≥ GATE_FULL_N, beklenti > 0
       K3 Maliyet ×GATE_COST_MULT: tüm dönem beklentisi > 0
       K4 Komşu parametreler: en az GATE_NEIGHBOR_POS oranında pozitif
       K5 Yıllar: (≥5 işlemli) yılların en az GATE_YEARS_POS oranı pozitif
       K6 Veri şüphesi yok (beklenti ≤ SUSPECT_EXP, isabet ≤ SUSPECT_WR)
  4) Geçenler tüm dönem t-istatistiğine göre sıralanır; varlık başına FINAL_PER_ASSET, toplam FINAL_MAX,
     aynı varlık × ZD × aile tekrarına izin verilmez.
"""
from __future__ import annotations

import math
import re
import time
from contextlib import contextmanager

import numpy as np
import pandas as pd

from . import config as C
from . import evaluate as EV
from . import exits as X

TF_MIN = {"5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240}
SC_TR = {"both": "iki yön", "long": "yalnız LONG", "short": "yalnız SHORT"}


# ───────────────────────── yardımcılar ─────────────────────────
@contextmanager
def overrides(ov: dict | None):
    """config parametrelerini geçici olarak değiştir (komşu parametre testi). Her durumda geri yükler."""
    ov = {k: v for k, v in (ov or {}).items() if not k.startswith("_")}
    old = {k: getattr(C, k) for k in ov}
    try:
        for k, v in ov.items():
            setattr(C, k, v)
        yield
    finally:
        for k, v in old.items():
            setattr(C, k, v)


def _ov_key(ov: dict | None) -> str:
    return "|".join(f"{k}={ov[k]}" for k in sorted(ov or {}) if not k.startswith("_")) or "base"


def family_of(entry: str) -> str:
    return entry.split(" · ", 1)[0]


def trade_stats(R: np.ndarray) -> dict:
    R = np.asarray(R, float)
    R = R[np.isfinite(R)]
    n = len(R)
    if n == 0:
        return {"n": 0, "exp": np.nan, "wr": np.nan, "pf": np.nan, "t": np.nan, "p": 1.0, "sd": np.nan}
    m = float(R.mean())
    sd = float(R.std(ddof=1)) if n > 1 else 0.0
    t = m / (sd / math.sqrt(n)) if sd > 0 else (np.inf if m > 0 else -np.inf)
    p = 0.5 * math.erfc(t / math.sqrt(2)) if np.isfinite(t) else (0.0 if t > 0 else 1.0)
    pos, neg = R[R > 0].sum(), -R[R < 0].sum()
    return {"n": n, "exp": m, "wr": float((R > 0).mean()), "pf": float(pos / neg) if neg > 0 else np.inf, "t": float(t), "p": float(p), "sd": sd}


def max_dd_R(R: np.ndarray) -> float:
    if len(R) == 0:
        return np.nan
    eq = np.cumsum(R)
    return float((np.maximum.accumulate(np.r_[0.0, eq])[1:] - eq).max())


# ───────────────────────── veri bağlamı ─────────────────────────
class DataCtx:
    """Bir varlık × ZD için veri ve önbellekli giriş defterleri."""

    def __init__(self, asset: str, tf: str, df: pd.DataFrame, partner: pd.Series | None, pname: str, funding):
        self.asset, self.tf, self.df = asset, tf, df
        self.partner, self.pname, self.funding = partner, pname, funding
        self.split = int(len(df) * C.IS_FRACTION)
        self.cost = C.ASSETS[asset]["cost_bps"]
        self.tf_delta = pd.Timedelta(minutes=TF_MIN[tf])
        self._books: dict = {}

    def book(self, family: str, ov: dict | None):
        fam_key = "ALL" if family == "META" else family
        key = (_ov_key(ov), fam_key)
        if key not in self._books:
            with overrides(ov):
                ctx = EV.build_context(self.df, self.cost, TF_MIN[self.tf], self.partner, self.pname, self.funding,
                                       self.split, families=None if family == "META" else (family,), all_exits=False)
            self._books[key] = (ctx["f"], ctx["book"], ctx["meta"])
        return self._books[key]


def run_spec(dc: DataCtx, entry: str, exit_cfg: dict, scope: str, ov: dict | None = None, cost_mult: float = 1.0) -> dict | None:
    """Çakışmasız backtest. Dönen: işlemler + OOS alfa için taban beklenti."""
    family = family_of(entry)
    # yalnızca çıkışı etkileyen parametreler defteri yeniden kurdurmaz (META hariç: zaman bariyeri etiketi etkiler)
    book_ov = {k: v for k, v in (ov or {}).items() if not (k == "HORIZON" and family != "META")}
    f, book, meta_msg = dc.book(family, book_ov)
    if entry not in book.items:
        return None
    _, L, S = book.items[entry]
    with overrides(ov):
        sm = X.simulate(dc.df, f["atr"], dc.cost * cost_mult, exit_cfg)
    valid = sm["valid"]
    sides = []
    if scope in ("both", "long"):
        sides.append((1, L))
    if scope in ("both", "short"):
        sides.append((-1, S))
    ev = []
    for side, M in sides:
        for i in np.flatnonzero(M & valid):
            ev.append((int(i), side))
    ev.sort()
    # aynı barda iki yön birden → belirsiz, ikisi de atlanır
    from collections import Counter
    cnt = Counter(i for i, _ in ev)
    dup = {i for i, c_ in cnt.items() if c_ > 1}
    idx = dc.df.index
    rows, last_exit = [], -1
    for i, side in ev:
        if i in dup or i < last_exit:
            continue
        k = sm[(side, "k")][i]
        R = sm[side][i]
        if not (np.isfinite(k) and np.isfinite(R)):
            continue
        k = int(k)
        rows.append({"bar": i, "side": side, "R": float(R), "k": k, "entry_time": idx[i + 1],
                     "exit_time": idx[i + k] + dc.tf_delta, "oos": i >= dc.split})
        last_exit = i + k
    t = pd.DataFrame(rows, columns=["bar", "side", "R", "k", "entry_time", "exit_time", "oos"])
    # OOS alfa tabanı: aynı çıkışla OOS'taki tüm geçerli barlara rastgele giriş (işlemlerin yön karışımıyla ağırlıklı)
    oos_m = np.zeros(len(idx), bool)
    oos_m[dc.split:] = True
    base = {s: float(np.nanmean(sm[s][valid & oos_m])) if (valid & oos_m).any() else np.nan for s in (1, -1)}
    to = t[t["oos"]]
    if len(to):
        w_long = (to["side"] == 1).mean()
        base_exp = w_long * base[1] + (1 - w_long) * base[-1]
    else:
        base_exp = np.nan
    return {"trades": t, "base_oos_exp": base_exp, "meta": meta_msg}


# ───────────────────────── komşu parametreler ─────────────────────────
def neighbors(entry: str, exit_name: str) -> list[tuple[str, dict, str, dict]]:
    """(etiket, config override, eşlenmiş giriş adı, çıkış cfg) listesi."""
    fam = family_of(entry)
    base_cfg = dict(C.EXITS[exit_name])
    out = []

    def add(label, ov=None, name=None, cfg=None):
        out.append((label, ov or {}, name or entry, cfg or base_cfg))

    # ortak
    add("ATR 10", {"ATR_LEN": 10})
    add("ATR 20", {"ATR_LEN": 20})
    add("zaman bariyeri 36", {"HORIZON": 36})
    add("zaman bariyeri 72", {"HORIZON": 72})
    add("stop ×0.8", cfg={**base_cfg, "sl_atr": round(base_cfg["sl_atr"] * 0.8, 3)})
    add("stop ×1.25", cfg={**base_cfg, "sl_atr": round(base_cfg["sl_atr"] * 1.25, 3)})
    if base_cfg.get("tp") is not None:
        add("hedef −0.5R", cfg={**base_cfg, "tp": max(base_cfg["tp"] - 0.5, (base_cfg.get("tp1") or 0) + 0.5, 0.5)})
        add("hedef +0.5R", cfg={**base_cfg, "tp": base_cfg["tp"] + 0.5})
    if base_cfg.get("trail") is not None:
        add("iz −0.5 ATR", cfg={**base_cfg, "trail": base_cfg["trail"] - 0.5})
        add("iz +0.5 ATR", cfg={**base_cfg, "trail": base_cfg["trail"] + 0.5})
    if "EMA200" in entry:
        add("trend EMA 150", {"TREND_EMA": 150})
        add("trend EMA 250", {"TREND_EMA": 250})
    if "hacim şoku" in entry or "volatilite şoku" in entry:
        add("şok eşiği 1.25σ", {"SHOCK_Z": 1.25})
        add("şok eşiği 1.75σ", {"SHOCK_Z": 1.75})
    # aileye özel
    if fam == "DONCH":
        m = re.search(r"Donchian (\d+)", entry)
        if m:
            n0 = int(m.group(1))
            for n1 in (round(n0 * 0.75), round(n0 * 1.25)):
                add(f"Donchian {n1}", {"DONCHIAN": (n1,)}, entry.replace(f"Donchian {n0}", f"Donchian {n1}"))
    elif fam == "RSI2":
        m = re.search(r"RSI\(2\) (\d+)/(\d+)", entry)
        if m:
            lo = int(m.group(1))
            for lo1 in (max(2, lo - 3), lo + 3):
                add(f"RSI(2) {lo1}/{100 - lo1}", {"RSI2_LO": (lo1,)}, entry.replace(f"RSI(2) {lo}/{100 - lo}", f"RSI(2) {lo1}/{100 - lo1}"))
    elif fam in ("OSC", "REJIM"):
        for k, vals in (("RSI_LEN", (10, 21)), ("STOCH_LEN", (10, 21)), ("DYN_LEN", (200, 400)), ("ARM_BARS", (4, 8))):
            for v in vals:
                add(f"{k} {v}", {k: v})
        if fam == "REJIM":
            add("ER 14", {"ER_LEN": 14})
            add("ER 30", {"ER_LEN": 30})
    elif fam == "SQZ":
        for k, vals in (("BB_LEN", (15, 25)), ("SQZ_MIN", (4, 8)), ("KC_K", (1.25, 1.75))):
            for v in vals:
                add(f"{k} {v}", {k: v})
    elif fam == "MA":
        m = re.search(r"EMA (\d+)/(\d+)", entry)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            for f_ in (0.75, 1.25):
                a1, b1 = max(2, round(a * f_)), max(3, round(b * f_))
                add(f"EMA {a1}/{b1}", {"MA_PAIRS": ((a1, b1),)}, entry.replace(f"EMA {a}/{b}", f"EMA {a1}/{b1}"))
        m = re.search(r"momentumu (\d+) bar", entry)
        if m:
            n0 = int(m.group(1))
            for n1 in (round(n0 * 0.75), round(n0 * 1.25)):
                add(f"momentum {n1}", {"TSMOM": (n1,)}, entry.replace(f"momentumu {n0} bar", f"momentumu {n1} bar"))
    elif fam == "META":
        for keep in (0.25, 0.45):
            add(f"meta üst %{int(keep * 100)}", {"META_KEEP": keep}, entry.replace("üst %35", f"üst %{int(keep * 100)}"))
    return out


# ───────────────────────── kurallar (insan dili) ─────────────────────────
def rules_text(asset: str, tf: str, entry: str, exit_name: str, scope: str) -> str:
    fam = family_of(entry)
    body = entry.split(" · ", 1)[1] if " · " in entry else entry
    yon = {"both": "LONG ve SHORT", "long": "yalnızca LONG", "short": "yalnızca SHORT"}[scope]
    if fam == "DONCH":
        n = re.search(r"Donchian (\d+)", entry).group(1)
        g = f"Mum kapanışı önceki {n} mumun en yükseğinin üstündeyse LONG, en düşüğünün altındaysa SHORT (ilk kırılım)."
        if "EMA200" in entry:
            g += " Filtre: LONG için kapanış EMA200 üstünde, SHORT için altında."
        if "hacim şoku" in entry:
            g += " Filtre: son 2 mumda hacim, son 50 mumun medyanına göre ≥1.5σ (robust) yüksek."
        if "sıkışma" in entry:
            g += " Filtre: son 10 mum içinde Bollinger genişliği 200 mumluk dağılımın alt %20'sinde."
    elif fam == "RSI2":
        m = re.search(r"RSI\(2\) (\d+)/(\d+)", entry)
        g = f"RSI(2) {m.group(1)} altına inerse LONG, {m.group(2)} üstüne çıkarsa SHORT (kesişim mumu)."
        if "EMA200" in entry:
            g += " Filtre: LONG için kapanış EMA200 üstünde, SHORT için altında."
    elif fam == "SQZ":
        g = "Bollinger(20,2) en az 6 mum Keltner(20,1.5) içinde kaldıktan sonra dışarı çıktığı mumda: kapanış orta bandın üstündeyse LONG, altındaysa SHORT."
        if "hacim" in entry:
            g += " Filtre: son 3 mumda hacim şoku."
    elif fam == "MA":
        g = f"{body}: hızlı ortalama yavaşı yukarı keserse LONG, aşağı keserse SHORT." if "EMA" in body else f"{body}: N mumluk getiri sıfırı yukarı keserse LONG, aşağı keserse SHORT."
    elif fam == "META":
        g = "Gradient boosting meta-modeli tüm aday sinyallerden başarı olasılığı en yüksek %35'lik dilimi seçer. Bu strateji yalnızca Telegram sinyaliyle izlenebilir (TradingView'da çizilemez)."
    elif fam in ("OSC", "REJIM"):
        g = f"{body}. Osilatörler (RSI14 / Stoch14 / WaveTrend) dinamik ya da sabit eşik bölgesine girip çıktığında sinyal; REJIM ailesinde verimlilik oranına göre yatay/trend filtresi uygulanır."
    else:
        g = body
    if " + " in entry:
        extra = {"günlük trend": f"günlük grafikte önceki gün kapanışı EMA{C.HTF_EMA} üstünde (SHORT: altında)",
                 f"ADX≥{C.ADX_MIN}": f"ADX(14) ≥ {C.ADX_MIN}", "önceden sıkışma": "son 10 mumda Bollinger genişliği alt %25'te",
                 "güçlü mum": f"sinyal mumunun gövdesi aralığının ≥%{int(C.BODY_MIN * 100)}'i ve yönle aynı",
                 "seans": f"sinyal mumu UTC {C.SESSION_UTC[0]:02d}:00–{C.SESSION_UTC[1]:02d}:00 arasında başlar", "hacim": "son 2 mumda hacim şoku"}
        for k_, v_ in extra.items():
            if entry.endswith(" + " + k_):
                g += f" Ek filtre: {v_}."
    cfg = C.EXITS[exit_name]
    e = [f"Giriş: sinyal mumunun kapanışından sonraki mumun açılışında.", f"Stop: giriş ∓ {cfg['sl_atr']} × ATR(14) (sinyal mumundaki ATR)."]
    if cfg.get("tp1") is not None:
        e.append(f"+{cfg['tp1']}R'de " + (f"pozisyonun %{int(cfg['part'] * 100)}'i kapatılır ve " if cfg.get("part") else "") + "stop girişe çekilir.")
    if cfg.get("tp") is not None:
        e.append(f"Hedef: +{cfg['tp']}R.")
    if cfg.get("fail") is not None:
        e.append(f"İlk {cfg['fail']} mum içinde kapanış sinyal mumunun dibinin altına (SHORT: tepesinin üstüne) dönerse kapanıştan çık.")
    if cfg.get("trail") is not None:
        e.append(f"İz süren stop: ulaşılan en uç fiyattan {cfg['trail']} × ATR" + (" (TP1 sonrası)." if cfg.get("trail_mode") == "be" else " (girişten itibaren)."))
    e.append(f"{C.HORIZON} mum sonra hâlâ açıksa kapanış fiyatından kapatılır.")
    return f"**{asset} {tf} · {yon}** — {g} " + " ".join(e)


# ───────────────────────── aday toplama + kapılar ─────────────────────────
def collect_candidates(research: dict) -> list[dict]:
    """research: {(asset, tf): sonuç tablosu}. Yalnızca IS bilgisi + tohumlar."""
    cands, seen = [], set()
    for s in C.FINAL_SEEDS:
        key = (s["asset"], s["tf"], s["entry"], s["exit"], s["scope"])
        if (s["asset"], s["tf"]) in research and key not in seen:
            seen.add(key)
            cands.append({**s, "source": "tohum"})
    for (asset, tf), res in research.items():
        rows = []
        for sc in EV.SCOPES:
            r = res[(res[f"{sc}_is_n"] >= C.MIN_TRADES_IS) & (res[f"{sc}_is_exp"] > 0) & ~EV.suspect(res, sc, "is")]
            if r.empty:
                continue
            se = (r[f"{sc}_is_exp"] - r[f"{sc}_is_lb"]) / 1.96
            t = r[f"{sc}_is_exp"] / se.replace(0, np.nan)
            for (_, row), tv in zip(r.iterrows(), t):
                if np.isfinite(tv) and tv >= C.FINAL_MIN_T_IS:
                    rows.append((tv, sc, row))
        rows.sort(key=lambda x: -x[0])
        used_entries = set()
        for tv, sc, row in rows:
            if row["entry"] in used_entries:
                continue
            key = (asset, tf, row["entry"], row["exit"], sc)
            if key in seen:
                continue
            used_entries.add(row["entry"])
            seen.add(key)
            cands.append({"asset": asset, "tf": tf, "entry": row["entry"], "exit": row["exit"], "scope": sc, "source": f"IS t={tv:.1f}"})
            if len(used_entries) >= C.FINAL_TOPK:
                break
    return cands


def year_table(t: pd.DataFrame) -> pd.DataFrame:
    if t.empty:
        return pd.DataFrame(columns=["n", "exp"])
    g = t.groupby(t["entry_time"].dt.year)["R"]
    return pd.DataFrame({"n": g.size(), "exp": g.mean(), "sum": g.sum()})


def evaluate_base(dc: DataCtx, cand: dict) -> dict:
    """Ucuz aşama: çakışmasız backtest + K1 ham, K2, K5, K6. (K1 nihai kararı çoklu test düzeltmesiyle run() içinde.)"""
    cfg = C.EXITS[cand["exit"]]
    out = {**cand, "family": family_of(cand["entry"]), "gates": {}, "passed": False, "error": None}
    r = run_spec(dc, cand["entry"], cfg, cand["scope"])
    if r is None:
        out["error"] = "giriş defterde yok"
        return out
    t = r["trades"]
    full, oos, ins = trade_stats(t["R"]), trade_stats(t.loc[t["oos"], "R"]), trade_stats(t.loc[~t["oos"], "R"])
    alpha = oos["exp"] - r["base_oos_exp"] if np.isfinite(r["base_oos_exp"]) else np.nan
    yt = year_table(t)
    yq = yt[yt["n"] >= 5]
    years_pos = float((yq["exp"] > 0).mean()) if len(yq) else np.nan
    years_span = max((t["entry_time"].max() - t["entry_time"].min()).days / 365.25, 0.1) if len(t) else np.nan
    out.update(trades=t, full=full, oos=oos, ins=ins, alpha=alpha, years=yt, years_pos=years_pos,
               per_year=len(t) / years_span if len(t) else 0.0, mdd_R=max_dd_R(t["R"].to_numpy()))
    out["k1_raw"] = bool(oos["n"] >= C.GATE_OOS_N and oos["exp"] > 0 and np.isfinite(alpha) and alpha > 0)
    g = out["gates"]
    g["K1 OOS"] = None
    g["K2 tüm dönem"] = bool(full["n"] >= C.GATE_FULL_N and full["exp"] > 0)
    g["K3 maliyet×2"] = None
    g["K4 komşular"] = None
    g["K5 yıllar"] = bool(np.isfinite(years_pos) and years_pos >= C.GATE_YEARS_POS)
    g["K6 veri"] = bool(full["exp"] <= C.SUSPECT_EXP and full["wr"] <= C.SUSPECT_WR)
    return out


def evaluate_robust(dc: DataCtx, out: dict, log=print) -> dict:
    """Pahalı aşama: maliyet ×2 ve komşu parametreler."""
    cfg = C.EXITS[out["exit"]]
    g = out["gates"]
    rc = run_spec(dc, out["entry"], cfg, out["scope"], cost_mult=C.GATE_COST_MULT)
    cost2 = trade_stats(rc["trades"]["R"]) if rc else {"exp": np.nan, "n": 0}
    out["cost2"] = cost2
    g["K3 maliyet×2"] = bool(np.isfinite(cost2["exp"]) and cost2["exp"] > 0)
    nb_rows = []
    for label, ov, name, ncfg in neighbors(out["entry"], out["exit"]):
        try:
            rn = run_spec(dc, name, ncfg, out["scope"], ov=ov)
        except Exception as ex:  # tek bir komşu hatası tüm adayı düşürmesin
            log(f"      komşu hata {label}: {ex}")
            rn = None
        if rn is None:
            nb_rows.append({"komşu": label, "n": 0, "exp": np.nan, "wr": np.nan})
            continue
        st = trade_stats(rn["trades"]["R"])
        nb_rows.append({"komşu": label, "n": st["n"], "exp": st["exp"], "wr": st["wr"]})
    nb = pd.DataFrame(nb_rows)
    out["neighbors"] = nb
    ok = nb[nb["n"] >= 20]
    nb_pos = float((ok["exp"] > 0).mean()) if len(ok) else np.nan
    out["neighbor_pos"] = nb_pos
    g["K4 komşular"] = bool(np.isfinite(nb_pos) and nb_pos >= C.GATE_NEIGHBOR_POS)
    out["passed"] = all(v is True for v in g.values())
    return out


def bh_pass(pvals: list[float], q: float) -> list[bool]:
    """Benjamini–Hochberg: yanlış keşif oranını q'da tutar (çok sayıda aday test edildiği için şans eseri geçenleri eler)."""
    m = len(pvals)
    if m == 0:
        return []
    order = np.argsort(pvals)
    thr_k = 0
    for rank, i in enumerate(order, 1):
        if pvals[i] <= rank / m * q:
            thr_k = rank
    passed = [False] * m
    for rank, i in enumerate(order, 1):
        passed[i] = rank <= thr_k
    return passed


def select(evals: list[dict]) -> list[dict]:
    ok = sorted([e for e in evals if e["passed"]], key=lambda e: -e["full"]["t"])
    sel, per_asset, used = [], {}, set()
    for e in ok:
        key = (e["asset"], e["tf"], e["family"])
        if key in used or per_asset.get(e["asset"], 0) >= C.FINAL_PER_ASSET:
            continue
        sel.append(e)
        used.add(key)
        per_asset[e["asset"]] = per_asset.get(e["asset"], 0) + 1
        if len(sel) >= C.FINAL_MAX:
            break
    for i, e in enumerate(sel, 1):
        e["is_final"] = True
        e["id"] = f"F{i}_{e['asset']}_{e['tf']}_{e['family']}"
        e["rules"] = rules_text(e["asset"], e["tf"], e["entry"], e["exit"], e["scope"])
    return sel


def run(ctxs: dict, research: dict, log=print) -> dict:
    """ctxs: {(asset, tf): DataCtx}. Dönen: {'evals', 'finalists', 'n_tested'}."""
    t0 = time.time()
    cands = collect_candidates(research)
    log(f"\n═══ FİNALİST AŞAMASI: {len(cands)} aday ═══")
    evals = []
    for c in cands:
        dc = ctxs.get((c["asset"], c["tf"]))
        if dc is None:
            continue
        try:
            e = evaluate_base(dc, c)
        except Exception as ex:
            e = {**c, "family": family_of(c["entry"]), "gates": {}, "passed": False, "k1_raw": False, "error": f"{type(ex).__name__}: {ex}"}
        evals.append(e)
    # K1: OOS beklenti > 0 testinin p-değerlerine tüm adaylar üzerinden Benjamini–Hochberg (q = GATE_OOS_P)
    pv = [e["oos"]["p"] if e.get("k1_raw") else 1.0 for e in evals]
    bh = bh_pass(pv, C.GATE_OOS_P)
    for e, ok in zip(evals, bh):
        if "gates" in e and e.get("error") is None:
            e["gates"]["K1 OOS"] = bool(e.get("k1_raw") and ok)
    for e in evals:
        g = e.get("gates", {})
        if e.get("error") is None and g.get("K1 OOS") and g.get("K2 tüm dönem") and g.get("K5 yıllar") and g.get("K6 veri"):
            t1 = time.time()
            try:
                evaluate_robust(ctxs[(e["asset"], e["tf"])], e, log)
            except Exception as ex:
                e["error"] = f"{type(ex).__name__}: {ex}"
            log(f"    sağlamlık {e['asset']} {e['tf']} {e['entry']} ({time.time() - t1:.0f}s)")
        gs = " ".join(("✓" if v else ("·" if v is None else "✗")) for v in g.values())
        log(f"  {e['asset']} {e['tf']} {e['entry']} | {e['exit']} | {e['scope']} → {gs} {'GEÇTİ' if e.get('passed') else ''} {e.get('error') or ''}")
    fin = select(evals)
    log(f"  finalist: {len(fin)} · süre {time.time() - t0:.0f}s")
    return {"evals": evals, "finalists": fin, "n_tested": len(evals)}


# ───────────────────────── rapor ─────────────────────────
def _r(x):
    return "—" if x is None or not np.isfinite(x) else f"{x:+.3f}R"


def _p(x):
    return "—" if x is None or not np.isfinite(x) else f"%{100 * x:.1f}"


def render(res: dict) -> list[str]:
    L = ["## Finalistler (v3) — çakışmasız backtest + sağlamlık kapıları", ""]
    L += ["Kapılar: **K1** OOS (n ≥ %d, beklenti > 0, alfa > 0, Benjamini–Hochberg yanlış keşif oranı ≤ %.2f — %d aday birlikte test edildi) · **K2** tüm dönem (n ≥ %d, beklenti > 0) · **K3** maliyet ×%.0f · "
          "**K4** komşu parametrelerin ≥ %%%d'i pozitif · **K5** yılların ≥ %%%d'i pozitif · **K6** veri şüphesi yok. "
          "Tümü çakışmasız: her strateji aynı anda tek pozisyon taşır. Not: tohum adaylar önceki raporun OOS sonuçlarından seçildi; "
          "onlar için OOS tam bağımsız değildir — asıl bağımsız sınav canlı kâğıt işlemdir." % (C.GATE_OOS_N, C.GATE_OOS_P, res.get("n_tested", 0), C.GATE_FULL_N, C.GATE_COST_MULT,
                                                                          int(C.GATE_NEIGHBOR_POS * 100), int(C.GATE_YEARS_POS * 100)), ""]
    fin = res["finalists"]
    if not fin:
        L += ["> **Hiçbir aday tüm kapıları geçemedi.** Canlı kâğıt işlem motoru sinyal üretmeyecek. Aşağıdaki aday tablosu hangi kapıda elendiklerini gösterir.", ""]
    else:
        L += ["| ID | Varlık | ZD | Yön | Giriş | Çıkış | Tüm dönem beklenti (n) | İsabet | PF | OOS beklenti (n) | OOS alfa | Maliyet×2 | Komşu + | Yıl + | İşlem/yıl | Maks. düşüş (R) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for e in fin:
            L.append(f"| **{e['id']}** | {e['asset']} | {e['tf']} | {SC_TR[e['scope']]} | {e['entry']} | {e['exit']} | {_r(e['full']['exp'])} ({e['full']['n']}) | "
                     f"{_p(e['full']['wr'])} | {e['full']['pf']:.2f} | {_r(e['oos']['exp'])} ({e['oos']['n']}) | {_r(e['alpha'])} | {_r(e['cost2']['exp'])} | "
                     f"{_p(e['neighbor_pos'])} | {_p(e['years_pos'])} | {e['per_year']:.1f} | {e['mdd_R']:.1f} |")
        L += ["", "### Kurallar (TradingView / manuel uygulama için)", ""]
        for e in fin:
            L += [f"- **{e['id']}** — {e['rules']}"]
        L += ["", "### Finalistlerin yıllık sonuçları (yıl ortalama R · işlem)", ""]
        yrs = sorted({y for e in fin for y in e["years"].index})
        L += ["| ID | " + " | ".join(str(y) for y in yrs) + " |", "|---|" + "---|" * len(yrs)]
        for e in fin:
            yt = e["years"]
            L.append(f"| {e['id']} | " + " | ".join((f"{yt.loc[y, 'exp']:+.2f} ({int(yt.loc[y, 'n'])})" if y in yt.index else "") for y in yrs) + " |")
        L += ["", "### Komşu parametre testleri", ""]
        for e in fin:
            nb = e["neighbors"]
            cells = " · ".join(f"{r['komşu']}: {_r(r['exp'])}" for _, r in nb.iterrows())
            L.append(f"- **{e['id']}**: {cells}")
    L += ["", "### Tüm adaylar ve kapı sonuçları", "",
          "| Varlık | ZD | Giriş | Çıkış | Yön | Kaynak | K1 | K2 | K3 | K4 | K5 | K6 | Tüm dönem | OOS | Not |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    sym = {True: "✓", False: "✗", None: "·"}
    for e in res["evals"]:
        g = e.get("gates", {})
        full = e.get("full", {})
        oos = e.get("oos", {})
        L.append(f"| {e['asset']} | {e['tf']} | {e['entry']} | {e['exit']} | {SC_TR[e['scope']]} | {e['source']} | "
                 + " | ".join(sym[g.get(k)] for k in ("K1 OOS", "K2 tüm dönem", "K3 maliyet×2", "K4 komşular", "K5 yıllar", "K6 veri"))
                 + f" | {_r(full.get('exp'))} ({full.get('n', 0)}) | {_r(oos.get('exp'))} ({oos.get('n', 0)}) | {e.get('error') or ('**FİNALİST**' if e.get('is_final') else '')} |")
    L.append("")
    return L


def to_json(fin: list[dict], risk: float | None) -> list[dict]:
    out = []
    for e in fin:
        out.append({
            "id": e["id"], "asset": e["asset"], "tf": e["tf"], "family": e["family"], "entry": e["entry"], "exit": e["exit"],
            "exit_cfg": C.EXITS[e["exit"]], "scope": e["scope"], "cost_bps": C.ASSETS[e["asset"]]["cost_bps"],
            "horizon": C.HORIZON, "risk_per_trade": risk if risk else C.LIVE_DEFAULT_RISK, "rules": e["rules"],
            "backtest": {"exp": e["full"]["exp"], "wr": e["full"]["wr"], "n": e["full"]["n"], "per_year": e["per_year"],
                         "oos_exp": e["oos"]["exp"], "oos_n": e["oos"]["n"], "alpha": e["alpha"]},
        })
    return out
