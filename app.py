try:
    stock = yf.Ticker(stock_name)
    hist = stock.history(period="1d")

    if hist.empty:
        st.error("Invalid stock name ❌")
    else:
        st.success("Stock Found ✅")

        # Use safer values
        pe = stock.fast_info.get("trailing_pe", 20)

        # Temporary logic values
        eps_growth = 15
        roe = 18
        de = 0.5

        st.subheader("📊 Analysis")

        st.write(f"P/E Ratio: {pe:.2f}")

        if eps_growth >= 15 and roe >= 18 and de <= 1:
            if pe <= 20:
                st.success("🟢 Strong Buy")
            else:
                st.warning("🟡 Buy (Expensive)")
        else:
            st.info("⚪ Hold")

except:
    st.error("Error fetching stock ❌")
