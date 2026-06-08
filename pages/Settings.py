import streamlit as st
import database as db

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please log in to access this page.")
    st.stop()

user = st.session_state.user

st.title("⚙️ Settings")
st.caption("Manage your account and preferences.")

st.subheader("Account Information")
st.markdown(f"**Username:** {user['username']}")

st.divider()

st.subheader("Change Password")
with st.form("change_password_form"):
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    submit = st.form_submit_button("Update Password")
    
    if submit:
        if not current_password or not new_password or not confirm_password:
            st.warning("All fields are required.")
        elif db.hash_password(current_password) != user['password']:
            st.error("Current password is incorrect.")
        elif len(new_password) < 6:
            st.error("New password must be at least 6 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            db.update_user_password(user['username'], new_password)
            # Update session user dict
            user['password'] = db.hash_password(new_password)
            st.success("Password updated successfully!")

st.divider()

st.subheader("Danger Zone")
if st.button("🚪 Logout", type="primary"):
    st.session_state.user = None
    st.rerun()
