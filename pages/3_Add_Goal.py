import streamlit as st
from datetime import datetime
from utils.database import add_goal_to_db

def page_add_goal():
    st.set_page_config(page_icon="🎯")
    st.header("🎯 Set a New Goal")
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

# Run the page
page_add_goal()
