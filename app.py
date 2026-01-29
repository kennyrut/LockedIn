import streamlit as st
import sqlite3
import uuid
from datetime import datetime
import pandas as pd

# ----------------------------
# App Config
# ----------------------------
st.set_page_config(
    page_title="LockedIn",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 LockedIn")
st.caption("Train hard. Track smarter. Stay locked in.")

# ----------------------------
# Device-based user ID
# ----------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

USER_ID = st.session_state.user_id

# ----------------------------
# Database setup (SQLite)
# ----------------------------
conn = sqlite3.connect("lockedin.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    date TEXT,
    exercise TEXT,
    weight INTEGER,
    reps INTEGER,
    rpe INTEGER
)
""")
conn.commit()

# ----------------------------
# Log Workout
# ----------------------------
st.subheader("Log a Workout")

exercise = st.text_input("Exercise")
weight = st.number_input("Weight (lbs)", min_value=0)
reps = st.number_input("Reps", min_value=0)
rpe = st.slider("RPE (effort)", 1, 10)

if st.button("Log Workout"):
    if exercise.strip():
        cursor.execute(
            "INSERT INTO workouts (user_id, date, exercise, weight, reps, rpe) VALUES (?, ?, ?, ?, ?, ?)",
            (
                USER_ID,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                exercise,
                weight,
                reps,
                rpe
            )
        )
        conn.commit()
        st.success("Workout logged 💪")
    else:
        st.warning("Please enter an exercise name.")

# ----------------------------
# Workout History (per user)
# ----------------------------
st.subheader("Your Workout History")

df = pd.read_sql_query(
    "SELECT date, exercise, weight, reps, rpe FROM workouts WHERE user_id = ? ORDER BY id DESC",
    conn,
    params=(USER_ID,)
)

st.dataframe(df, use_container_width=True)

# ----------------------------
# Smart Recommendation
# ----------------------------
st.subheader("📈 Smart Recommendation")

if not df.empty:
    last = df.iloc[0]

    if last["rpe"] >= 9:
        st.info("⚠️ High fatigue detected. Consider reducing volume or deloading.")
    elif last["reps"] >= 8:
        st.info("✅ Strong performance. Consider increasing weight next session.")
    else:
        st.info("➡️ Maintain weight and aim to increase reps.")
else:
    st.info("Log a workout to receive recommendations.")
