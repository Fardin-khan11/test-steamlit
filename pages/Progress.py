import streamlit as st
import database as db
import pandas as pd
from datetime import date

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.user

st.title("📈 Progress Tracker")
st.caption("Track your daily tasks and study progress.")

subjects_data = db.get_subjects(user["id"])
subject_names = ["General"] + [s["subject_name"] for s in subjects_data]

tab1, tab2 = st.tabs(["Active Tasks", "Add New Task"])

tasks = db.get_tasks(user["id"])

with tab2:
    with st.form("add_task_form", clear_on_submit=True):
        st.subheader("New Task")
        task_name = st.text_input("Task Description")
        subject = st.selectbox("Related Subject", subject_names)
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
        task_date = st.date_input("Target Date", value=date.today())
        
        submit = st.form_submit_button("➕ Add Task", use_container_width=True)
        if submit:
            if not task_name:
                st.error("Task description required.")
            else:
                db.add_task(user["id"], task_name, subject, "Pending", priority, task_date.strftime("%Y-%m-%d"))
                st.success("Task added!")
                st.rerun()

with tab1:
    if not tasks:
        st.info("No tasks yet. Create one in the 'Add New Task' tab.")
    else:
        df = pd.DataFrame(tasks, columns=["ID", "User ID", "Task", "Subject", "Status", "Priority", "Date", "Created"])
        
        # Split into Pending and Completed
        pending_df = df[df["Status"] == "Pending"]
        completed_df = df[df["Status"] == "Completed"]
        
        st.subheader(f"Pending Tasks ({len(pending_df)})")
        if not pending_df.empty:
            for idx, row in pending_df.iterrows():
                with st.container(border=True):
                    col1, col2, col3 = st.columns([4, 2, 1])
                    with col1:
                        st.markdown(f"**{row['Task']}** (_{row['Subject']}_)")
                        st.caption(f"📅 {row['Date']}")
                    with col2:
                        color = "red" if row['Priority'] == "High" else "orange" if row['Priority'] == "Medium" else "green"
                        st.markdown(f"<span style='color:{color}'>Priority: {row['Priority']}</span>", unsafe_allow_html=True)
                    with col3:
                        if st.button("✅ Done", key=f"done_{row['ID']}", use_container_width=True):
                            db.update_task_status(row['ID'], "Completed")
                            st.rerun()
                        if st.button("🗑️", key=f"del_{row['ID']}", use_container_width=True):
                            db.delete_task(row['ID'])
                            st.rerun()
        else:
            st.success("All caught up! No pending tasks.")
            
        st.markdown("<br/>", unsafe_allow_html=True)
        with st.expander(f"Completed Tasks ({len(completed_df)})"):
            if not completed_df.empty:
                for idx, row in completed_df.iterrows():
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"~~{row['Task']}~~ (_{row['Subject']}_)")
                    with col2:
                        if st.button("🗑️", key=f"del_c_{row['ID']}", use_container_width=True):
                            db.delete_task(row['ID'])
                            st.rerun()
