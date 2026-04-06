import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ── MUST be first Streamlit call ──────────────────────────────
st.set_page_config(
    page_title="StockSense",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #070d17 !important;
    color: #c8dff0 !important;
    font-family: 'Syne', sans-serif !important;
}
.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1100px !important;
}
#MainMenu, footer, header, .stDeployButton,
div[data-testid="stDecoration"] { display: none !important; }

.app-title {
    font-size: 2.4rem; font-weight: 800; color: #fff;
    letter-spacing: -0.02em; line-height: 1; margin-bottom: 0.2rem;
}
.app-title span { color: #00d4ff; }
.app-subtitle {
    font-family: 'Space Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: #3a6080; margin-bottom: 1.8rem;
}

.stTextInput > div > div > input {
    background: #0d1a2a !important; border: 1.5px solid #1a3050 !important;
    color: #00d4ff !important; font-family: 'Space Mono', monospace !important;
    font-size: 1rem !important; border-radius: 8px !important; padding: 0.6rem 1rem !important;
    letter-spacing: 0.08em !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important; box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}
.stTextInput label {
    color: #5a7a9a !important; font-size: 0.7rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}
.stSelectbox > div > div {
    background: #0d1a2a !important; border: 1.5px solid #1a3050 !important;
    border-radius: 8px !important; color: #c8dff0 !important;
}
.stSelectbox label {
    color: #5a7a9a !important; font-size: 0.7rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    font-family: 'Space Mono', monospace !important;
}
.stButton > button {
    background: #00d4ff !important; color: #070d17 !important;
    border: none !important; font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important; font-size: 0.75rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    padding: 0.65rem 2rem !important; border-radius: 8px !important;
    width: 100% !important; margin-top: 1.4rem !important; transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

[data-testid="metric-container"] {
    background: #0d1a2a !important; border: 1px solid #1a3050 !important;
    border-radius: 10px !important; padding: 1rem 1.2rem !important;
}
[data-testid="metric-container"] label {
    color: #3a6080 !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00d4ff !important; font-family: 'Space Mono', monospace !important;
    font-size: 1.2rem !important; font-weight: 700 !important;
}

.signal-box { border-radius: 12px; padding: 1.5rem 2rem; text-align: center; margin: 1rem 0; }
.signal-box.green  { background: rgba(0,255,136,0.07);  border: 1.5px solid #00ff88; }
.signal-box.yellow { background: rgba(255,214,10,0.07); border: 1.5px solid #ffd60a; }
.signal-box.red    { background: rgba(255,69,96,0.07);  border: 1.5px solid #ff4560; }
.signal-box.grey   { background: rgba(90,122,154,0.07); border: 1.5px solid #3a6080; }
.signal-verdict { font-size: 1.8rem; font-weight: 800; letter-spacing: -0.01em; margin-bottom: 0.3rem; }
.signal-box.green  .signal-verdict { color: #00ff88; }
.signal-box.yellow .signal-verdict { color: #ffd60a; }
.signal-box.red    .signal-verdict { color: #ff4560; }
.signal-box.grey   .signal-verdict { color: #5a7a9a; }
.signal-reason { font-family: 'Space Mono', monospace; font-size: 0.68rem; color: #5a7a9a; }

.sec-head {
    font-family: 'Space Mono', monospace; font-size: 0.6rem;
    letter-spacing: 0.22em; text-transform: uppercase; color: #3a6080;
    border-bottom: 1px solid #1a3050; padding-bottom: 0.5rem; margin: 1.8rem 0 1rem;
}
.company-name { font-size: 1.5rem; font-weight: 800; color: #fff; }
.company-ticker { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: #00d4ff; margin-left: 0.5rem; }
.price-big { font-family: 'Space Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #fff; }
.price-pos { color: #00ff88; font-size: 0.9rem; font-family: 'Space Mono', monospace; }
.price-neg { color: #ff4560; font-size: 0.9rem; font-family: 'Space Mono', monospace; }

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important; border-bottom: 1px solid #1a3050 !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #3a6080 !important;
    font-family: 'Space Mono', monospace !important; font-size: 0.65rem !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    border: none !important; padding: 0.6rem 1.2rem !important;
}
.stTabs [aria-selected="true"] { color: #00d4ff !important; border-bottom: 2px solid #00d4ff !important; }

.score-row { margin-bottom: 0.9rem; }
.score-label {
    display: flex; justify-content: space-between;
    font-family: 'Space Mono', monospace; font-size: 0.62rem;
    color: #c8dff0; margin-bottom: 0.3rem; letter-spacing: 0.04em;
}
.score-track { height: 5px; background: #1a3050; border-radius: 3px; overflow: hidden; }
.score-fill  { height: 100%; border-radius: 3px; }

hr { border-color: #1a3050 !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def safe(val, fmt="{:.2f}", fallback="N/A"):
    try:
        if val is None or (isinstance(val, float) and val != val):
            return fallback
        return fmt.format(float(val))
    except:
        return fallback

def get_signal(eps_g, roe, de, pe):
    try:
        if eps_g >= 15 and roe >= 18 and de <= 1:
            return ("STRONG BUY", "🟢", "green",  "Excellent fundamentals at a fair valuation.") if pe <= 20 \
              else ("BUY · PRICEY", "🟡", "yellow", "Great fundamentals but valuation is stretched.")
        if eps_g >= 10 and roe >= 15 and de <= 1.5:
            return "BUY", "🟡", "yellow", "Solid metrics. Monitor P/E before entering."
        if de > 2:
            return "AVOID", "🔴", "red", "High leverage is a significant risk factor."
        return "HOLD", "⚪", "grey", "Mixed signals — wait for clearer catalysts."
    except:
        return "HOLD", "⚪", "grey", "Could not compute signal."

def bar_color(p):
    return "#00ff88" if p >= 65 else "#ffd60a" if p >= 35 else "#ff4560"

def clamp(v, lo, hi):
    try: return max(0, min(100, int((float(v) - lo) / (hi - lo) * 100)))
    except: return 0

def score_bar(label, val_str, pct, color):
    return f"""<div class="score-row">
        <div class="score-label"><span>{label}</span><span>{val_str}</span></div>
        <div class="score-track"><div class="score-fill" style="width:{pct}%;background:{color};"></div></div>
    </div>"""


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-title">Stock<span>Sense</span></div>
<div class="app-subtitle">Fundamental Analysis · Live Data via yFinance · Instant Signal</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([3, 1.5, 1])
with c1:
    ticker_input = st.text_input("Stock Ticker", placeholder="e.g. RELIANCE.NS  /  TCS.NS  /  AAPL")
with c2:
    period = st.selectbox("Chart Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
with c3:
    run = st.button("Analyse →")

st.caption("💡 Indian stocks: add `.NS` (NSE) or `.BO` (BSE) — e.g. `INFY.NS`, `HDFCBANK.NS`")


# ── Main ───────────────────────────────────────────────────────────────────────
if run and ticker_input.strip():
    ticker_str = ticker_input.strip().upper()

    with st.spinner(f"Fetching {ticker_str} from Yahoo Finance…"):
        try:
            stock = yf.Ticker(ticker_str)
            info  = stock.info
            hist  = stock.history(period=period)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    if hist.empty:
        st.error(f"No price data found for **{ticker_str}**. Check the symbol and try again.")
        st.stop()

    # ── Extract ──────────────────────────────────────────────────────────────
    name          = info.get("longName") or info.get("shortName") or ticker_str
    currency      = info.get("currency", "")
    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or float(hist["Close"].iloc[-1])
    prev_close    = info.get("previousClose") or (float(hist["Close"].iloc[-2]) if len(hist) > 1 else current_price)
    price_chg     = current_price - prev_close
    price_chg_pct = (price_chg / prev_close * 100) if prev_close else 0

    market_cap    = info.get("marketCap")
    pe_ratio      = float(info.get("trailingPE") or info.get("forwardPE") or 0)
    pb_ratio      = float(info.get("priceToBook") or 0)
    roe_raw       = float(info.get("returnOnEquity") or 0)
    roe           = roe_raw * 100
    eps           = float(info.get("trailingEps") or 0)
    eps_g_raw     = float(info.get("earningsGrowth") or info.get("revenueGrowth") or 0)
    eps_g         = eps_g_raw * 100
    de_raw        = float(info.get("debtToEquity") or 0)
    de            = de_raw / 100 if de_raw > 10 else de_raw  # normalise yfinance inconsistency
    div_yield     = float(info.get("dividendYield") or 0)
    beta          = float(info.get("beta") or 0)
    w52h          = float(info.get("fiftyTwoWeekHigh") or 0)
    w52l          = float(info.get("fiftyTwoWeekLow") or 0)
    sector        = info.get("sector") or "—"
    industry      = info.get("industry") or "—"

    curr_sym = "₹" if any(x in ticker_str for x in [".NS", ".BO"]) else "$"
    if market_cap:
        mc_str = f"{curr_sym}{market_cap/1e12:.2f}T" if market_cap >= 1e12 else \
                 f"{curr_sym}{market_cap/1e9:.2f}B"  if market_cap >= 1e9  else \
                 f"{curr_sym}{market_cap/1e6:.0f}M"
    else:
        mc_str = "N/A"

    # ── Company Header ────────────────────────────────────────────────────────
    st.markdown("---")
    hc1, hc2 = st.columns([2, 1])
    with hc1:
        st.markdown(f"""
        <div class="company-name">{name}<span class="company-ticker">{ticker_str}</span></div>
        <div style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#3a6080;margin-top:0.3rem;">
            {sector} · {industry}
        </div>""", unsafe_allow_html=True)
    with hc2:
        chg_cls = "price-pos" if price_chg >= 0 else "price-neg"
        sym     = "▲" if price_chg >= 0 else "▼"
        st.markdown(f"""
        <div style="text-align:right">
            <div class="price-big">{curr_sym}{current_price:,.2f}</div>
            <div class="{chg_cls}">{sym} {abs(price_chg):.2f} ({abs(price_chg_pct):.2f}%)</div>
        </div>""", unsafe_allow_html=True)

    # ── Signal ────────────────────────────────────────────────────────────────
    res = get_signal(eps_g, roe, de, pe_ratio)
    verdict, emoji, css_cls, reason = res if len(res) == 4 else res
    st.markdown(f"""
    <div class="signal-box {css_cls}">
        <div class="signal-verdict">{emoji} {verdict}</div>
        <div class="signal-reason">{reason}</div>
    </div>""", unsafe_allow_html=True)

    # ── Key Metrics ───────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Key Metrics</div>', unsafe_allow_html=True)
    cols = st.columns(6)
    vals = [
        ("P/E Ratio",   safe(pe_ratio, "{:.1f}")),
        ("ROE",         safe(roe, "{:.1f}") + "%"),
        ("Debt/Equity", safe(de, "{:.2f}")),
        ("EPS",         f"{curr_sym}{safe(eps, '{:.2f}')}"),
        ("Mkt Cap",     mc_str),
        ("Beta",        safe(beta, "{:.2f}")),
    ]
    for col, (label, val) in zip(cols, vals):
        col.metric(label, val)

    cols2 = st.columns(6)
    vals2 = [
        ("P/B Ratio",   safe(pb_ratio, "{:.2f}")),
        ("Div Yield",   safe(div_yield*100, "{:.2f}") + "%"),
        ("52W High",    f"{curr_sym}{safe(w52h, '{:,.2f}')}"),
        ("52W Low",     f"{curr_sym}{safe(w52l, '{:,.2f}')}"),
        ("EPS Growth",  safe(eps_g, "{:.1f}") + "%"),
        ("Currency",    currency),
    ]
    for col, (label, val) in zip(cols2, vals2):
        col.metric(label, val)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Charts & Analysis</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📈  Price & Volume", "🕯  Candlestick + BB", "📊  Scorecard"])

    CHART_THEME = dict(
        plot_bgcolor="#0a1828", paper_bgcolor="#070d17",
        font=dict(family="Space Mono", color="#5a7a9a", size=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="x unified", height=480,
    )
    XAXIS = dict(showgrid=False, zeroline=False, showspikes=True,
                 spikecolor="#1a3050", spikethickness=1)
    YAXIS = dict(gridcolor="#0f1f30", zeroline=False, tickprefix=curr_sym)

    # Tab 1 – Price + Volume + MAs
    with tab1:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.75, 0.25], vertical_spacing=0.04)
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"], mode="lines",
            line=dict(color="#00d4ff", width=2),
            fill="tozeroy", fillcolor="rgba(0,212,255,0.07)", name="Price",
        ), row=1, col=1)
        if len(hist) >= 20:
            fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(20).mean(),
                mode="lines", line=dict(color="#ffd60a", width=1.2, dash="dot"), name="MA20"), row=1, col=1)
        if len(hist) >= 50:
            fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"].rolling(50).mean(),
                mode="lines", line=dict(color="#ff4560", width=1.2, dash="dot"), name="MA50"), row=1, col=1)
        v_colors = ["#00ff88" if c >= o else "#ff4560"
                    for c, o in zip(hist["Close"], hist["Open"])]
        fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"],
            marker_color=v_colors, opacity=0.6, name="Volume"), row=2, col=1)
        fig.update_layout(**CHART_THEME,
            xaxis=XAXIS, yaxis=YAXIS,
            xaxis2=dict(showgrid=False), yaxis2=dict(gridcolor="#0f1f30", zeroline=False))
        st.plotly_chart(fig, use_container_width=True)

    # Tab 2 – Candlestick + Bollinger Bands
    with tab2:
        cd = hist.tail(120)
        fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             row_heights=[0.75, 0.25], vertical_spacing=0.04)
        fig2.add_trace(go.Candlestick(
            x=cd.index, open=cd["Open"], high=cd["High"], low=cd["Low"], close=cd["Close"],
            increasing_line_color="#00ff88", decreasing_line_color="#ff4560",
            increasing_fillcolor="#00ff88", decreasing_fillcolor="#ff4560", name="OHLC",
        ), row=1, col=1)
        if len(cd) >= 20:
            mid   = cd["Close"].rolling(20).mean()
            std   = cd["Close"].rolling(20).std()
            upper = mid + 2 * std
            lower = mid - 2 * std
            fig2.add_trace(go.Scatter(x=cd.index, y=upper,
                line=dict(color="rgba(255,214,10,0.5)", width=1, dash="dot"), name="BB Upper"), row=1, col=1)
            fig2.add_trace(go.Scatter(x=cd.index, y=lower,
                line=dict(color="rgba(255,214,10,0.5)", width=1, dash="dot"), name="BB Lower",
                fill="tonexty", fillcolor="rgba(255,214,10,0.04)"), row=1, col=1)
        vc2 = ["#00ff88" if c >= o else "#ff4560" for c, o in zip(cd["Close"], cd["Open"])]
        fig2.add_trace(go.Bar(x=cd.index, y=cd["Volume"],
            marker_color=vc2, opacity=0.55, name="Volume"), row=2, col=1)
        fig2.update_layout(**CHART_THEME,
            xaxis=dict(showgrid=False, zeroline=False, rangeslider=dict(visible=False)),
            yaxis=YAXIS,
            xaxis2=dict(showgrid=False), yaxis2=dict(gridcolor="#0f1f30", zeroline=False))
        st.plotly_chart(fig2, use_container_width=True)

    # Tab 3 – Scorecard
    with tab3:
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("**Metric Scorecard**")
            bars = [
                ("EPS Growth",            f"{eps_g:.1f}%",       clamp(eps_g, 0, 30),            ),
                ("Return on Equity",       f"{roe:.1f}%",         clamp(roe, 0, 30),              ),
                ("Debt/Equity (↓ better)", f"{de:.2f}",           clamp(3 - de, 0, 3),            ),
                ("P/E (↓ = cheaper)",      f"{pe_ratio:.1f}",     clamp(50 - pe_ratio, 0, 50),    ),
                ("P/B (↓ = cheaper)",      f"{pb_ratio:.2f}",     clamp(10 - pb_ratio, 0, 10),    ),
            ]
            html = "".join(score_bar(l, v, p, bar_color(p)) for l, v, p in bars)
            st.markdown(html, unsafe_allow_html=True)

        with sc2:
            if w52h and w52l and current_price:
                rng_pct = int((current_price - w52l) / (w52h - w52l) * 100) if w52h != w52l else 50
                st.markdown("**52-Week Range**")
                st.markdown(f"""
                <div style="background:#0d1a2a;border:1px solid #1a3050;border-radius:10px;padding:1.2rem;margin-bottom:1rem;">
                    <div style="display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:0.62rem;color:#3a6080;margin-bottom:0.5rem;">
                        <span>52W Low<br>{curr_sym}{w52l:,.2f}</span>
                        <span style="text-align:center;">Now<br><span style="color:#fff;">{curr_sym}{current_price:,.2f}</span></span>
                        <span style="text-align:right;">52W High<br>{curr_sym}{w52h:,.2f}</span>
                    </div>
                    <div style="height:6px;background:#1a3050;border-radius:3px;overflow:hidden;">
                        <div style="width:{rng_pct}%;height:100%;background:linear-gradient(90deg,#ff4560,#ffd60a,#00ff88);border-radius:3px;"></div>
                    </div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.6rem;color:#3a6080;text-align:center;margin-top:0.4rem;">
                        {rng_pct}% from 52-week low
                    </div>
                </div>""", unsafe_allow_html=True)

            signal_color = {"green": "#00ff88", "yellow": "#ffd60a", "red": "#ff4560", "grey": "#5a7a9a"}.get(css_cls, "#5a7a9a")
            st.markdown("**Signal Summary**")
            st.markdown(f"""
            <div style="background:#0d1a2a;border:1px solid #1a3050;border-radius:10px;padding:1.2rem;font-family:'Space Mono',monospace;font-size:0.65rem;line-height:2.2;">
                <span style="color:#3a6080;">TICKER</span>&nbsp;&nbsp;<span style="color:#00d4ff;">{ticker_str}</span><br>
                <span style="color:#3a6080;">SECTOR</span>&nbsp;&nbsp;<span style="color:#c8dff0;">{sector}</span><br>
                <span style="color:#3a6080;">SIGNAL</span>&nbsp;&nbsp;<span style="color:{signal_color};">{emoji} {verdict}</span><br>
                <span style="color:#3a6080;">NOTE</span>&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#c8dff0;">{reason}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:0.58rem;color:#1a3050;text-align:center;margin-top:2rem;">
        Data via Yahoo Finance · For educational purposes only · Not financial advice
    </div>""", unsafe_allow_html=True)

elif run:
    st.warning("Please enter a ticker symbol first.")
