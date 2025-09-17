import streamlit as st
import requests
import pandas as pd

# --- App Config ---
st.set_page_config(page_title="Currency Converter", layout="wide")

st.title("💱 Currency Converter")

# --- Fetch latest exchange rates ---
@st.cache_data
def get_exchange_rates(base_currency="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data

# --- Input Section ---
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    amount = st.number_input("Enter Amount", min_value=0.0, value=100.0, step=1.0)

with col2:
    base_currency = st.selectbox("From Currency", ["USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD"])

with col3:
    target_currency = st.selectbox("To Currency", ["USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD"])

# --- Conversion ---
rates_data = get_exchange_rates(base_currency)
rates = rates_data["rates"]

if target_currency in rates:
    converted_amount = amount * rates[target_currency]
    st.subheader(f"✅ {amount} {base_currency} = {converted_amount:.2f} {target_currency}")
else:
    st.error("Conversion not available for selected currency.")

# --- Conversion Table (currencies as header, center aligned) ---
st.write("### 🌍 Conversion Across Major Currencies")

selected_currencies = ["USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD"]

conversion_dict = {cur: round(amount * rates[cur], 2) for cur in selected_currencies if cur in rates}

# Create DataFrame
df = pd.DataFrame([conversion_dict])

# Apply center alignment using Pandas Styler
styled_df = df.style.set_table_styles(
    [
        {"selector": "th", "props": [("text-align", "center")]},  # center header
        {"selector": "td", "props": [("text-align", "center")]}   # center content
    ]
)

st.write(styled_df)
