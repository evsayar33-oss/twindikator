"""ATVS Paneli — canlı bot kasası, işlemler, öz sermaye getirisi ve kıyaslama (altın, S&P 500, dolar...).

Veri kaynakları (hepsi ücretsiz):
  • Canlı veri : GitHub'daki "canli-veri" dalı (sunucu her saat gönderir: veri/kasa_log.csv, trader_trades.csv ...)
  • Backtest   : ana daldaki reports/ klasörü (portfoy_kasa.csv, finalist_islemler.csv.gz, finalists.json)
  • Kıyaslama  : yfinance günlük kapanışlar
  • Yatırımlar : (isteğe bağlı) ana daldaki yatirimlar.csv — tarih,tutar (otomatik transfer kaydını düzeltmek için)
"""
from __future__ import annotations

import io
import json
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(page_title="ATVS Panel", page_icon="📈", layout="wide")

# ───────────────────────── ayarlar ─────────────────────────
REPO = st.secrets.get("REPO", "evsayar33-oss/twindikator")
MAIN = st.secrets.get("MAIN_BRANCH", "main")
DATA = st.secrets.get("DATA_BRANCH", "canli-veri")
TOKEN = st.secrets.get("GH_TOKEN", "")          # repo private ise: yalnızca okuma yetkili token

# Varlık → (yfinance kodu, renk). Renk varlığa sabittir; seçim değişse de değişmez.
BENCH = {
    "Altın (XAU)":            ("GC=F", "#c98500"),
    "S&P 500":                ("^GSPC", "#d95926"),
    "Dolar endeksi (DXY)":    ("DX-Y.NYB", "#199e70"),
    "Dolar/TL (USD tutmak)":  ("TRY=X", "#9085e9"),
    "Bitcoin":                ("BTC-USD", "#d55181"),
    "Nasdaq 100":             ("^NDX", "#008300"),
}
C_STRAT, C_DD, C_FLOW = "#3987e5", "#e66767", "#898781"
LAYOUT = dict(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified",
              legend=dict(orientation="h", y=1.08, x=0), height=420,
              xaxis=dict(showgrid=False), yaxis=dict(gridcolor="rgba(137,135,129,0.18)"))


# ───────────────────────── veri ─────────────────────────
def _raw(branch: str, path: str) -> bytes | None:
    h = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    if TOKEN:   # private repo: API üzerinden ham içerik
        url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={branch}"
        h["Accept"] = "application/vnd.github.raw"
    else:
        url = f"https://raw.githubusercontent.com/{REPO}/{branch}/{path}"
    try:
        r = requests.get(url, headers=h, timeout=20)
        return r.content if r.status_code == 200 else None
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)
def load_live():
    out = {}
    b = _raw(DATA, "veri/kasa_log.csv")
    if b:
        k = pd.read_csv(io.BytesIO(b))
        k["time"] = pd.to_datetime(k["time"], utc=True)
        out["kasa"] = k.sort_values("time")
    b = _raw(DATA, "veri/trader_trades.csv")
    if b:
        t = pd.read_csv(io.BytesIO(b))
        for c in ("entry_time", "exit_time"):
            t[c] = pd.to_datetime(t[c], utc=True, errors="coerce")
        out["trades"] = t
    b = _raw(DATA, "veri/trader_state.json")
    if b:
        out["state"] = json.loads(b)
    for name in ("guncelleme.txt", "son_log.txt"):
        b = _raw(DATA, f"veri/{name}")
        if b:
            out[name] = b.decode("utf-8", "replace")
    b = _raw(MAIN, "yatirimlar.csv")
    if b:
        y = pd.read_csv(io.BytesIO(b))
        y.columns = [c.strip().lower() for c in y.columns]
        y["tarih"] = pd.to_datetime(y["tarih"], utc=True)
        out["yatirimlar"] = y
    return out


@st.cache_data(ttl=3600, show_spinner=False)
def load_backtest():
    out = {}
    b = _raw(MAIN, "reports/portfoy_kasa.csv")
    if b:
        k = pd.read_csv(io.BytesIO(b), index_col=0)
        k.index = pd.to_datetime(k.index, utc=True)
        out["kasa"] = k
    b = _raw(MAIN, "reports/finalist_islemler.csv.gz")
    if b:
        t = pd.read_csv(io.BytesIO(b), compression="gzip")
        for c in ("entry_time", "exit_time"):
            t[c] = pd.to_datetime(t[c], utc=True, errors="coerce")
        out["trades"] = t
    b = _raw(MAIN, "state/finalists.json") or _raw(MAIN, "reports/finalists.json")
    if b:
        out["fin"] = json.loads(b)
    return out


@st.cache_data(ttl=3600 * 6, show_spinner=False)
def load_bench(tickers: tuple, start: str) -> pd.DataFrame:
    import yfinance as yf
    frames = {}
    for tk in tickers:
        try:
            d = yf.download(tk, start=start, progress=False, auto_adjust=True)["Close"]
            d = d.iloc[:, 0] if isinstance(d, pd.DataFrame) else d
            d.index = pd.to_datetime(d.index).tz_localize(None)
            frames[tk] = d
        except Exception:
            pass
    return pd.DataFrame(frames)


# ───────────────────────── hesaplar ─────────────────────────
def daily_twr(k: pd.DataFrame, manual: pd.DataFrame | None) -> pd.DataFrame:
    """Zaman ağırlıklı getiri: para yatırma/çekme getiriyi bozmaz. r_t = (E_t − F_t) / E_{t−1} − 1."""
    d = k.set_index("time")
    eq = d["equity"].resample("1D").last().dropna()
    fl = d["flow"].resample("1D").sum().reindex(eq.index).fillna(0.0) if "flow" in d else eq * 0
    if manual is not None and len(manual):
        m = manual.set_index("tarih")["tutar"].resample("1D").sum()
        fl = m.reindex(eq.index).fillna(0.0)          # elle girilen yatırımlar otomatik kaydın yerine geçer
    prev = eq.shift(1)
    r = ((eq - fl) / prev - 1).fillna(0.0)
    r[(prev <= 0) | prev.isna()] = 0.0
    out = pd.DataFrame({"equity": eq, "flow": fl, "ret": r})
    out["net_yatirim"] = eq.iloc[0] + fl.cumsum() - fl.iloc[0]
    out["index"] = (1 + r).cumprod()
    out.index = out.index.tz_localize(None)
    return out


def stats(ret: pd.Series, ann: int = 365) -> dict:
    ret = ret.dropna()
    if len(ret) < 2:
        return {}
    idx = (1 + ret).cumprod()
    yrs = max((ret.index[-1] - ret.index[0]).days / 365.25, 1 / 365)
    tot = idx.iloc[-1] - 1
    cagr = idx.iloc[-1] ** (1 / yrs) - 1 if yrs >= 0.25 else np.nan
    vol = ret.std() * math.sqrt(ann)
    dn = ret[ret < 0].std() * math.sqrt(ann)
    mdd = (idx / idx.cummax() - 1).min()
    mu = ret.mean() * ann
    return {"Toplam getiri": tot, "Yıllık (CAGR)": cagr, "Oynaklık": vol,
            "Sharpe": mu / vol if vol > 0 else np.nan, "Sortino": mu / dn if dn and dn > 0 else np.nan,
            "Maks. düşüş": mdd, "Calmar": (cagr / -mdd) if mdd < 0 and not np.isnan(cagr) else np.nan}


def compare_table(strat: pd.Series, bench: pd.DataFrame, names: dict, ann: int) -> pd.DataFrame:
    rows = {"ATVS": stats(strat, ann)}
    for nm, tk in names.items():
        if tk not in bench:
            continue
        b = bench[tk].reindex(strat.index).ffill().pct_change().fillna(0.0)
        s = stats(b, ann)
        both = pd.concat([strat, b], axis=1).dropna()
        if len(both) > 5 and both.iloc[:, 1].std() > 0:
            s["Korelasyon (ATVS ile)"] = both.corr().iloc[0, 1]
            beta = both.cov().iloc[0, 1] / both.iloc[:, 1].var()
            s["ATVS betası"] = beta
            s["ATVS alfası (yıllık)"] = (both.iloc[:, 0].mean() - beta * both.iloc[:, 1].mean()) * ann
        rows[nm] = s
    return pd.DataFrame(rows).T


def fmt_table(df: pd.DataFrame) -> pd.DataFrame:
    pct = {"Toplam getiri", "Yıllık (CAGR)", "Oynaklık", "Maks. düşüş", "ATVS alfası (yıllık)"}
    out = df.copy().astype(object)
    for c in df.columns:
        out[c] = [("—" if pd.isna(v) else (f"{v:+.1%}" if c in pct else f"{v:.2f}")) for v in df[c]]
    return out


def rebased_chart(strat_idx: pd.Series, bench: pd.DataFrame, names: dict, title: str, log=False):
    fig = go.Figure()
    for nm, tk in names.items():
        if tk not in bench:
            continue
        b = bench[tk].reindex(strat_idx.index).ffill().dropna()
        if b.empty:
            continue
        fig.add_trace(go.Scatter(x=b.index, y=100 * b / b.iloc[0], name=nm, line=dict(width=1.6, color=BENCH[nm][1]),
                                 hovertemplate="%{y:.1f}"))
    fig.add_trace(go.Scatter(x=strat_idx.index, y=100 * strat_idx / strat_idx.iloc[0], name="ATVS",
                             line=dict(width=2.6, color=C_STRAT), hovertemplate="%{y:.1f}"))
    fig.add_hline(y=100, line=dict(color=C_FLOW, width=1, dash="dot"))
    fig.update_layout(**LAYOUT, title=title, yaxis_title="Başlangıç = 100")
    if log:
        fig.update_yaxes(type="log")
    return fig


def dd_chart(idx: pd.Series, title="Zirveden düşüş"):
    dd = idx / idx.cummax() - 1
    fig = go.Figure(go.Scatter(x=dd.index, y=dd * 100, fill="tozeroy", name="Düşüş",
                               line=dict(color=C_DD, width=1.5), hovertemplate="%{y:.1f}%"))
    fig.update_layout(**{**LAYOUT, "height": 260}, title=title, yaxis_title="%", showlegend=False)
    return fig


def monthly_table(ret: pd.Series) -> pd.DataFrame:
    m = (1 + ret).resample("ME").prod() - 1
    t = pd.DataFrame({"Yıl": m.index.year, "Ay": m.index.month, "r": m.values})
    p = t.pivot(index="Yıl", columns="Ay", values="r")
    ay = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
    p.columns = [ay[c - 1] for c in p.columns]
    p["Yıl"] = (1 + ret).groupby(ret.index.year).prod() - 1
    return p


def heat(p: pd.DataFrame):
    return p.style.format(lambda v: "" if pd.isna(v) else f"{v:+.1%}") \
        .background_gradient(cmap="RdYlGn", vmin=-0.08, vmax=0.08, axis=None)


def trade_stats(R: pd.Series) -> dict:
    R = R.dropna()
    if R.empty:
        return {}
    w, l = R[R > 0], R[R <= 0]
    return {"İşlem": len(R), "Kazanma oranı": len(w) / len(R), "Ortalama R": R.mean(),
            "Ort. kazanç R": w.mean() if len(w) else np.nan, "Ort. kayıp R": l.mean() if len(l) else np.nan,
            "Kâr faktörü": w.sum() / -l.sum() if l.sum() < 0 else np.nan,
            "Beklenti alt sınırı (%95)": R.mean() - 1.96 * R.std(ddof=1) / math.sqrt(len(R)) if len(R) > 1 else np.nan}


def kpi_row(items):
    cols = st.columns(len(items))
    for c, (lab, val, help_) in zip(cols, items):
        c.metric(lab, val, help=help_)


# ───────────────────────── arayüz ─────────────────────────
st.title("ATVS Panel")
live, bt = load_live(), load_backtest()

with st.sidebar:
    st.header("Kıyaslama")
    pick = st.multiselect("Karşılaştırılacak varlıklar", list(BENCH), default=["Altın (XAU)", "S&P 500", "Dolar/TL (USD tutmak)"])
    names = {n: BENCH[n][0] for n in pick}
    st.caption("ATVS kasası USDT cinsindendir. 'Dolar/TL' çizgisi, aynı parayı dolar olarak tutmanın TL bazındaki getirisidir.")
    if st.button("Veriyi yenile"):
        st.cache_data.clear()
        st.rerun()
    if "guncelleme.txt" in live:
        st.caption(f"Son canlı veri: {live['guncelleme.txt'].strip()} (UTC)")

tab_live, tab_trades, tab_bt, tab_log = st.tabs(["Canlı kasa", "İşlemler", "Backtest kıyası", "Bot günlüğü"])

# ── Canlı kasa
with tab_live:
    if "kasa" not in live or len(live["kasa"]) < 1:
        st.info("Henüz canlı veri yok. Sunucu kurulumunda GH_TOKEN satırı doldurulduğunda bot her saat veriyi "
                "'canli-veri' dalına gönderir ve bu sayfa kendiliğinden dolar. O zamana kadar **Backtest kıyası** sekmesine bakabilirsin.")
    else:
        d = daily_twr(live["kasa"], live.get("yatirimlar"))
        eq_now = float(live["kasa"]["equity"].iloc[-1])
        net_in = float(d["net_yatirim"].iloc[-1])
        s = stats(d["ret"]) if len(d) > 1 else {}
        tr = live.get("trades", pd.DataFrame())
        ts = trade_stats(tr["R"]) if "R" in tr else {}
        kpi_row([
            ("Kasa", f"{eq_now:,.2f} USDT", "Bitget vadeli cüzdan toplamı (açık pozisyonların anlık kâr/zararı dahil)"),
            ("Net kâr", f"{eq_now - net_in:+,.2f} USDT", "Kasa − (başlangıç + yatırılanlar − çekilenler)"),
            ("Öz sermaye getirisi", f"{s.get('Toplam getiri', 0):+.2%}", "Zaman ağırlıklı: para yatırma/çekme getiriyi etkilemez"),
            ("Maks. düşüş", f"{s.get('Maks. düşüş', 0):.2%}", "Zirveden en büyük düşüş"),
            ("İşlem / kazanma", f"{ts.get('İşlem', 0)} / {ts.get('Kazanma oranı', 0):.0%}" if ts else "0", None),
            ("Ortalama R", f"{ts.get('Ortalama R', float('nan')):+.2f}" if ts else "—", "1R = işleme girerken riske edilen tutar"),
        ])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d.index, y=d["net_yatirim"], name="Net yatırılan", line=dict(color=C_FLOW, width=1.5, dash="dot"),
                                 hovertemplate="%{y:,.2f}"))
        fig.add_trace(go.Scatter(x=d.index, y=d["equity"], name="Kasa", line=dict(color=C_STRAT, width=2.4), hovertemplate="%{y:,.2f}"))
        fig.update_layout(**LAYOUT, title="Kasa büyümesi (USDT)", yaxis_title="USDT")
        st.plotly_chart(fig, use_container_width=True)

        if len(d) > 2:
            bench = load_bench(tuple(names.values()), str((d.index[0] - pd.Timedelta(days=7)).date()))
            st.plotly_chart(rebased_chart(d["index"], bench, names, "Öz sermaye getirisi ve kıyaslama"), use_container_width=True)
            c1, c2 = st.columns([3, 2])
            c1.plotly_chart(dd_chart(d["index"]), use_container_width=True)
            with c2:
                st.markdown("**Aylık getiri**")
                st.dataframe(heat(monthly_table(d["ret"])), use_container_width=True)
            st.markdown("**Kıyaslama tablosu** (aynı dönem)")
            st.dataframe(fmt_table(compare_table(d["ret"], bench, names, 365)), use_container_width=True)
            if len(d) < 90:
                st.caption("90 günden kısa dönemde yıllık oranlar (CAGR, Sharpe) anlamlı değildir; birkaç ay sonra yorumla.")

        # canlı karne: canlı R ortalaması backtest beklentisiyle uyumlu mu?
        if ts and "trades" in bt:
            st.markdown("**Canlı karne** — canlı sonuçlar backtest beklentisinin içinde mi?")
            rows = []
            for fid, g in tr.groupby("id"):
                b = bt["trades"][bt["trades"]["id"] == fid]["R"]
                if "R" not in g or b.empty:
                    continue
                n, m = g["R"].notna().sum(), g["R"].mean()
                band = 1.96 * b.std() / math.sqrt(max(n, 1))
                ok = abs(m - b.mean()) <= band if n else None
                rows.append({"Strateji": fid, "Canlı işlem": n, "Canlı ort. R": m, "Backtest ort. R": b.mean(),
                             "Beklenen aralık": f"{b.mean() - band:+.2f} … {b.mean() + band:+.2f}",
                             "Durum": "✅ uyumlu" if ok else ("⚠️ sapma — izle" if n >= 10 else "ℹ️ az işlem")})
            if rows:
                st.dataframe(pd.DataFrame(rows).round(3), use_container_width=True, hide_index=True)

        if "state" in live:
            opn = {k: v for k, v in live["state"].get("pos", {}).items() if v}
            st.markdown(f"**Açık pozisyonlar:** {len(opn)}")
            if opn:
                st.dataframe(pd.DataFrame([{"Strateji": k, "Sembol": v["symbol"], "Yön": "LONG" if v["side"] == 1 else "SHORT",
                                            "Miktar": v["qty"], "Giriş": v["entry"], "Stop": v["stop"],
                                            "Stop girişte": "evet" if v.get("be") else "hayır", "Giriş zamanı": v["entry_time"]}
                                           for k, v in opn.items()]), use_container_width=True, hide_index=True)

# ── İşlemler
with tab_trades:
    tr = live.get("trades")
    if tr is None or tr.empty:
        st.info("Henüz kapanmış canlı işlem yok.")
    else:
        ts = trade_stats(tr["R"]) if "R" in tr else {}
        if ts:
            kpi_row([(k, (f"{v:.0%}" if k == "Kazanma oranı" else (f"{v:+.2f}" if isinstance(v, float) else str(v))), None)
                     for k, v in ts.items()])
        if "pnl_usdt" in tr:
            t2 = tr.sort_values("exit_time")
            fig = go.Figure(go.Bar(x=t2["exit_time"], y=t2["pnl_usdt"], name="İşlem kâr/zararı",
                                   marker_color=[C_STRAT if v > 0 else C_DD for v in t2["pnl_usdt"].fillna(0)],
                                   hovertemplate="%{y:+.2f} USDT"))
            fig.add_trace(go.Scatter(x=t2["exit_time"], y=t2["pnl_usdt"].fillna(0).cumsum(), name="Birikimli",
                                     line=dict(color="#ffffff", width=1.8), hovertemplate="%{y:+.2f} USDT"))
            fig.update_layout(**LAYOUT, title="İşlem bazında kâr/zarar (USDT)")
            st.plotly_chart(fig, use_container_width=True)
        show = tr.copy()
        show["Yön"] = show["side"].map({1: "LONG", -1: "SHORT"})
        cols = [c for c in ["id", "symbol", "Yön", "entry_time", "entry", "exit_time", "exit", "qty", "risk_usdt",
                            "pnl_usdt", "R", "fee", "reason"] if c in show]
        st.dataframe(show[cols].sort_values("exit_time", ascending=False).round(4), use_container_width=True, hide_index=True)
        st.download_button("İşlemleri indir (CSV)", tr.to_csv(index=False).encode(), "atvs_islemler.csv", "text/csv")

# ── Backtest kıyası
with tab_bt:
    if "kasa" not in bt:
        st.info("reports/portfoy_kasa.csv bulunamadı.")
    else:
        k = bt["kasa"]
        risk_cols = [c for c in k.columns if c.startswith("risk_")]
        rc = st.selectbox("Risk seviyesi", risk_cols, index=risk_cols.index("risk_%1") if "risk_%1" in risk_cols else 0)
        eq = k[rc].copy()
        eq.index = eq.index.tz_localize(None)
        eq = eq.resample("1D").last().ffill()
        r = eq.pct_change().fillna(0.0)
        st.caption("İki finalist (XAU + ETH) birlikte, olay tabanlı portföy simülasyonu; maliyetler dahil. "
                   "Geçmiş sonuçtur, geleceği garanti etmez. Yalnızca XAU çalışırken getiri bundan düşük olur.")
        bench = load_bench(tuple(names.values()), str(eq.index[0].date()))
        st.plotly_chart(rebased_chart(eq, bench, names, f"Backtest öz sermaye ({rc.replace('risk_', 'risk ')}) ve kıyaslama", log=True),
                        use_container_width=True)
        st.plotly_chart(dd_chart(eq, "Backtest zirveden düşüş"), use_container_width=True)
        st.markdown("**Kıyaslama tablosu**")
        st.dataframe(fmt_table(compare_table(r, bench, names, 365)), use_container_width=True)
        yr = (1 + r).groupby(r.index.year).prod() - 1
        ytab = pd.DataFrame({"ATVS": yr})
        for nm, tk in names.items():
            if tk in bench:
                bb = bench[tk].reindex(eq.index).ffill()
                ytab[nm] = bb.groupby(bb.index.year).last() / bb.groupby(bb.index.year).first() - 1
        st.markdown("**Yıllık getiriler**")
        st.dataframe(ytab.style.format(lambda v: "" if pd.isna(v) else f"{v:+.1%}")
                     .background_gradient(cmap="RdYlGn", vmin=-0.3, vmax=0.3, axis=None), use_container_width=True)
        if "trades" in bt:
            st.markdown("**Strateji bazında backtest işlem istatistikleri**")
            rows = {fid: trade_stats(g["R"]) for fid, g in bt["trades"].groupby("id")}
            tb = pd.DataFrame(rows).T
            st.dataframe(tb.style.format({c: ("{:.0%}" if c == "Kazanma oranı" else ("{:.0f}" if c == "İşlem" else "{:+.3f}"))
                                          for c in tb.columns}), use_container_width=True)

# ── Bot günlüğü
with tab_log:
    if "son_log.txt" in live:
        st.code(live["son_log.txt"][-15000:], language="text")
    else:
        st.info("Günlük henüz gönderilmedi.")
