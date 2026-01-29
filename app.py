import streamlit as st
from datetime import date

st.set_page_config(page_title="Lockedin", layout="centered")

# -----------------------------
# App State
# -----------------------------
if "workouts" not in st.session_state:
    st.session_state.workouts = {}  
    # format:
    # {
    #   "2026-01-28": {
    #       "name": "Back",
    #       "exercises": [
    #           {
    #               "name": "Row Machine",
    #               "mode": "Plates",
    #               "value": 4,
    #               "sets": 5,
    #               "reps": 5
    #           }
    #       ]
    #   }
    # }

# -----------------------------
# Header
# -----------------------------
st.title("🔒 Lockedin")

tab1, tab2 = st.tabs(["Workout", "Calendar"])

# -----------------------------
# WORKOUT TAB
# -----------------------------
with tab1:
    st.header("Workout")

    workout_name = st.text_input("Workout name", placeholder="Back, Chest, Legs...")
    workout_date = st.date_input("Workout date", value=date.today())

    st.subheader("Add Exercise")

    ex_name = st.text_input("Exercise name", placeholder="Row Machine")

    mode = st.radio("Tracking mode", ["Plates", "Weight"], horizontal=True)

    if mode == "Plates":
        value = st.number_input("Plates", min_value=0, step=1)
    else:
        value = st.number_input("Weight (lbs)", min_value=0, step=5)

    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)

    if st.button("Add Exercise to Workout"):
        key = workout_date.isoformat()

        if key not in st.session_state.workouts:
            st.session_state.workouts[key] = {
                "name": workout_name,
                "exercises": []
            }

        st.session_state.workouts[key]["exercises"].append({
            "name": ex_name,
            "mode": mode,
            "value": value,
            "sets": sets,
            "reps": reps
        })

        st.success(f"Added {ex_name}")

    # Preview current workout
    if workout_date.isoformat() in st.session_state.workouts:
        st.subheader("Current Workout")
        workout = st.session_state.workouts[workout_date.isoformat()]

        st.markdown(f"**{workout['name']}**")

        for ex in workout["exercises"]:
            unit = "plates" if ex["mode"] == "Plates" else "lbs"
            st.write(
                f"- {ex['name']}: {ex['value']} {unit}, "
                f"{ex['sets']} sets of {ex['reps']}"
            )

# -----------------------------
# CALENDAR TAB
# -----------------------------
with tab2:
    st.header("Calendar")

    if not st.session_state.workouts:
        st.info("No workouts logged yet.")
    else:
        for day, workout in sorted(st.session_state.workouts.items(), reverse=True):
            st.subheader(day)
            st.markdown(f"**Workout:** {workout['name']}")

            for ex in workout["exercises"]:
                unit = "plates" if ex["mode"] == "Plates" else "lbs"
                st.write(
                    f"- {ex['name']}: {ex['value']} {unit}, "
                    f"{ex['sets']} x {ex['reps']}"
                )
