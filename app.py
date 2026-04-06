import streamlit as st
import yfinance as yf

# Page config
st.set_page_config(page_title="Stock Selection Tool", layout="centered")

# Title
st.title("📊 Fundamental Stock Selection Model")
st.write("Enter a stock name to analyze automatically 🚀")

# Input stock name
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS, RELIANCE.NS)")

if st.button("Analyze Stock"):

    try:
        stock = yf.Ticker(stock_name)
        info = stock.info

        # Extract data
        eps_growth = info.get("earningsGrowth", 0) * 100 if info.get("earningsGrowth") else 0
        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        de = info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else 0
        pe = info.get("trailingPE", 0)

        st.subheader("📊 Fetched Data")
        st.write(f"EPS Growth: {eps_growth:.2f}%")
        st.write(f"ROE: {roe:.2f}%")
        st.write(f"Debt/Equity: {de:.2f}")
        st.write(f"P/E Ratio: {pe:.2f}")

        # 🔥 AI-like logic
        if eps_growth >= 15 and roe >= 18 and de <= 1:
            if pe <= 20:
                st.success("🟢 Strong Buy (High Growth + Undervalued)")
            else:
                st.warning("🟡 Buy (Strong but Expensive)")
        
        elif eps_growth >= 10 and roe >= 15:
            st.warning("🟡 Moderate Buy")

        elif de > 2:
            st.error("🔴 Avoid (High Debt Risk)")

        elif pe > 30:
            st.error("🔴 Avoid (Overvalued)")

        else:
            st.info("⚪ Hold / Watchlist")

    except Exception as e:
        st.error("Invalid stock name or data not available ❌")
