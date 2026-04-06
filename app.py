import streamlit as st
import yfinance as yf

# Page config
st.set_page_config(page_title="Stock App", layout="centered")

st.title("📊 Fundamental Stock Selection Model")

stock_name = st.text_input("Enter Stock (e.g., TCS.NS)")

if st.button("Analyze"):

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
                st.success(f"Price: ₹{price:.2f}")

        except:
            st.error("Error fetching data")
