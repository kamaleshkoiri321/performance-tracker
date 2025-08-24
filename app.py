import streamlit as st
from streamlit_option_menu import option_menu
from utils.database import setup_database

# Import page functions with their new names
from pages.Dashboard import page_dashboard
from pages.Add_Activity import page_add_activity
from pages.Add_Goal import page_add_goal
from pages.Add_Exam import page_add_exam
from pages.Daily_Routine import page_daily_routine
from pages.History import page_history
from pages.Analytics import page_analytics
from pages.Deep_Analysis import page_deep_analysis

# --- MAIN APP CONFIG ---
def main():
    st.set_page_config(
        page_title="Performance Tracker",
        page_icon="👨‍💻",
        layout="wide"
    )

    # Initialize the database
    setup_database()

    # --- TOP NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Add Activity", "Add Goal", "Add Exam", "Daily Routine", "History", "Analytics", "Deep Analysis"],
        icons=["house", "pencil-square", "bullseye", "calendar-check", "clock", "book", "bar-chart", "search"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    # --- PAGE ROUTING ---
    if selected == "Dashboard":
        page_dashboard()
    elif selected == "Add Activity":
        page_add_activity()
    elif selected == "Add Goal":
        page_add_goal()
    elif selected == "Add Exam":
        page_add_exam()
    elif selected == "Daily Routine":
        page_daily_routine()
    elif selected == "History":
        page_history()
    elif selected == "Analytics":
        page_analytics()
    elif selected == "Deep Analysis":
        page_deep_analysis()


if __name__ == "__main__":
    main()
