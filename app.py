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

    workout_name = st.text_input(
        "Workout name",
        placeholder="Back, Chest, Legs"
    )

    workout_date = st.date_input(
        "Workout date",
        value=date.today()
    )

    st.divider()
    st.subheader("Add Exercise")

    ex_name = st.text_input(
        "Exercise name",
        placeholder="Row Machine"
    )

    mode = st.radio(
        "Tracking method",
        ["Plates", "Weight"],
        horizontal=True
    )

    if mode == "Plates":
        value = st.number_input("Plates", min_value=0, step=1)
    else:
        value = st.number_input("Weight (lbs)", min_value=0, step=5)

    sets = st.number_input("Sets", min_value=1, step=1)
    reps = st.number_input("Reps", min_value=1, step=1)

    notes = st.text_input(
        "Notes (optional)",
        placeholder="Optional"
    )

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

    # Live workout preview
    if st.session_state.current_exercises:
        st.subheader("Workout Preview")

        for ex in st.session_state.current_exercises:
            unit = "plates" if ex["mode"] == "Plates" else "lbs"
            st.markdown(
                f"""
                **{ex['name']}**  
                {ex['value']} {unit} — {ex['sets']} x {ex['reps']}  
                <small>{ex['notes']}</small>
                """,
                unsafe_allow_html=True
            )

    if st.button("💾 Save Workout"):
        if workout_name and st.session_state.current_exercises:
            key = workout_date.isoformat()
            st.session_state.workouts[key] = {
                "name": workout_name,
                "exercises": st.session_state.current_exercises.copy()
            }
            st.session_state.current_exercises.clear()
            st.success("Workout saved to calendar")

# =============================
# CALENDAR TAB (DESK CALENDAR)
# =============================
with tab2:
    st.header("Calendar")

    today = date.today()
    year = today.year
    month = today.month

    month_name = calendar.month_name[month]

    st.markdown(
        f"<h2 style='text-align:center;'>{month_name} {year}</h2>",
        unsafe_allow_html=True
    )

    cal = calendar.Calendar(calendar.SUNDAY).monthdayscalendar(year, month)

    html = """
    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        background: #ccc;
        gap: 1px;
    }
    .day-header {
        background: #f3f3f3;
        text-align: center;
        font-weight: bold;
        padding: 10px;
        border: 1px solid #bbb;
    }
    .day-cell {
        background: white;
        min-height: 110px;
        padding: 6px;
        border: 1px solid #bbb;
        font-size: 12px;
        position: relative;
    }
    .day-number {
        font-weight: bold;
        font-size: 14px;
    }
    .workout {
        margin-top: 6px;
        font-size: 11px;
        background: #e8f0ff;
        padding: 4px;
        border-radius: 4px;
    }
    </style>

    <div class="calendar">
    """

    # Day headers
    for day in ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]:
        html += f"<div class='day-header'>{day}</div>"

    # Calendar days
    for week in cal:
        for day in week:
            if day == 0:
                html += "<div class='day-cell'></div>"
            else:
                date_key = date(year, month, day).isoformat()
                workout = st.session_state.workouts.get(date_key)

                workout_html = (
                    f"<div class='workout'>{workout['name']}</div>"
                    if workout else ""
                )

                html += f"""
                <div class='day-cell'>
                    <div class='day-number'>{day}</div>
                    {workout_html}
                </div>
                """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)
