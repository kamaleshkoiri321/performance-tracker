import streamlit as st
from datetime import datetime
from utils.database import add_exam_to_db

def page_add_exam():
    st.header("📅 Schedule a New Exam")
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

# Run the page
page_add_exam()
