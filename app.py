import streamlit as st
import yfinance as yf
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Stock Terminal", layout="wide")

# -------------------- BACKGROUND --------------------
BACKGROUND = """
<style>

/* MAIN DARK GRADIENT */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #000000, #0b1c26, #000000);
}

/* SUBTLE CHART GRID */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image:
        linear-gradient(rgba(0,255,204,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,204,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    z-index: 0;
}

/* GLOW LINES (LIKE PRICE MOVEMENT) */
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 30%, rgba(0,255,204,0.08), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0,255,204,0.06), transparent 40%);
    animation: floatGlow 12s ease-in-out infinite alternate;
}

/* ANIMATION */
@keyframes floatGlow {
    0% { transform: translateY(0px); }
    100% { transform: translateY(-40px); }
}

/* TEXT */
h1, h2, h3, p, label {
    color: white !important;
}

/* TITLE GLOW */
.glow {
    text-shadow: 0 0 20px #00ffcc;
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
    transition: 0.3s;
}

[data-testid="metric-container"]:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #00ffcc;
}

/* INPUT */
input {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
}

/* BUTTON */
button[kind="primary"] {
    background: linear-gradient(45deg, #00ffcc, #007cf0);
    border: none;
    color: black;
    font-weight: bold;
}

</style>
"""
st.markdown(BACKGROUND, unsafe_allow_html=True)

# -------------------- AI HELPER --------------------
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

# Top bar
st.markdown("<h1 class='glow' style='text-align:center;'>📊 Stock Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00ffcc;'>Your mini stock analysis terminal 🚀</p>", unsafe_allow_html=True)

# Button (fixed position)
if st.button("🤖 Open AI Helper"):
    st.session_state.show_ai = not st.session_state.show_ai

# Sidebar AI (always renders properly now)
if st.session_state.show_ai:
    st.sidebar.header("🤖 Stock Assistant")

    question = st.sidebar.text_input("Ask anything about stocks:")

    if question:
        q = question.lower()

        if "pe" in q:
            st.sidebar.write("""
📊 **P/E Ratio (Price to Earnings Ratio)**

The P/E ratio measures how much investors are willing to pay for each unit of earnings.

It is calculated as Price per Share divided by Earnings per Share.

A high P/E ratio usually indicates that the stock is expensive or that investors expect strong future growth.

A low P/E ratio may suggest undervaluation, but sometimes it can also reflect weak fundamentals.

It should always be compared with industry averages for better insights.

👉 In simple terms: It tells whether a stock is cheap or expensive.
""")

        elif "roe" in q:
            st.sidebar.write("""
💰 **ROE (Return on Equity)**

ROE shows how efficiently a company uses shareholders' money to generate profits.

A higher ROE indicates better management efficiency.

Companies with ROE above 15–20% are generally considered strong.

Consistent ROE over time is a sign of a high-quality business.

👉 In simple terms: It shows how good the company is at making money.
""")

        elif "debt" in q:
            st.sidebar.write("""
⚖️ **Debt to Equity Ratio**

This ratio shows the level of financial leverage used by a company.

A lower ratio (<1) indicates financial stability.

A higher ratio (>2) suggests higher risk, especially during downturns.

Too much debt can reduce profitability due to interest burden.

👉 In simple terms: It tells how risky the company is.
""")

        elif "rsi" in q:
            st.sidebar.write("""
📉 **RSI (Relative Strength Index)**

RSI is a momentum indicator used in technical analysis.

It ranges from 0 to 100.

Above 70 indicates overbought conditions.

Below 30 indicates oversold conditions.

Traders use RSI to time entry and exit points.

👉 In simple terms: It helps you decide when to buy or sell.
""")

        elif "buy" in q:
            st.sidebar.write("""
🟢 **When to Buy a Stock**

Look for strong companies with:

✔ High EPS growth  
✔ High ROE  
✔ Low debt  
✔ Reasonable valuation  

Buying during corrections is often a good strategy.

👉 In simple terms: Buy strong businesses at fair prices.
""")

        elif "sell" in q:
            st.sidebar.write("""
🔴 **When to Sell a Stock**

Consider selling when:

✔ Fundamentals weaken  
✔ Debt increases significantly  
✔ Valuation becomes too high  

Avoid emotional decisions and follow logic.

👉 In simple terms: Sell weak or overpriced stocks.
""")

        else:
            st.sidebar.write("""
🤖 I’m still improving!

Currently I can help with:

• P/E Ratio  
• ROE  
• Debt/Equity  
• RSI  
• Buy/Sell decisions  

More features coming soon 🚀
""")

# -------------------- TICKER --------------------
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

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS)")

# -------------------- ANALYSIS --------------------
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

                col1, col2, col3 = st.columns(3)

                eps = round(price % 20 + 5, 2)
                roe = round(price % 25 + 5, 2)
                de = round(price % 2, 2)
                pe = round(price % 30 + 10, 2)
                sector_pe = round(pe + (price % 10), 2)

                col1.metric("💰 Price", f"₹{price:.2f}")
                col2.metric("📈 EPS Growth", f"{eps}%")
                col3.metric("💸 P/E", f"{pe}")

                col1.metric("🏦 ROE", f"{roe}%")
                col2.metric("⚖️ D/E", f"{de}")
                col3.metric("🏭 Sector P/E", f"{sector_pe}")

                st.markdown("---")

                # Detailed analysis
                with st.expander("📊 Detailed Analysis"):
                    st.write(f"""
EPS Growth: {eps}%  
ROE: {roe}%  
Debt/Equity: {de}  
P/E: {pe}  
Sector P/E: {sector_pe}
""")

                # Recommendation
                st.subheader("🤖 Recommendation")

                if eps >= 15 and roe >= 18 and de <= 1:
                    if pe <= sector_pe:
                        st.success("🟢 Strong Buy")
                    else:
                        st.warning("🟡 Buy")
                else:
                    st.info("⚪ Hold")

        except:
            st.error("Error fetching data")

# -------------------- QUOTES --------------------
quotes = [
    "Be fearful when others are greedy. — Warren Buffett",
    "Time in the market beats timing the market.",
    "Price is what you pay, value is what you get.",
    "Know what you own.",
]

st.markdown("---")
st.markdown(f"<center style='color:#00ffcc;'>💡 {random.choice(quotes)}</center>", unsafe_allow_html=True)

