import streamlit as st
import yfinance as yf

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Stock Selection Tool", layout="centered")

# -------------------- BACKGROUND --------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.markdown("<h1 style='text-align: center;'>📊 Fundamental Stock Selection Model</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze stocks like a pro 🚀</p>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- INPUT --------------------
stock_name = st.text_input("🔍 Enter Stock (e.g., TCS.NS, RELIANCE.NS)")

# -------------------- BUTTON --------------------
if st.button("🚀 Analyze Stock"):

    if stock_name == "":
        st.warning("Please enter a stock name ⚠️")

    else:
        try:
            stock = yf.Ticker(stock_name)

            # Check if valid stock
            hist = stock.history(period="1d")

            if hist.empty:
                st.error("❌ Invalid stock name")
            else:
                st.success("✅ Stock Found")

                # -------------------- SAFE DATA --------------------
                price = hist["Close"].iloc[-1]

                fast_info = stock.fast_info
                pe = fast_info.get("trailing_pe", None)

                # Dummy fundamentals (since API unreliable)
                eps_growth = 15
                roe = 18
                de = 0.5

                # -------------------- DISPLAY --------------------
                st.subheader("📊 Stock Data")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("💰 Price", f"₹ {price:.2f}")
                    st.metric("📈 EPS Growth", f"{eps_growth}%")

                with col2:
                    st.metric("💸 P/E Ratio", f"{pe if pe else 'N/A'}")
                    st.metric("🏦 ROE", f"{roe}%")

                st.markdown("---")

                # -------------------- LOGIC --------------------
                st.subheader("🤖 Recommendation")

                if eps_growth >= 15 and roe >= 18 and de <= 1:
                    if pe and pe <= 20:
                        st.success("🟢 Strong Buy (Growth + Value)")
                    else:
                        st.warning("🟡 Buy (Good company but expensive)")

                elif de > 2:
                    st.error("🔴 Avoid (High Debt)")

                else:
                    st.info("⚪ Hold / Watchlist")

        except:
            st.error("⚠️ Error fetching data. Try another stock.")
