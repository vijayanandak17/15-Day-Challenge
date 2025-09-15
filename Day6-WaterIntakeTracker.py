import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- App Title ---
st.set_page_config(page_title="Water Intake Tracker", layout="wide")

# --- Custom CSS for Dark Gray Theme ---
# --- Custom CSS for Beige Theme ---
st.markdown(
    """
    <style>
    body {
        background-color: beige;
        color: white;
    }
    .stApp {
        background-color: beige;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: black !important; /* Force titles/subheaders to black */
    }
    .stProgress > div > div > div {
        background-color: #1f77b4;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("💧 Water Intake Tracker")

# --- Constants ---
DAILY_GOAL_LITERS = 5.0
TIME_BLOCKS = ["Morning", "Afternoon", "Evening"]

# --- Initialize session state ---
if "water_log" not in st.session_state:
    st.session_state.water_log = {block: 0.0 for block in TIME_BLOCKS}

if "daily_log" not in st.session_state:
    st.session_state.daily_log = pd.DataFrame(columns=["Date", "Total Intake(L)"])

# --- Layout: 3 Columns (Input | Daily Progress | Weekly Progress) ---
col1, col2, col3 = st.columns(3)

# --- Daily Water Input ---
with col1:
    st.subheader("💦 Input Water Intake")
    for block in TIME_BLOCKS:
        st.session_state.water_log[block] = st.number_input(
            f"{block}", min_value=0.0, max_value=3.0, step=0.1,
            value=st.session_state.water_log[block], key=f"input_{block}"
        )

# --- Daily Total ---
daily_total = sum(st.session_state.water_log.values())

# --- Daily Progress ---
with col2:
    st.subheader("📊 Daily Progress")
    st.progress(min(daily_total / DAILY_GOAL_LITERS, 1.0))
    st.write(f"**Total Intake Today:** {daily_total:.2f} L / {DAILY_GOAL_LITERS} L")

    # RAG Status
    if daily_total >= DAILY_GOAL_LITERS:
        st.success("✅ Goal Achieved! (Green)")
    elif daily_total >= 0.7 * DAILY_GOAL_LITERS:
        st.warning("⚠️ Partial Goal (Amber)")
    else:
        st.error("❌ Goal Not Met (Red)")

# --- Update Daily Log ---
today = datetime.date.today()
if today not in st.session_state.daily_log["Date"].values:
    st.session_state.daily_log = pd.concat(
        [st.session_state.daily_log,
         pd.DataFrame({"Date": [today], "Total Intake(L)":[daily_total]})],
        ignore_index=True
    )
else:
    st.session_state.daily_log.loc[
        st.session_state.daily_log["Date"] == today, "Total Intake(L)"
    ] = daily_total

# --- Weekly Data (3 days before today, today, 3 days after) ---
week_range = pd.date_range(start=today - datetime.timedelta(days=3),
                           end=today + datetime.timedelta(days=3)).date
weekly_data = pd.DataFrame({"Date": week_range})
weekly_data = weekly_data.merge(
    st.session_state.daily_log, on="Date", how="left"
).fillna(0)

# --- Weekly Bar Chart ---
with col3:
    st.subheader("📅 Weekly Progress (Centered on Today)")
    if not weekly_data.empty:
        colors = []
        for date, val in zip(weekly_data["Date"], weekly_data["Total Intake(L)"]):
            if date == today:
                colors.append("blue")  # Highlight current day
            elif val >= DAILY_GOAL_LITERS:
                colors.append("green")
            elif val >= 0.7 * DAILY_GOAL_LITERS:
                colors.append("orange")
            else:
                colors.append("red")

        fig_week = px.bar(
            weekly_data,
            x="Date",
            y="Total Intake(L)",
            title="Hydration (3 Days Before & After Today)",
        )
        fig_week.update_traces(marker=dict(color=colors))
        fig_week.update_layout(
            yaxis_title="Liters",
            xaxis_title="Date",
            xaxis=dict(tickformat="%a\n%d-%b"),
            plot_bgcolor="#2e2e2e",
            paper_bgcolor="#2e2e2e",
            font=dict(color="white")
        )
        st.plotly_chart(fig_week, use_container_width=True)

        # Weekly RAG Status
        weekly_avg = weekly_data["Total Intake(L)"].mean()
        if weekly_avg >= DAILY_GOAL_LITERS:
            st.success(f"✅ Excellent! Avg {weekly_avg:.2f} L/day")
        elif weekly_avg >= 0.7 * DAILY_GOAL_LITERS:
            st.warning(f"⚠️ Moderate. Avg {weekly_avg:.2f} L/day")
        else:
            st.error(f"❌ Poor. Avg {weekly_avg:.2f} L/day")
    else:
        st.info("No weekly data yet.")
