import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import fetch_all_data, fetch_upcoming_exams
from utils.ai_assistant import get_ai_suggestions

def page_dashboard():
    """The main dashboard page with summary and UI enhancements."""
    st.set_page_config(page_icon="🏠")
    st.header("🏠 Dashboard")

    # Get API Key
    st.sidebar.header("AI Assistant")
    api_key_input = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get a free key from groq.com")

    try:
        GROQ_API_KEY_SECRET = st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, KeyError):
        GROQ_API_KEY_SECRET = ""

    GROQ_API_KEY = api_key_input if api_key_input else GROQ_API_KEY_SECRET

    # --- Data Loading ---
    activities_df = fetch_all_data("activities")
    exams_df = fetch_upcoming_exams()
    goals_df = fetch_all_data("goals")

    # --- Top Metrics ---
    st.subheader("At a Glance")
    total_activities = len(activities_df)
    completed_goals = len(goals_df[goals_df['status'] == 'Completed'])
    upcoming_exams_count = len(exams_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Activities Logged", total_activities)
    col2.metric("Completed Goals", completed_goals)
    col3.metric("Upcoming Exams", upcoming_exams_count)
    st.divider()

    # --- Main Dashboard Layout ---
    col_ai, col_exams = st.columns(2)

    with col_ai:
        st.subheader("🤖 AI-Powered Suggestions")
        if not activities_df.empty:
            recent_activities = activities_df[pd.to_datetime(activities_df['date']) > (datetime.now() - pd.Timedelta(days=7))]
            summary_text = f"- Recent Activities ({len(recent_activities)} entries):\n{recent_activities[['title', 'category', 'time_spent']].to_string(index=False)}\n- Upcoming Exams ({len(exams_df)}):\n{exams_df[['subject', 'exam_date']].to_string(index=False)}"
            with st.spinner("Generating suggestions..."):
                suggestions = get_ai_suggestions(GROQ_API_KEY, summary_text)
                st.markdown(suggestions)
        else:
            st.info("Log some activities to start receiving personalized suggestions.")

    with col_exams:
        st.subheader("🗓️ Upcoming Exams")
        if not exams_df.empty:
            st.dataframe(exams_df[['subject', 'exam_date', 'notes']], use_container_width=True)
        else:
            st.info("No upcoming exams scheduled. You can add them from the 'Add Exam' page.")

# Run the page
page_dashboard()
