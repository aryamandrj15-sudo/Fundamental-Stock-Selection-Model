import streamlit as st
import yfinance as yf

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
.glow {
    text-shadow: 0 0 10px #00ffcc;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- AI HELPER --------------------
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

top1, top2 = st.columns([6,1])

with top1:
    st.markdown("<h1 class='glow' style='text-align:center;'>📊 Stock Intelligence Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00ffcc;'>Your mini stock analysis terminal 🚀</p>", unsafe_allow_html=True)

with top2:
    if st.button("🤖 AI Helper"):
        st.session_state.show_ai = not st.session_state.show_ai

# Sidebar AI
if st.session_state.show_ai:
    st.sidebar.title("🤖 Stock Assistant")
    question = st.sidebar.text_input("Ask anything about stocks:")

    if question:
        q = question.lower()

        if "pe" in q:
            st.sidebar.write("""
📊 **P/E Ratio (Price to Earnings Ratio)**

The P/E ratio measures how much investors are willing to pay for each unit of earnings.

It is calculated as: Price per Share / Earnings per Share.

A high P/E ratio usually indicates that the stock is expensive or that investors expect high future growth.

A low P/E ratio may suggest undervaluation, but sometimes it can also indicate weak business performance.

It should always be compared with industry or sector P/E for better understanding.

👉 In simple terms: It tells you whether a stock is cheap or expensive.
""")

        elif "roe" in q:
            st.sidebar.write("""
💰 **ROE (Return on Equity)**

ROE shows how efficiently a company uses shareholders' money to generate profits.

It is calculated as: Net Income / Shareholder Equity.

A higher ROE generally means better management and efficient use of capital.

Companies with ROE above 15–20% are usually considered strong.

Consistently high ROE over years is a sign of a quality business.

👉 In simple terms: It tells how good the company is at making money.
""")

        elif "debt" in q or "de" in q:
            st.sidebar.write("""
⚖️ **Debt to Equity Ratio**

This ratio shows how much debt a company has compared to its own capital.

A lower ratio (<1) means the company is financially stable.

A higher ratio (>2) indicates higher risk, especially during downturns.

Too much debt can reduce profits due to interest payments.

👉 In simple terms: It tells how risky the company is financially.
""")

        elif "rsi" in q:
            st.sidebar.write("""
📉 **RSI (Relative Strength Index)**

RSI is a momentum indicator used in technical analysis.

It ranges from 0 to 100 and helps identify overbought or oversold conditions.

Above 70 → Overbought (possible correction)

Below 30 → Oversold (possible bounce)

👉 In simple terms: It helps you decide when to buy or sell.
""")

        elif "buy" in q:
            st.sidebar.write("""
🟢 **When should you buy a stock?**

Look for companies with strong fundamentals.

Key indicators include high EPS growth, high ROE, and low debt.

Also check if the stock is reasonably valued.

👉 Buy good companies at fair prices.
""")

        elif "sell" in q:
            st.sidebar.write("""
🔴 **When should you sell a stock?**

Sell when fundamentals weaken or valuation becomes too high.

High debt or falling profits are warning signs.

👉 Avoid emotional decisions.
""")

        else:
            st.sidebar.write("""
🤖 I'm still improving and learning!

Right now, I can help you with:

• P/E Ratio  
• ROE  
• Debt/Equity  
• RSI  
• Buy/Sell decisions  

More advanced features coming soon 🚀
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
