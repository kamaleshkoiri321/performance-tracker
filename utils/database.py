import sqlite3
import pandas as pd

DB_FILE = "performance_tracker.db"

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Initializes the database and creates tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()
    # Activities Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            date DATE NOT NULL,
            time_spent INTEGER, -- in minutes
            priority TEXT,
            notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Goals Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            deadline DATE,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Exams Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            exam_date DATETIME NOT NULL,
            notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Routines Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            scheduled_time TIME NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_activity_to_db(title, category, date, time_spent, priority, notes):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO activities (title, category, date, time_spent, priority, notes) VALUES (?, ?, ?, ?, ?, ?)", (title, category, date, time_spent, priority, notes))
    conn.commit()
    conn.close()

def add_goal_to_db(title, category, deadline, status):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO goals (title, category, deadline, status) VALUES (?, ?, ?, ?)", (title, category, deadline, status))
    conn.commit()
    conn.close()

def add_exam_to_db(subject, exam_date, notes):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO exams (subject, exam_date, notes) VALUES (?, ?, ?)", (subject, exam_date, notes))
    conn.commit()
    conn.close()

def fetch_all_data(table_name):
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_routine_item_to_db(title, scheduled_time):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO routines (title, scheduled_time) VALUES (?, ?)", (title, scheduled_time))
    conn.commit()
    conn.close()

def delete_routine_item_from_db(item_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM routines WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def fetch_upcoming_exams():
    conn = get_db_connection()
    query = "SELECT * FROM exams WHERE exam_date >= date('now') ORDER BY exam_date ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
