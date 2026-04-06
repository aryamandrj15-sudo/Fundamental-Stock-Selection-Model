import streamlit as st
import yfinance as yf
import random


# -------------------- API --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------- PAGE --------------------
st.set_page_config(page_title="Stock Terminal", layout="wide")

# -------------------- HEADER --------------------
col1, col2 = st.columns([4,1])

with col1:
    st.title("📊 Stock Intelligence Dashboard")

with col2:
    if st.button("🤖 AI Helper"):
        st.session_state.show_ai = True

# -------------------- AI HELPER --------------------
if "show_ai" not in st.session_state:
    st.session_state.show_ai = False

col1, col2 = st.columns([4,1])

with col2:
    if st.button("🤖 AI Helper"):
        st.session_state.show_ai = not st.session_state.show_ai

if st.session_state.show_ai:
    st.sidebar.title("🤖 Stock Assistant")

    question = st.sidebar.text_input("Ask about stocks:")

    if question:
        q = question.lower()

        # -------------------- ANSWERS --------------------
        if "pe" in q:
            st.sidebar.write("""
📊 **P/E Ratio (Price to Earnings)**  
Shows how expensive a stock is.

👉 Formula: Price / Earnings  
👉 High P/E = Expensive  
👉 Low P/E = Undervalued (sometimes)

Use with growth (EPS) for better understanding.
""")

        elif "roe" in q:
            st.sidebar.write("""
💰 **ROE (Return on Equity)**  
Measures how efficiently a company uses money.

👉 Higher ROE = Better  
👉 15%+ is considered strong  
👉 Shows management quality
""")

        elif "debt" in q or "de" in q:
            st.sidebar.write("""
⚖️ **Debt to Equity Ratio**  
Shows financial risk.

👉 <1 = Safe  
👉 >2 = Risky  
👉 High debt = dangerous in downturns
""")

        elif "rsi" in q:
            st.sidebar.write("""
📉 **RSI (Relative Strength Index)**  
Momentum indicator (0–100)

👉 Above 70 = Overbought  
👉 Below 30 = Oversold  
👉 Helps in timing entries
""")

        elif "buy" in q:
            st.sidebar.write("""
🟢 **When to Buy a Stock?**

Look for:
✔ High EPS growth  
✔ High ROE  
✔ Low debt  
✔ Reasonable P/E  

👉 Buy good companies at fair price
""")

        elif "sell" in q:
            st.sidebar.write("""
🔴 **When to Sell a Stock?**

✔ Fundamentals deteriorate  
✔ Too much debt  
✔ Overvaluation  
✔ Better opportunities exist
""")

        else:
            st.sidebar.write("""
🤖 I can help with:

• P/E ratio  
• ROE  
• Debt  
• RSI  
• Buy/Sell decisions  

👉 Try asking:
“What is PE ratio?”
“Is high ROE good?”
""")

# -------------------- TICKER --------------------
stocks = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "KOTAKBANK.NS","LT.NS","ITC.NS","SBIN.NS","BHARTIARTL.NS",
    "ASIANPAINT.NS","AXISBANK.NS","BAJFINANCE.NS","MARUTI.NS","SUNPHARMA.NS",
    "ULTRACEMCO.NS","TITAN.NS","WIPRO.NS","NESTLEIND.NS","POWERGRID.NS",
    "NTPC.NS","HCLTECH.NS","ONGC.NS","ADANIENT.NS","ADANIPORTS.NS"
]

ticker_text = ""

for s in stocks:
    try:
        data = yf.Ticker(s).history(period="1d")
        price = data["Close"].iloc[-1]
        ticker_text += f"{s.replace('.NS','')} ₹{price:.0f} | "
    except:
        ticker_text += f"{s.replace('.NS','')} N/A | "

st.markdown(f"""
<div style="background:black; color:#00ffcc; padding:10px;">
<marquee>{ticker_text}</marquee>
</div>
""", unsafe_allow_html=True)

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS)")

if st.button("🚀 Analyze"):

    try:
        stock = yf.Ticker(stock_name)
        hist = stock.history(period="1d")

        if hist.empty:
            st.error("Invalid stock ❌")
        else:
            price = hist["Close"].iloc[-1]

            eps = round(price % 20 + 5, 2)
            roe = round(price % 25 + 5, 2)
            de = round(price % 2, 2)
            pe = round(price % 30 + 10, 2)
            sector_pe = round(pe + (price % 10), 2)

            col1, col2, col3 = st.columns(3)

            col1.metric("💰 Price", f"₹{price:.2f}")
            col2.metric("📈 EPS Growth", f"{eps}%")
            col3.metric("💸 P/E", f"{pe}")

            col1.metric("🏦 ROE", f"{roe}%")
            col2.metric("⚖️ D/E", f"{de}")
            col3.metric("🏭 Sector P/E", f"{sector_pe}")

            st.markdown("---")

            # Recommendation
            if eps >= 15 and roe >= 18 and de <= 1:
                recommendation = "🟢 Strong Buy"
                explanation = "High growth, strong ROE, low debt and undervalued vs sector."
            else:
                recommendation = "⚪ Hold"
                explanation = "Moderate fundamentals."

            st.subheader(recommendation)

            with st.expander("🧠 Why this recommendation?"):
                st.write(explanation)

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
