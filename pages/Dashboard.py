import streamlit as st
import database as db
import random
from utils.helpers import MOTIVATIONAL_QUOTES, apply_global_styles
import pandas as pd
import plotly.express as px

# Protect page
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

st.title("📊 Dashboard")
user = st.session_state.user
st.markdown(f"**Welcome back, {user['username']}!**")
st.caption(random.choice(MOTIVATIONAL_QUOTES))

# Fetch stats
subjects = db.get_subjects(user["id"])
total, completed, pending = db.get_task_stats(user["id"])
reminders = db.get_reminders(user["id"])

# Top stat cards
st.markdown("<div class='stat-card-container'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="stat-card bg-indigo">
            <div class="stat-title">Total Subjects</div>
            <div class="stat-value">{}</div>
        </div>
    """.format(len(subjects)), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-card bg-emerald">
            <div class="stat-title">Tasks Completed</div>
            <div class="stat-value">{}</div>
        </div>
    """.format(completed), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-card bg-amber">
            <div class="stat-title">Tasks Pending</div>
            <div class="stat-value">{}</div>
        </div>
    """.format(pending), unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="stat-card bg-red">
            <div class="stat-title">Active Reminders</div>
            <div class="stat-value">{}</div>
        </div>
    """.format(len([r for r in reminders if r["status"] == "Active"])), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Progress Overview")
    if total > 0:
        # Create a pie chart
        df_chart = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [completed, pending]
        })
        fig = px.pie(df_chart, values="Count", names="Status", color="Status",
                     color_discrete_map={"Completed": "#10b981", "Pending": "#f59e0b"},
                     hole=0.4)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tasks to display progress chart. Go to 'Progress' to add some tasks.")

with col2:
    st.subheader("Upcoming Exams")
    exam_subjects = [s for s in subjects if s["exam_date"]]
    if exam_subjects:
        for s in exam_subjects[:5]:
            st.markdown(f"""
                <div class="custom-card" style="margin-bottom: 0.5rem; padding: 1rem;">
                    <strong>{s['subject_name']}</strong><br/>
                    <span style='color: #94a3b8; font-size: 0.9em;'>📅 {s['exam_date']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No upcoming exams scheduled.")
