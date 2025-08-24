import streamlit as st
from datetime import datetime
from utils.database import add_activity_to_db

def page_add_activity():
    st.set_page_config(page_icon="✍️")
    st.header("✍️ Add a New Activity")
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

# Run the page
page_add_activity()
