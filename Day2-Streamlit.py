import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bill Splitter by Vijayanand - Day 2", layout="centered")

st.title("💰 Bill Splitter Application")

# Inputs
total_amount = st.number_input("Enter total bill amount", min_value=0.0, step=0.01)
num_people = st.number_input("Enter number of people", min_value=1, step=1)

if total_amount > 0 and num_people > 0:
    st.subheader("Contribution Settings")

    # Default equal split
    equal_share = round(total_amount / num_people, 2)
    st.write(f"💡 Default equal share per person: **{equal_share}**")

    contributions = []
    total_contributed = 0

    # Sliders for each person
    for i in range(num_people):
        contribution = st.slider(
            f"Person {i+1} contribution",
            min_value=0.0,
            max_value=float(total_amount),
            value=equal_share,
            step=0.5,
        )
        contributions.append(contribution)
        total_contributed += contribution

    # Display results
    st.subheader("Summary")
    st.write(f"💵 Total Bill: **{total_amount}**")
    st.write(f"🧾 Total Contributions: **{total_contributed}**")

    if round(total_contributed, 2) == round(total_amount, 2):
        st.success("✅ The bill is fully covered!")
    elif total_contributed < total_amount:
        st.warning(f"⚠️ Still need {total_amount - total_contributed:.2f}")
    else:
        st.error(f"⚠️ Overpaid by {total_contributed - total_amount:.2f}")

    

else:
    st.info("👉 Please enter a valid bill amount and number of people to continue.")
