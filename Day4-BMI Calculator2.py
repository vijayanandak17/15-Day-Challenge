import streamlit as st

# Set Streamlit page configuration (title, icon, layout)
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# ----------------------
# Custom CSS for styling
# ----------------------
# We include styles for the card, value text, and simple rules to highlight the selected silhouette.
st.markdown(
    """
    <style>
        .main { background-color: #f8f9fa; }
        div.block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .bmi-box { background: white; padding: 2rem; border-radius: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); text-align: center; }
        .bmi-value { font-size: 2.5rem; font-weight: bold; color: #ff6b6b; }
        .bmi-status { font-size: 1.2rem; font-weight: 500; margin-top: 0.5rem; }
        /* container for silhouettes */
        .sil-container { display: flex; gap: 1rem; justify-content: center; margin-bottom: 1rem; }
        .sil-card { background: white; padding: 0.6rem; border-radius: 12px; width: 120px; display:flex; align-items:center; justify-content:center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: transform .15s ease, box-shadow .15s ease; }
        .sil-card.selected { transform: translateY(-6px); box-shadow: 0 8px 20px rgba(0,0,0,0.12); border: 2px solid #38b000; }
        .sil-icon { width: 80px; height: 120px; }
        /* small responsive tweaks */
        @media (max-width: 600px) {
            .sil-card { width: 90px; }
            .sil-icon { width: 60px; height: 90px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------
# Title and description
# ----------------------
st.title("⚖️ BMI Calculator")
st.write("Easily calculate your Body Mass Index and check your health category. Select your gender for a tailored silhouette preview.")

# ----------------------
# Gender selection UI
# ----------------------
# We show inline SVG silhouettes for male and female. The selected option gets a highlighted card via CSS class.
gender = st.radio("Select Gender", ["Male", "Female", "Prefer not to say"], horizontal=True)

# Inline SVGs for silhouettes (keeps the app self-contained without external image files).
male_svg = '''
<svg class="sil-icon" viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg">
  <g fill="#4b5563">
    <circle cx="40" cy="18" r="12" />
    <rect x="30" y="34" width="20" height="36" rx="6" />
    <rect x="18" y="70" width="12" height="32" rx="6" />
    <rect x="50" y="70" width="12" height="32" rx="6" />
  </g>
</svg>
'''

female_svg = '''
<svg class="sil-icon" viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg">
  <g fill="#4b5563">
    <circle cx="40" cy="16" r="10" />
    <path d="M28 30c0 0 4 18 12 18s12-18 12-18v10c0 0-4 6-12 6s-12-6-12-6V30z" />
    <path d="M22 52c0 0 6 18 18 18s18-18 18-18v38h-36V52z" />
  </g>
</svg>
'''

# Build the HTML for silhouettes and apply 'selected' class depending on user choice
male_class = "sil-card selected" if gender == "Male" else "sil-card"
female_class = "sil-card selected" if gender == "Female" else "sil-card"

st.markdown(
    f"""
    <div class="sil-container">
        <div class="{male_class}">{male_svg}</div>
        <div class="{female_class}">{female_svg}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------
# Unit selection (height/weight)
# ----------------------
col_units1, col_units2 = st.columns(2)
with col_units1:
    height_unit = st.radio("Height Unit", ["cm", "feet/inches"])  # choose between cm and feet+inches
with col_units2:
    weight_unit = st.radio("Weight Unit", ["kg", "lbs"])        # choose between kg and lbs

# ----------------------
# Inputs: vertical sliders and conversion handling
# ----------------------
# We keep the existing sliders but present them clearly. Streamlit does not provide a native vertical slider
# component that is stable cross-platform, so we use regular sliders arranged vertically by layout.
left_col, right_col = st.columns(2)
with left_col:
    if height_unit == "cm":
        height = st.slider("Height (cm)", 100, 220, 170, key="height_cm")
    else:
        feet = st.slider("Feet", 3, 7, 5, key="feet")
        inches = st.slider("Inches", 0, 11, 6, key="inches")
        # Convert feet+inches to cm (1 inch = 2.54 cm)
        height = (feet * 12 + inches) * 2.54

with right_col:
    if weight_unit == "kg":
        weight = st.slider("Weight (kg)", 30, 150, 70, key="weight_kg")
    else:
        weight_lbs = st.slider("Weight (lbs)", 66, 330, 154, key="weight_lbs")
        # Convert pounds to kilograms (1 lb = 0.453592 kg)
        weight = weight_lbs * 0.453592

# ----------------------
# BMI calculation and category logic
# ----------------------
# BMI formula: weight (kg) / (height (m) ^ 2)
bmi = weight / ((height / 100) ** 2)

def bmi_category(bmi_value: float):
    """Return a (label, color) tuple based on BMI ranges."""
    if bmi_value < 18.5:
        return ("Underweight", "#00b4d8")
    elif 18.5 <= bmi_value < 24.9:
        return ("Normal weight", "#38b000")
    elif 25 <= bmi_value < 29.9:
        return ("Overweight", "#ffb703")
    else:
        return ("Obese", "#d00000")

status, color = bmi_category(bmi)

# ----------------------
# Display results
# ----------------------
# Show a styled card with the BMI and status. We keep the male/female selection purely visual here; BMI
# calculation is independent of gender (but you asked for gender input so we surface it in the UI).
st.markdown(
    f"""
    <div class="bmi-box">
        <div style="font-size:0.9rem; color:#6b7280; margin-bottom:6px;">Selected: {gender}</div>
        <div class="bmi-value">{bmi:.1f}</div>
        <div class="bmi-status" style="color:{color};">{status}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Provide an informational note about BMI and gender
st.info("💡 BMI provides a rough estimate of body fat — gender-aware assessments exist, so consult a professional for personalized advice.")
