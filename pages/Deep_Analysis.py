import streamlit as st
import pandas as pd
from utils.database import fetch_all_data
from utils.ai_assistant import get_deep_analysis

def page_deep_analysis():
    st.header("🔍 Deep Analysis Assistant")
    st.write("Ask anything about your performance, and the AI will give you a detailed analysis.")

    # Get API Key
    st.sidebar.header("AI Assistant")
    api_key_input = st.sidebar.text_input("Enter Groq API Key", type="password", help="Get a free key from groq.com")

    try:
        GROQ_API_KEY_SECRET = st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, KeyError):
        GROQ_API_KEY_SECRET = ""

    GROQ_API_KEY = api_key_input if api_key_input else GROQ_API_KEY_SECRET

    activities_df = fetch_all_data("activities")

    if activities_df.empty:
        st.warning("You don't have any activity data to analyze yet.")
        return

    # User input
    default_question = "How has my time distribution been over the last month, and where can I improve?"
    user_question = st.text_area("Your question:", value=default_question, height=100)

    if st.button("Analyze My Performance"):
        if not GROQ_API_KEY:
            st.error("Please enter your Groq API key in the sidebar to run the analysis.")
        elif not user_question.strip():
            st.error("Please enter a question before analyzing.")
        else:
            with st.spinner("Performing deep analysis... This may take a moment."):
                # Prepare data summary
                data_summary = f"Here is a summary of all activities logged:\n{activities_df.to_string()}"

                # Get analysis from AI
                analysis_result = get_deep_analysis(GROQ_API_KEY, user_question, data_summary)

                st.subheader("Analysis Report")
                st.markdown(analysis_result)

# The main app.py handles the calling of this function
