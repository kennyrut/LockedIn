import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Lockedin", layout="centered")
st.title("🔒 Lockedin")

# -----------------------------
# Session State
# -----------------------------
if "workouts" not in st.session_state:
    st.session_state.workouts = {}

if "current_exercises" not in st.session_state:
    st.session_state.current_exercises = []

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Workout", "Calendar"])

# =============================
# WORKOUT TAB
# =============================
with tab1:
    st.header("Create Workout")

    workout_name = st.text_input("Workout name", placeholder="Back, Chest, Legs")
    workout_date = st.date_input("Workout date", value=date.today())

    st.divider()
    st.subheader("Add Exercise")

    ex_name = st.text_input("Exercise name", placeholder="Row Machine")

    mode = st.radio("Tracking", ["Plates", "Weight"], horizontal=True)

    if mode == "Plates":
        value = st.number_input("Plates", min_value=0, step=1)
    else:
        value = st.number_input("Weight (lbs)", min_value=0, step=5)

    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)

    notes = st.text_input("Notes (optional)", placeholder="Optional")

    if st.button("➕ Add Exercise"):
        st.session_state.current_exercises.append({
            "name": ex_name,
            "mode": mode,
            "value": value,
            "sets": sets,
            "reps": reps,
            "notes": notes
        })

    # Live preview of workout
    if st.session_state.current_exercises:
        st.subheader("Workout Preview")

        for ex in st.session_state.current_exercises:
            unit = "plates" if ex["mode"] == "Plates" else "lbs"
            st.markdown(
                f"""
                **{ex['name']}**  
                {ex['value']} {unit} — {ex['sets']} x {ex['reps']}  
                _{ex['notes']}_
                """
            )

    if st.button("💾 Save Workout"):
        key = workout_date.isoformat()
        st.session_state.workouts[key] = {
            "name": workout_name,
            "exercises": st.session_state.current_exercises.copy()
        }
        st.session_state.current_exercises.clear()
        st.success("Workout saved to calendar")

# =============================
# CALENDAR TAB
# =============================
with tab2:
    st.header("Calendar")

    start = date.today() - timedelta(days=14)
    days = [start + timedelta(days=i) for i in range(28)]

    for week in range(0, 28, 7):
        cols = st.columns(7)
        for i, col in enumerate(cols):
            day = days[week + i]
            key = day.isoformat()

            label = day.strftime("%d")

            if key in st.session_state.workouts:
                workout = st.session_state.workouts[key]["name"]
                if col.button(f"{label}\n{workout}", key=key):
                    st.session_state.selected_day = key
            else:
                col.write(label)

    if "selected_day" in st.session_state:
        day = st.session_state.selected_day
        workout = st.session_state.workouts[day]

        st.divider()
        st.subheader(f"{day} — {workout['name']}")

        for ex in workout["exercises"]:
            unit = "plates" if ex["mode"] == "Plates" else "lbs"
            st.write(
                f"- {ex['name']}: {ex['value']} {unit}, "
                f"{ex['sets']} x {ex['reps']}"
            )
            if ex["notes"]:
                st.caption(ex["notes"])
