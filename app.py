import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, time
import os
import groq

# --- CONFIG and SECRETS ---
# It's recommended to use st.secrets for API keys in Streamlit Cloud
try:
    GROQ_API_KEY_SECRET = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    GROQ_API_KEY_SECRET = ""

# --- DATABASE SETUP ---
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
    conn.commit()
    conn.close()

# --- DATABASE HELPER FUNCTIONS ---
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

def fetch_upcoming_exams():
    conn = get_db_connection()
    query = "SELECT * FROM exams WHERE exam_date >= date('now') ORDER BY exam_date ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- AI ASSISTANT ---
def get_ai_suggestions(api_key, data_summary):
    if not api_key:
        return "Please add your Groq API key in the sidebar to get AI-powered suggestions."
    try:
        client = groq.Groq(api_key=api_key)
        prompt = f"""
        You are a helpful student productivity assistant for a B.Tech CSE student. Your goal is to provide actionable advice based on the user's recent activity. Do not be generic. Use the data provided to make specific, encouraging, and helpful recommendations.
        Here is the user's data summary for the last 7 days:
        {data_summary}
        Based on this, what are 3-5 concise, actionable suggestions for improvement? For example, if a student is spending a lot of time on 'Projects' but an 'Exam' is near, suggest they allocate more time to exam preparation. If they are not logging any 'Fitness' activities, gently remind them of its importance. Frame your advice positively. Format the output as a markdown list.
        """
        chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama3-8b-8192")
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while fetching AI suggestions: {e}"

# --- UI PAGE FUNCTIONS ---
def page_dashboard(api_key):
    st.header("Dashboard")
    activities_df = fetch_all_data("activities")
    exams_df = fetch_upcoming_exams()

    st.subheader("🤖 AI-Powered Suggestions")
    if not activities_df.empty:
        recent_activities = activities_df[pd.to_datetime(activities_df['date']) > (datetime.now() - pd.Timedelta(days=7))]
        summary_text = f"- Recent Activities ({len(recent_activities)} entries):\n{recent_activities[['title', 'category', 'time_spent']].to_string(index=False)}\n- Upcoming Exams ({len(exams_df)}):\n{exams_df[['subject', 'exam_date']].to_string(index=False)}"
        with st.spinner("Generating suggestions..."):
            suggestions = get_ai_suggestions(api_key, summary_text)
            st.markdown(suggestions)
    else:
        st.info("Log some activities to start receiving personalized suggestions.")

    st.subheader("Upcoming Exams")
    if not exams_df.empty:
        st.dataframe(exams_df[['subject', 'exam_date', 'notes']], use_container_width=True)
    else:
        st.info("No upcoming exams scheduled. You can add them from the 'Add Exam' page.")

def page_add_activity():
    st.header("Add a New Activity")
    with st.form("activity_form", clear_on_submit=True):
        title = st.text_input("Title", help="What did you do?")
        category = st.selectbox("Category", ["Academic", "Personal", "Projects", "DSA Practice", "Exams", "Fitness", "Hobbies", "Other"])
        date = st.date_input("Date", datetime.now())
        time_spent = st.number_input("Time Spent (in minutes)", min_value=0, step=15)
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        notes = st.text_area("Notes", help="Add any details or reflections here.")
        if st.form_submit_button("Add Activity"):
            if title:
                add_activity_to_db(title, category, date, time_spent, priority, notes)
                st.success("Activity added successfully!")
            else:
                st.error("Title is a required field.")

def page_add_goal():
    st.header("Set a New Goal")
    with st.form("goal_form", clear_on_submit=True):
        title = st.text_input("Goal Title", help="What do you want to achieve?")
        category = st.selectbox("Category", ["Academic", "Personal", "Projects", "DSA Practice", "Fitness", "Career"])
        deadline = st.date_input("Deadline", min_value=datetime.now())
        status = st.selectbox("Initial Status", ["Not Started", "In-Progress"])
        if st.form_submit_button("Add Goal"):
            if title:
                add_goal_to_db(title, category, deadline, status)
                st.success("Goal added successfully!")
            else:
                st.error("Title is a required field.")

def page_add_exam():
    st.header("Schedule a New Exam")
    with st.form("exam_form", clear_on_submit=True):
        subject = st.text_input("Subject/Course Name")
        exam_date = st.date_input("Exam Date", min_value=datetime.now().date())
        exam_time = st.time_input("Exam Time")
        notes = st.text_area("Notes", help="Add details like syllabus, location, etc.")
        if st.form_submit_button("Add Exam"):
            if subject:
                exam_datetime = datetime.combine(exam_date, exam_time)
                add_exam_to_db(subject, exam_datetime, notes)
                st.success(f"Exam for {subject} on {exam_datetime.strftime('%Y-%m-%d %H:%M')} added!")
            else:
                st.error("Subject is a required field.")

def page_analytics():
    st.header("Performance Analytics")
    activities_df = fetch_all_data("activities")
    if activities_df.empty or activities_df['time_spent'].sum() == 0:
        st.warning("Not enough data to generate analytics. Add activities with time spent.")
        return
    activities_df['date'] = pd.to_datetime(activities_df['date'])
    st.subheader("Time Spent per Category")
    time_per_category = activities_df.groupby('category')['time_spent'].sum().reset_index()
    fig_bar = px.bar(time_per_category, x='category', y='time_spent', title="Total Minutes Spent per Category")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.subheader("Activity Distribution")
    category_dist = activities_df['category'].value_counts().reset_index()
    fig_pie = px.pie(category_dist, names='category', values='count', title="Distribution of Activities")
    st.plotly_chart(fig_pie, use_container_width=True)
    st.subheader("Activity Trend Over Time")
    activities_df.set_index('date', inplace=True)
    weekly_summary = activities_df.resample('W-Mon')['time_spent'].sum().reset_index()
    fig_line = px.line(weekly_summary, x='date', y='time_spent', title="Weekly Time Spent", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

def page_history():
    st.header("Activity History")
    activities_df = fetch_all_data("activities")
    if activities_df.empty:
        st.warning("No activities found.")
        return
    st.sidebar.header("Filter History")
    search_query = st.sidebar.text_input("Search by Title or Notes")
    categories = activities_df['category'].unique()
    selected_category = st.sidebar.multiselect("Filter by Category", options=categories, default=list(categories))
    filtered_df = activities_df[
        (activities_df['title'].str.contains(search_query, case=False, na=False) |
         activities_df['notes'].str.contains(search_query, case=False, na=False)) &
        (activities_df['category'].isin(selected_category))
    ]
    st.dataframe(filtered_df, use_container_width=True)
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("Export to CSV", csv, "activity_history.csv", "text/csv")

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="Performance Tracker", layout="wide")
    st.title("👨‍💻 B.Tech CSE Performance Tracker & Analyzer")
    st.write("Welcome to your personal dashboard.")

    setup_database()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Activity", "Add Goal", "Add Exam", "Analytics", "History"])

    # Get API Key
    st.sidebar.header("AI Assistant")
    api_key_input = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get a free key from groq.com")

    # Use the key from input if provided, otherwise from secrets
    GROQ_API_KEY = api_key_input if api_key_input else GROQ_API_KEY_SECRET

    if page == "Dashboard":
        page_dashboard(GROQ_API_KEY)
    elif page == "Add Activity":
        page_add_activity()
    elif page == "Add Goal":
        page_add_goal()
    elif page == "Add Exam":
        page_add_exam()
    elif page == "Analytics":
        page_analytics()
    elif page == "History":
        page_history()

if __name__ == "__main__":
    main()
