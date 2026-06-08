import streamlit as st
import database as db
import pandas as pd
from datetime import date, datetime

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.user

st.title("🔔 Exam Reminders")
st.caption("Never miss an important date or deadline.")

reminders = db.get_reminders(user["id"])

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Add Reminder")
    with st.form("add_reminder_form", clear_on_submit=True):
        title = st.text_input("Title (e.g. Math Midterm)")
        message = st.text_area("Details", height=100)
        reminder_date = st.date_input("Date", value=date.today())
        reminder_time = st.time_input("Time", value=datetime.strptime('08:00', '%H:%M').time())
        
        submit = st.form_submit_button("➕ Add Reminder", use_container_width=True)
        if submit:
            if not title:
                st.error("Title is required.")
            else:
                formatted_date = reminder_date.strftime("%Y-%m-%d")
                formatted_time = reminder_time.strftime("%H:%M")
                db.add_reminder(user["id"], title, message, formatted_date, formatted_time)
                st.success("Reminder added!")
                st.rerun()

with col2:
    st.subheader("Your Reminders")
    
    if not reminders:
        st.info("No active reminders.")
    else:
        for r in reminders:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    status = "✅" if r["status"] == "Completed" else "⏳"
                    st.markdown(f"#### {status} {r['title']}")
                    st.markdown(f"**Date:** {r['reminder_date']} at {r['reminder_time']}")
                    if r["message"]:
                        st.caption(r["message"])
                with c2:
                    if r["status"] != "Completed":
                        if st.button("Mark done", key=f"rdone_{r['ID']}", use_container_width=True):
                            db.update_reminder_status(r["ID"], "Completed")
                            st.rerun()
                    if st.button("Delete", key=f"rdel_{r['ID']}", use_container_width=True):
                        db.delete_reminder(r["ID"])
                        st.rerun()
