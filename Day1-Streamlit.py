import streamlit as st

# Page config
st.set_page_config(page_title= "Day1 - Python challenge - Greeting App", layout="centered")

# Beige background using custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f5dc;  /* Beige */
        }
        .stForm {
            background-color: #fffaf0;  /* Light beige form */
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("👋 Greeting App")

# Create form
with st.form("greeting_form"):
    name = st.text_input("Enter your name")
    age = st.slider("Select your age", 1, 100, 25)
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name.strip():
            st.error("⚠️ Please enter your name.")
        else:
            st.success(f"Hello **{name}** 👋! You are {age} years old.")
