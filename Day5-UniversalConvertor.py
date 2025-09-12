import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Universal Unit Converter", page_icon="🔄", layout="centered")

# ---- CUSTOM CSS for Apple-like UI ----
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom right, #f5f5f7, #e5e5ea);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .stApp {
        background-color: #f5f5f7;
    }
    h1 {
        font-weight: 600;
        color: #1d1d1f;
        text-align: center;
        padding-bottom: 20px;
    }
    .result-box {
        background: white;
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        color: #1d1d1f;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- HEADER ----
st.markdown("<h1>🌍 Universal Unit Converter</h1>", unsafe_allow_html=True)

# ---- Categories ----
categories = {
    "Length": {
        "Meter": 1,
        "Kilometer": 1000,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254
    },
    "Weight": {
        "Kilogram": 1,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.453592,
        "Ounce": 0.0283495
    },
    "Temperature": "special",
    "Volume": {
        "Liter": 1,
        "Milliliter": 0.001,
        "Cubic meter": 1000,
        "Gallon": 3.78541,
        "Quart": 0.946353,
        "Pint": 0.473176,
        "Cup": 0.24
    }
}

# ---- Category selection ----
category = st.radio("Select Category", list(categories.keys()), horizontal=True)

if category != "Temperature":
    units = list(categories[category].keys())

    col1, col2, col3 = st.columns([1, 1, 1.2])

    with col1:
        from_unit = st.radio("From", units)
    with col2:
        to_unit = st.radio("To", units)
    with col3:
        value = st.number_input("Value", min_value=0.0, format="%.1f")

    # ---- Instant Conversion ----
    if value:
        result = value * (categories[category][from_unit] / categories[category][to_unit])
        st.markdown(f"<div class='result-box'>{value} {from_unit} = {result:.4f} {to_unit}</div>", unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns([1, 1, 1.2])

    with col1:
        from_unit = st.radio("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.radio("To", ["Celsius", "Fahrenheit", "Kelvin"])
    with col3:
        value = st.number_input("Temperature", format="%.2f")

    # ---- Instant Temperature Conversion ----
    result = None
    if from_unit == to_unit:
        result = value
    elif from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            result = (value * 9/5) + 32
        elif to_unit == "Kelvin":
            result = value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            result = (value - 32) * 5/9
        elif to_unit == "Kelvin":
            result = (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            result = value - 273.15
        elif to_unit == "Fahrenheit":
            result = (value - 273.15) * 9/5 + 32

    if result is not None:
        st.markdown(f"<div class='result-box'>{value} {from_unit} = {result:.1f} {to_unit}</div>", unsafe_allow_html=True)
