import streamlit as st

# Removed dependency on unavailable package: streamlit_extras.metric_cards

# Set Streamlit page configuration (title, icon, layout)
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background-color: #f8f9fa; /* light background color */
        }
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 2rem; /* spacing top & bottom */
        }
        .bmi-box {
            background: white;
            padding: 2rem; /* inner padding */
            border-radius: 20px; /* rounded card corners */
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* subtle shadow */
            text-align: center; /* center alignment */
        }
        .bmi-value {
            font-size: 2.5rem; /* large BMI value */
            font-weight: bold;
            color: #ff6b6b; /* default text color */
        }
        .bmi-status {
            font-size: 1.2rem;
            font-weight: 500;
            margin-top: 0.5rem; /* spacing above */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description
st.title("⚖️ BMI Calculator")
st.write("Easily calculate your Body Mass Index and check your health category.")

# Input section: height and weight
col1, col2 = st.columns(2)
with col1:
    height = st.slider("Select your height (cm)", 100, 220, 170)
with col2:
    weight = st.slider("Select your weight (kg)", 30, 150, 70)

# Calculate BMI using formula: weight (kg) / (height (m) ^ 2)
bmi = weight / ((height / 100) ** 2)

# Function to determine BMI category with color coding
def bmi_category(bmi):
    if bmi < 18.5:
        return ("Underweight", "#00b4d8")
    elif 18.5 <= bmi < 24.9:
        return ("Normal weight", "#38b000")
    elif 25 <= bmi < 29.9:
        return ("Overweight", "#ffb703")
    else:
        return ("Obese", "#d00000")

# Get category and its color
status, color = bmi_category(bmi)

# Display the BMI result in styled box
st.markdown(
    f"""
    <div class="bmi-box">
        <div class="bmi-value">{bmi:.1f}</div>
        <div class="bmi-status" style="color:{color};">{status}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Info message for users
st.info("💡 BMI is a general guideline. Consult a healthcare provider for more accurate health assessments.")