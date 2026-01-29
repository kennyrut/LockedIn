
import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="LockedIn", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #0b0f14;
    color: #e5e7eb;
}

h1, h2, h3 {
    color: #ef4444;
    font-weight: 800;
}

label {
    color: #9ca3af !important;
}

div.stButton > button {
    background-color: #ef4444;
    color: white;
    border-radius: 6px;
    font-weight: 700;
    border: none;
    padding: 0.5rem 1.2rem;
}

div.stButton > button:hover {
    background-color: #b91c1c;
}

.stAlert {
    border-left: 6px solid #ef4444;
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🏋️ LockedIn")
st.caption("Track. Progress. Dominate.")

# ---------------- DATA ----------------
DATA_FILE = "workouts.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["date", "exercise", "weight", "reps", "rpe"])

# ---------------- LOG WORKOUT ----------------
st.subheader("Log Exercise")

exercise = st.text_input("Exercise name")
weight = st.number_input("Weight (lbs)", min_value=0)
reps = st.number_input("Reps", min_value=0)
rpe = st.slider("RPE (effort)", 1, 10)

if st.button("Log Exercise"):
    if exercise:
        new_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "rpe": rpe
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Exercise logged.")
    else:
        st.warning("Enter an exercise name.")

# ---------------- HISTORY ----------------
st.subheader("Workout History")
st.dataframe(df)

# ---------------- SMART LOGIC ----------------
st.subheader("📈 Smart Recommendation")

if not df.empty:
    last = df.iloc[-1]
    if last["rpe"] >= 9:
        st.info("⚠️ High fatigue detected. Consider deloading.")
    elif last["reps"] >= 8:
        st.info("✅ Strong performance. Increase weight next session.")
    else:
        st.info("➡️ Maintain weight and aim for more reps.")
else:
    st.write("Log a workout to get recommendations.")

