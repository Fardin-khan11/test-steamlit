import streamlit as st
import os

def apply_global_styles():
    """Inject global CSS."""
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "css", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

MOTIVATIONAL_QUOTES = [
    "The secret of getting ahead is getting started. — Mark Twain",
    "Education is the most powerful weapon you can use to change the world. — Nelson Mandela",
    "The beautiful thing about learning is that no one can take it away from you. — B.B. King",
    "Success is the sum of small efforts, repeated day in and day out. — Robert Collier",
    "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
    "The expert in anything was once a beginner. — Helen Hayes",
    "Study hard, for the well is deep and our brains are shallow. — Richard Baxter",
    "The more that you read, the more things you will know. — Dr. Seuss",
    "An investment in knowledge pays the best interest. — Benjamin Franklin",
    "There are no shortcuts to any place worth going. — Beverly Sills",
]

def render_card(title, content):
    st.markdown(f'''
    <div class="custom-card">
        <h3>{title}</h3>
        <div>{content}</div>
    </div>
    ''', unsafe_allow_html=True)
