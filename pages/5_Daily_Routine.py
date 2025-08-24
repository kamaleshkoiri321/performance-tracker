import streamlit as st
import pandas as pd
from datetime import time
from utils.database import fetch_all_data, add_routine_item_to_db, delete_routine_item_from_db

def page_daily_routine():
    st.set_page_config(page_icon="⏰")
    st.header("⏰ Build Your Daily Routine")
    st.write("Plan your day for maximum productivity. Add tasks and schedule them.")

    # Form to add a new routine item
    with st.form("new_routine_item_form", clear_on_submit=True):
        st.subheader("Add New Routine Item")
        item_title = st.text_input("Task Title (e.g., 'Wake up', 'DSA Practice')")
        item_time = st.time_input("Scheduled Time")
        submitted = st.form_submit_button("Add Item")

        if submitted:
            if item_title:
                add_routine_item_to_db(item_title, item_time)
                st.success(f"'{item_title}' added to your routine!")
            else:
                st.error("Please enter a title for the routine item.")

    # Display the current routine
    st.subheader("Your Current Routine")
    routine_df = fetch_all_data("routines")

    if routine_df.empty:
        st.info("Your routine is empty. Add some items to get started.")
    else:
        # Sort by time
        routine_df['scheduled_time'] = pd.to_datetime(routine_df['scheduled_time'], format='%H:%M:%S').dt.time
        routine_df = routine_df.sort_values(by='scheduled_time')

        # Display in a more charming way
        for index, row in routine_df.iterrows():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.write(f"**{row['scheduled_time'].strftime('%H:%M')}**")
            with col2:
                st.write(row['title'])
            with col3:
                if st.button(f"Delete", key=f"del_{row['id']}"):
                    delete_routine_item_from_db(row['id'])
                    st.rerun()

# Run the page
page_daily_routine()
