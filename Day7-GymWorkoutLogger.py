import streamlit as st
import pandas as pd
import datetime
import os

# --- File to store workout history ---
FILE_PATH = "workout_log.csv"

# --- Initialize file if not present ---
if not os.path.exists(FILE_PATH):
    df_init = pd.DataFrame(columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Total_Lifted"])
    df_init.to_csv(FILE_PATH, index=False)

# --- Load data ---
df = pd.read_csv(FILE_PATH)

# --- App Title ---
st.title("🏋️ Gym Workout Logger")
st.markdown("Log your daily workouts and track progress over time.")

# --- Sidebar Input Form ---
st.sidebar.header("➕ Add New Workout Entry")

date = st.sidebar.date_input("Date", datetime.date.today())
exercise = st.sidebar.text_input("Exercise Name")
sets = st.sidebar.number_input("Sets", min_value=1, step=1)
reps = st.sidebar.number_input("Reps per Set", min_value=1, step=1)
weight = st.sidebar.number_input("Weight per Rep (lbs)", min_value=0, step=5)

# Calculate total lifted
total_lifted = sets * reps * weight

if st.sidebar.button("Add Entry"):
    new_entry = pd.DataFrame([[date, exercise, sets, reps, weight, total_lifted]],
                             columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Total_Lifted"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)
    st.sidebar.success("✅ Entry Added Successfully!")

# --- Show Workout History ---
st.subheader("📋 Workout History")
st.dataframe(df)

# --- Summary Stats ---
st.subheader("📊 Weekly Progress")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.isocalendar().week

weekly_progress = df.groupby("Week").agg({
    "Total_Lifted": "sum",
    "Reps": "sum",
    "Sets": "sum"
}).reset_index()

st.line_chart(weekly_progress.set_index("Week")[["Total_Lifted", "Reps", "Sets"]])

# --- Additional Stats ---
st.subheader("📌 Summary Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Weight Lifted", f"{df['Total_Lifted'].sum()} lbs")
col2.metric("Total Reps", f"{df['Reps'].sum()}")
col3.metric("Total Sets", f"{df['Sets'].sum()}")
