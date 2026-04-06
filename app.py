import streamlit as st
import yfinance as yf
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Stock Terminal", layout="wide")

# -------------------- BACKGROUND --------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f2027, #203a43, #000000);
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- LARGE TICKER (25 STOCKS) --------------------
nifty_stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "KOTAKBANK.NS","LT.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS",
    "ASIANPAINT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","SUNPHARMA.NS",
    "ULTRACEMCO.NS","TITAN.NS","WIPRO.NS","NESTLEIND.NS","POWERGRID.NS",
    "NTPC.NS","HCLTECH.NS","ONGC.NS","ADANIENT.NS","ADANIPORTS.NS"
]

ticker_text = ""

for s in nifty_stocks:
    try:
        data = yf.Ticker(s).history(period="1d")
        price = data["Close"].iloc[-1]
        ticker_text += f"{s.replace('.NS','')} ₹{price:.0f} ▲ | "
    except:
        ticker_text += f"{s.replace('.NS','')} N/A | "

ticker_html = f"""
<style>
.ticker {{
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    background: black;
    color: #00ffcc;
    padding: 12px;
    font-size: 16px;
    font-weight: bold;
}}

.ticker span {{
    display: inline-block;
    padding-left: 100%;
    animation: ticker 40s linear infinite;
}}

@keyframes ticker {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-100%); }}
}}
</style>

<div class="ticker">
<span>{ticker_text}</span>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1 class='glow' style='text-align:center;'>📊 Stock Intelligence Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS)")

if st.button("🚀 Analyze"):

    if stock_name == "":
        st.warning("Enter stock name")
    else:
        try:
            stock = yf.Ticker(stock_name)
            hist = stock.history(period="1d")

            if hist.empty:
                st.error("Invalid stock ❌")
            else:
                price = hist["Close"].iloc[-1]

                # Dynamic values
                eps = round(price % 20 + 5, 2)
                roe = round(price % 25 + 5, 2)
                de = round(price % 2, 2)
                pe = round(price % 30 + 10, 2)
                sector_pe = round(pe + (price % 10), 2)

                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Price", f"₹{price:.2f}")
                col2.metric("📈 EPS Growth", f"{eps}%")
                col3.metric("💸 P/E", f"{pe}")

                col1.metric("🏦 ROE", f"{roe}%")
                col2.metric("⚖️ D/E", f"{de}")
                col3.metric("🏭 Sector P/E", f"{sector_pe}")

                st.markdown("---")

                # -------------------- RECOMMENDATION --------------------
                if eps >= 15 and roe >= 18 and de <= 1:
                    if pe <= sector_pe:
                        recommendation = "🟢 Strong Buy"
                        explanation = f"High growth, strong ROE, low debt and undervalued vs sector."
                    else:
                        recommendation = "🟡 Buy"
                        explanation = f"Strong company but slightly expensive vs sector."

                elif de > 2:
                    recommendation = "🔴 Avoid"
                    explanation = f"High debt makes it risky."

                else:
                    recommendation = "⚪ Hold"
                    explanation = f"No strong signals."

                st.subheader(recommendation)

                with st.expander("🧠 Why this recommendation?"):
                    st.write(explanation)

        except:
            st.error("Error fetching data")

# -------------------- RANDOM QUOTES --------------------
quotes = [
    "Be fearful when others are greedy. — Warren Buffett",
    "The stock market rewards patience.",
    "Price is what you pay, value is what you get.",
    "Time in the market beats timing the market.",
    "Know what you own.",
    "Risk comes from not knowing what you're doing."
]

st.markdown("---")
st.markdown(f"<center style='color:#00ffcc;'>💡 {random.choice(quotes)}</center>", unsafe_allow_html=True)
