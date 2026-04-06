import streamlit as st

# Page config
st.set_page_config(page_title="Stock Selection Tool", layout="centered")

# 🔥 Background CSS (stock theme)
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>📊 Fundamental Stock Selection Model</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze stocks like a pro 🚀</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Section
st.subheader("📥 Enter Financial Metrics")

col1, col2 = st.columns(2)

with col1:
    eps = st.number_input("📈 EPS Growth (%)", min_value=0.0, step=0.1)
    roe = st.number_input("💰 ROE (%)", min_value=0.0, step=0.1)

with col2:
    de = st.number_input("⚖️ Debt/Equity", min_value=0.0, step=0.1)
    pe = st.number_input("💸 P/E Ratio", min_value=0.0, step=0.1)

st.markdown("---")

# Button
if st.button("🚀 Analyze Stock"):

    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            st.success("🟢 Strong Buy")
        else:
            st.warning("🟡 Buy (Expensive)")

    elif eps >= 10 and roe >= 15 and de <= 1.5:
        st.warning("🟡 Buy")

    elif de > 2:
        st.error("🔴 Avoid (High Debt)")

    else:
        st.info("⚪ Hold")

    st.markdown("---")

    # Metrics Display
    st.subheader("📊 Input Summary")
    st.write(f"""
    - EPS Growth: {eps}%
    - ROE: {roe}%
    - Debt/Equity: {de}
    - P/E Ratio: {pe}
    """)
