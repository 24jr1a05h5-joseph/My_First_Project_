import requests
import streamlit as st

st.set_page_config(page_title="Joseph Currency Converter", page_icon="💱")

# Offline fallback rates (per 1 USD) used if the live API is unreachable
FALLBACK_RATES = {
    "USD": 1.0, "INR": 83.0, "EUR": 0.92, "GBP": 0.79, "JPY": 150.0,
    "AUD": 1.55, "CAD": 1.36, "CNY": 7.2, "AED": 3.67, "SGD": 1.35,
}
CURRENCIES = list(FALLBACK_RATES.keys())


@st.cache_data(ttl=3600)
def get_rates():
    """Fetch live rates (base USD). Fall back to static rates on failure."""
    try:
        resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        resp.raise_for_status()
        rates = resp.json()["rates"]
        return {c: rates[c] for c in CURRENCIES}, True
    except Exception:
        return FALLBACK_RATES, False


def convert(amount, from_cur, to_cur, rates):
    return amount / rates[from_cur] * rates[to_cur]


st.title("💱 joseph Currency Converter")
st.write("Convert money between popular currencies instantly.")

rates, is_live = get_rates()
if is_live:
    st.caption("✅ Using live exchange rates (updated hourly).")
else:
    st.caption("⚠️ Live rates unavailable. Using approximate offline rates.")

amount = st.number_input("Amount", min_value=0.0, value=100.0, step=1.0)

col1, col2 = st.columns(2)
with col1:
    from_cur = st.selectbox("From", CURRENCIES, index=CURRENCIES.index("USD"))
with col2:
    to_cur = st.selectbox("To", CURRENCIES, index=CURRENCIES.index("INR"))

if st.button("Convert", type="primary"):
    result = convert(amount, from_cur, to_cur, rates)
    st.success(f"{amount:,.2f} {from_cur} = {result:,.2f} {to_cur}")
    unit = convert(1, from_cur, to_cur, rates)
    st.info(f"Rate: 1 {from_cur} = {unit:,.4f} {to_cur}")
