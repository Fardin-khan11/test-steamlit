# config.py - Application configuration

import os

# Base paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
CSS_PATH = os.path.join(ASSETS_DIR, "css", "styles.css")
DATABASE_DIR = os.path.join(ROOT_DIR, "database")

# App parameters
APP_NAME = "Smart Study Planner Pro"
APP_VERSION = "1.0.0"

# Color mappings aligning with ttkbootstrap's darkly theme
COLORS = {
    "sidebar_bg": "#1a1d2e",
    "content_bg": "#0f1117",
    "card_bg": "#1a1d2e",
    "accent_blue": "#4f46e5",
    "accent_purple": "#7c3aed",
    "accent_green": "#10b981",
    "accent_orange": "#f59e0b",
    "accent_red": "#ef4444",
    "text_primary": "#e2e8f0"
}
