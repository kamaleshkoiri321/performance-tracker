import streamlit as st
from utils.database import fetch_all_data

def page_history():
    st.header("📚 Activity History")
    activities_df = fetch_all_data("activities")
    if activities_df.empty:
        st.warning("No activities found.")
        return
    st.sidebar.header("Filter History")
    search_query = st.sidebar.text_input("Search by Title or Notes")

    # Check if 'category' column exists before using it
    if 'category' in activities_df.columns:
        categories = activities_df['category'].unique()
        selected_category = st.sidebar.multiselect("Filter by Category", options=categories, default=list(categories))
    else:
        selected_category = []

    # Basic search functionality
    filtered_df = activities_df[
        activities_df['title'].str.contains(search_query, case=False, na=False) |
        activities_df['notes'].str.contains(search_query, case=False, na=False)
    ]

    if selected_category and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]

    st.dataframe(filtered_df, use_container_width=True)

    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("Export to CSV", csv, "activity_history.csv", "text/csv")

# Run the page
page_history()
