import groq

def get_ai_suggestions(api_key, data_summary):
    if not api_key:
        return "Please add your Groq API key in the sidebar to get AI-powered suggestions."
    try:
        client = groq.Groq(api_key=api_key)
        prompt = f"""
        You are a helpful student productivity assistant for a B.Tech CSE student. Your goal is to provide actionable advice based on the user's recent activity. Do not be generic. Use the data provided to make specific, encouraging, and helpful recommendations.
        Here is the user's data summary for the last 7 days:
        {data_summary}
        Based on this, what are 3-5 concise, actionable suggestions for improvement? For example, if a student is spending a lot of time on 'Projects' but an 'Exam' is near, suggest they allocate more time to exam preparation. If they are not logging any 'Fitness' activities, gently remind them of its importance. Frame your advice positively. Format the output as a markdown list.
        """
        chat_completion = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama3-8b-8192")
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while fetching AI suggestions: {e}"

def get_deep_analysis(api_key, user_question, data_summary):
    if not api_key:
        return "Please add your Groq API key to use the Deep Analysis feature."

    try:
        client = groq.Groq(api_key=api_key)
        prompt = f"""
        You are a data analyst and productivity coach for a B.Tech CSE student.
        The user has asked a specific question about their performance.
        Your task is to provide a detailed, data-driven answer based on their activity history.

        USER'S QUESTION: "{user_question}"

        AVAILABLE DATA:
        {data_summary}

        Please provide a clear, well-structured analysis that directly answers the user's question.
        Use the data to support your points. You can identify trends, patterns, and potential areas for improvement.
        Start by directly addressing the question, then provide supporting evidence and conclude with actionable recommendations.
        Format your response using markdown for readability (e.g., use headings, lists, bold text).
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the analysis: {e}"
