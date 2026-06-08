import sqlite3
import os
import hashlib

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "study_planner.db")

def get_connection():
    """Return a new database connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Create all tables if they don't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'Medium',
                exam_date TEXT,
                study_hours REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Progress / Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                subject TEXT DEFAULT 'General',
                status TEXT DEFAULT 'Pending',
                priority TEXT DEFAULT 'Medium',
                date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Timetable table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                day TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration_hours REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Reminders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                message TEXT,
                reminder_date TEXT,
                reminder_time TEXT DEFAULT '08:00',
                status TEXT DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()

# ─────────────────────────── USER OPERATIONS ──────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def get_user(username: str):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def update_user_password(username: str, new_password: str):
    with get_connection() as conn:
        conn.execute("UPDATE users SET password=? WHERE username=?", (hash_password(new_password), username))
        conn.commit()

# ─────────────────────────── SUBJECT OPERATIONS ───────────────────────────
def add_subject(user_id, name, difficulty, exam_date, study_hours):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO subjects (user_id, subject_name, difficulty, exam_date, study_hours) VALUES (?,?,?,?,?)",
            (user_id, name, difficulty, exam_date, study_hours)
        )
        conn.commit()

def get_subjects(user_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM subjects WHERE user_id = ? ORDER BY exam_date ASC", (user_id,)).fetchall()

def update_subject(subject_id, name, difficulty, exam_date, study_hours):
    with get_connection() as conn:
        conn.execute(
            "UPDATE subjects SET subject_name=?, difficulty=?, exam_date=?, study_hours=? WHERE id=?",
            (name, difficulty, exam_date, study_hours, subject_id)
        )
        conn.commit()

def delete_subject(subject_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
        conn.commit()

# ─────────────────────────── PROGRESS OPERATIONS ──────────────────────────
def add_task(user_id, task_name, subject, status, priority, date):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO progress (user_id, task_name, subject, status, priority, date) VALUES (?,?,?,?,?,?)",
            (user_id, task_name, subject, status, priority, date)
        )
        conn.commit()

def get_tasks(user_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM progress WHERE user_id = ? ORDER BY date ASC", (user_id,)).fetchall()

def update_task_status(task_id, status):
    with get_connection() as conn:
        conn.execute("UPDATE progress SET status=? WHERE id=?", (status, task_id))
        conn.commit()

def delete_task(task_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM progress WHERE id=?", (task_id,))
        conn.commit()

def get_task_stats(user_id):
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM progress WHERE user_id=?", (user_id,)).fetchone()[0]
        completed = conn.execute("SELECT COUNT(*) FROM progress WHERE user_id=? AND status='Completed'", (user_id,)).fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM progress WHERE user_id=? AND status='Pending'", (user_id,)).fetchone()[0]
        return total, completed, pending

# ─────────────────────────── TIMETABLE OPERATIONS ─────────────────────────
def save_timetable(user_id, entries):
    with get_connection() as conn:
        conn.execute("DELETE FROM timetable WHERE user_id=?", (user_id,))
        for e in entries:
            conn.execute(
                "INSERT INTO timetable (user_id, day, time_slot, subject, duration_hours) VALUES (?,?,?,?,?)",
                (user_id, e["day"], e["time_slot"], e["subject"], e["duration_hours"])
            )
        conn.commit()

def get_timetable(user_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM timetable WHERE user_id=? ORDER BY id ASC", (user_id,)).fetchall()

# ─────────────────────────── REMINDER OPERATIONS ──────────────────────────
def add_reminder(user_id, title, message, reminder_date, reminder_time):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO reminders (user_id, title, message, reminder_date, reminder_time) VALUES (?,?,?,?,?)",
            (user_id, title, message, reminder_date, reminder_time)
        )
        conn.commit()

def get_reminders(user_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM reminders WHERE user_id=? ORDER BY reminder_date ASC", (user_id,)).fetchall()

def delete_reminder(reminder_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
        conn.commit()

def update_reminder_status(reminder_id, status):
    with get_connection() as conn:
        conn.execute("UPDATE reminders SET status=? WHERE id=?", (status, reminder_id))
        conn.commit()
