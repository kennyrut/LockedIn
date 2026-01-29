import streamlit as st
from datetime import date
import calendar

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Lockedin Fitness", layout="centered")
st.title("🔒 Lockedin Fitness")

# -----------------------------
# Session State
# -----------------------------
if "workouts" not in st.session_state:
    # { "YYYY-MM-DD": [ workout_session, workout_session ] }
    st.session_state.workouts = {}

if "current_exercises" not in st.session_state:
    st.session_state.current_exercises = []

if "selected_day" not in st.session_state:
    st.session_state.selected_day = None

if "reuse_template" not in st.session_state:
    st.session_state.reuse_template = None

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Workout", "Calendar"])

# =============================
# WORKOUT TAB
# =============================
with tab1:
    st.header("Create Workout")

    workout_name = st.text_input("Workout name", placeholder="Back / Chest / Legs")
    workout_date = st.date_input("Workout date", value=date.today())

    # If reusing a workout
    if st.session_state.reuse_template:
        workout_name = st.session_state.reuse_template["name"]
        st.session_state.current_exercises = [
            {
                **ex,
                "value": 0,
                "sets": ex["sets"],
                "reps": ex["reps"]
            }
            for ex in st.session_state.reuse_template["exercises"]
        ]
        st.session_state.reuse_template = None
        st.info("Workout loaded — values reset")

    st.divider()
    st.subheader("Add Exercise")

    ex_name = st.text_input("Exercise name")
    mode = st.radio("Tracking method", ["Plates", "Weight"], horizontal=True)

    value = st.number_input("Weight / Plates", min_value=0, step=5)
    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)
    notes = st.text_input("Notes (optional)")

    if st.button("➕ Add Exercise"):
        if ex_name:
            st.session_state.current_exercises.append({
                "name": ex_name,
                "mode": mode,
                "value": value,
                "sets": sets,
                "reps": reps,
                "notes": notes
            })

    if st.session_state.current_exercises:
        st.subheader("Workout Preview")
        for ex in st.session_state.current_exercises:
            unit = "plates" if ex["mode"] == "Plates" else "lbs"
            st.write(f"**{ex['name']}** — {ex['value']} {unit}, {ex['sets']} x {ex['reps']}")
            if ex["notes"]:
                st.caption(ex["notes"])

    if st.button("💾 Save Workout"):
        if workout_name and st.session_state.current_exercises:
            key = workout_date.isoformat()
            workout_entry = {
                "name": workout_name,
                "exercises": st.session_state.current_exercises.copy()
            }
            st.session_state.workouts.setdefault(key, []).append(workout_entry)
            st.session_state.current_exercises.clear()
            st.success("Workout saved")

# =============================
# CALENDAR TAB
# =============================
with tab2:
    st.header("Training Calendar")

    today = date.today()
    year = today.year
    month = today.month
    month_name = calendar.month_name[month]

    cal = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(year, month)

    st.markdown(
        """
        <style>
        .day-box {
            border: 1px solid #333;
            padding: 8px;
            min-height: 90px;
            background: #111;
            color: white;
            cursor: pointer;
        }
        .filled {
            border: 2px solid #ff4b4b;
        }
        .badge {
            font-size: 11px;
            background: #ff4b4b;
            padding: 2px 6px;
            margin-top: 4px;
            display: inline-block;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader(f"{month_name} {year}")

    cols = st.columns(7)
    for d in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]:
        cols[["SUN","MON","TUE","WED","THU","FRI","SAT"].index(d)].markdown(f"**{d}**")

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].markdown("")
            else:
                key = date(year, month, day).isoformat()
                workouts = st.session_state.workouts.get(key, [])

                label = f"{day}"
                if workouts:
                    label += f" 🔥 {len(workouts)}"

                if cols[i].button(label, key=f"day-{key}"):
                    st.session_state.selected_day = key

    # =============================
    # DAY DETAIL VIEW
    # =============================
    if st.session_state.selected_day:
        st.divider()
        st.subheader(f"Workouts on {st.session_state.selected_day}")

        day_workouts = st.session_state.workouts.get(st.session_state.selected_day, [])

        for idx, w in enumerate(day_workouts):
            with st.expander(w["name"], expanded=False):
                for ex in w["exercises"]:
                    unit = "plates" if ex["mode"] == "Plates" else "lbs"
                    st.write(
                        f"- **{ex['name']}** — {ex['value']} {unit}, {ex['sets']} x {ex['reps']}"
                    )
                    if ex["notes"]:
                        st.caption(ex["notes"])

                if st.button("🔁 Use This Workout Again", key=f"reuse-{idx}"):
                    st.session_state.reuse_template = w
                    st.session_state.selected_day = None
                    st.switch_page(st.session_state._main_script_path)
