import streamlit as st
from utils.database import setup_database

# --- MAIN APP CONFIG ---
def main():
    st.set_page_config(
        page_title="Performance Tracker",
        page_icon="👨‍💻",
        layout="wide"
    )

    st.title("👨‍💻 B.Tech CSE Performance Tracker & Analyzer")
    st.write("Welcome! Use the sidebar to navigate through the app sections.")

    # Initialize the database
    setup_database()

    st.info("Select a page from the sidebar to get started.", icon="👈")

if __name__ == "__main__":
    main()
