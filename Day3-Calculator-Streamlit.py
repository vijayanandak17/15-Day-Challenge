import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Simple Calculator")

# Store the expression
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Display area
st.text_input("Display", st.session_state.expression, key="display", disabled=True)

# Button layout (ordered like real calculator)
buttons = [
    ["1", "2", "3", "+"],
    ["4", "5", "6", "−"],
    ["7", "8", "9", "×"],
    ["0", ".", "=", "÷"],
    ["AC"]
]

# Button actions
def click(btn):
    if btn == "AC":
        st.session_state.expression = ""
    elif btn == "=":
        try:
            expr = st.session_state.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            st.session_state.expression = str(eval(expr))
        except:
            st.session_state.expression = "Error"
    else:
        st.session_state.expression += btn

# Render buttons
for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            click(btn)
