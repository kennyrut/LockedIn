import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="LockedIn",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 LockedIn")
st.write("Train hard. Track smarter. Stay locked in.")

# ----------------------------
# Data setup
# ----------------------------
DATA_FILE = "workouts.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["date", "exercise", "weight", "reps", "rpe"])

# ----------------------------
# Input Form
# ----------------------------
st.subheader("Log a Workout")

exercise = st.text_input("Exercise name")
weight = st.number_input("Weight (lbs)", min_value=0)
reps = st.number_input("Reps", min_value=0)
rpe = st.slider("RPE (effort)", 1, 10)

if st.button("Log Workout"):
    if exercise.strip():
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "rpe": rpe
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Workout logged!")
    else:
        st.warning("Please enter an exercise name.")

# ----------------------------
# History
# ----------------------------
st.subheader("Workout History")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Smart Recommendation
# ----------------------------
st.subheader("📈 Smart Recommendation")

if not df.empty:
    last = df.iloc[-1]

    if last["rpe"] >= 9:
        st.info("⚠️ High fatigue detected. Consider reducing volume or deloading.")
    elif last["reps"] >= 8:
        st.info("✅ Strong performance. Consider increasing weight next session.")
    else:
        st.info("➡️ Maintain weight and aim to increase reps.")
else:
    st.info("Log a workout to receive recommendations.")

