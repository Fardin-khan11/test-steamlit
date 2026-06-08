import streamlit as st
import database as db
from utils.helpers import apply_global_styles

def show_auth_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">📖 Smart Study Planner Pro</h1>
            <p style="font-size: 1.2rem; color: #a5b4fc;">Your AI-powered academic companion for success</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Create Account"])
        
        with tab1:
            st.markdown("### Welcome Back 👋")
            st.markdown("<p style='color:#94a3b8;margin-bottom:1rem;'>Sign in to your account</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In →", use_container_width=True)
                
                if submit:
                    if not username or not password:
                        st.warning("Please enter both username and password.")
                    else:
                        user = db.get_user(username)
                        if user is None:
                            st.error("Username not found. Please register first.")
                        elif user["password"] != db.hash_password(password):
                            st.error("Incorrect password. Please try again.")
                        else:
                            st.session_state.user = dict(user)
                            st.success(f"Welcome {username}!")
                            st.rerun()

        with tab2:
            st.markdown("### Create Account 🎓")
            st.markdown("<p style='color:#94a3b8;margin-bottom:1rem;'>Start your study journey today</p>", unsafe_allow_html=True)
            
            with st.form("register_form"):
                reg_username = st.text_input("Username")
                reg_password = st.text_input("Password", type="password")
                reg_confirm = st.text_input("Confirm Password", type="password")
                submit_reg = st.form_submit_button("Create Account →", use_container_width=True)
                
                if submit_reg:
                    if not reg_username or not reg_password or not reg_confirm:
                        st.warning("All fields are required.")
                    elif len(reg_username) < 3:
                        st.warning("Username must be at least 3 characters.")
                    elif len(reg_password) < 6:
                        st.warning("Password must be at least 6 characters.")
                    elif reg_password != reg_confirm:
                        st.error("Passwords do not match.")
                    else:
                        if db.create_user(reg_username, reg_password):
                            st.success("Account created successfully! You can now log in.")
                        else:
                            st.error("Username already exists. Please choose another.")
