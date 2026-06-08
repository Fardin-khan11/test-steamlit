import streamlit as st
import database as db
import pandas as pd

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.user

st.title("📚 Subjects Management")
st.caption("Manage your courses and tracking their difficulty.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Add New Subject")
    with st.form("add_subject_form", clear_on_submit=True):
        name = st.text_input("Subject Name")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        exam_date = st.date_input("Exam Date (Optional)", value=None)
        study_hours = st.number_input("Target Weekly Study Hours", min_value=0.5, value=2.0, step=0.5)
        
        submit = st.form_submit_button("➕ Add Subject", use_container_width=True)
        if submit:
            if not name:
                st.error("Subject name is required.")
            else:
                formatted_date = exam_date.strftime("%Y-%m-%d") if exam_date else ""
                db.add_subject(user["id"], name, difficulty, formatted_date, study_hours)
                st.success(f"Added subject '{name}'.")
                st.rerun()

with col2:
    st.subheader("Your Subjects")
    subjects = db.get_subjects(user["id"])
    
    if not subjects:
        st.info("No subjects added yet. Add a subject from the left panel.")
    else:
        # Display as a dataframe
        df = pd.DataFrame(subjects, columns=["ID", "User ID", "Subject Name", "Difficulty", "Exam Date", "Study Hours", "Created At"])
        display_df = df[["ID", "Subject Name", "Difficulty", "Exam Date", "Study Hours"]]
        
        st.dataframe(display_df, hide_index=True, use_container_width=True)
        
        # Delete Subject
        st.subheader("Actions")
        action_col1, action_col2 = st.columns([3, 1])
        with action_col1:
            subject_to_delete = st.selectbox("Select subject to delete", display_df["Subject Name"])
        with action_col2:
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("🗑️ Delete", type="primary", use_container_width=True):
                sub_id_to_delete = df[df["Subject Name"] == subject_to_delete]["ID"].values[0]
                db.delete_subject(sub_id_to_delete)
                st.success(f"Deleted {subject_to_delete}")
                st.rerun()
