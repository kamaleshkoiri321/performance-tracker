import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import fetch_all_data

def page_analytics():
    st.header("📊 Performance Analytics")
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

# The main app.py handles the calling of this function
