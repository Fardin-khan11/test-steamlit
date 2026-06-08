import streamlit as st
from database import initialize_database
from auth import show_auth_page
import urllib.parse
from utils.helpers import apply_global_styles

st.set_page_config(
    page_title="Smart Study Planner Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize DB on first load
if "db_initialized" not in st.session_state:
    initialize_database()
    st.session_state.db_initialized = True

# Add Custom CSS
apply_global_styles()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    # Hide sidebar when not logged in (using some hacky CSS, or just let users see login)
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] { display: none; }
            [data-testid="stSidebar"] { display: none; }
        </style>
    """, unsafe_allow_html=True)
    show_auth_page()
else:
    # Show main application
    pages = {
        "Menu": [
            st.Page("pages/Dashboard.py", title="Dashboard", icon="📊"),
            st.Page("pages/Subjects.py", title="Subjects", icon="📚"),
            st.Page("pages/Timetable.py", title="Timetable", icon="📅"),
            st.Page("pages/Progress.py", title="Progress", icon="📈"),
            st.Page("pages/Reminders.py", title="Reminders", icon="🔔"),
            st.Page("pages/Settings.py", title="Settings", icon="⚙️"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()
