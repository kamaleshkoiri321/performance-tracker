# B.Tech CSE Performance Tracker & Analyzer v2.0

This is a powerful, multi-page Streamlit web application designed to help a B.Tech CSE student track activities, manage goals, build a daily routine, and gain deep, AI-powered insights into their performance. This project has been refactored for better organization and includes several new features.

## ✨ Features

- **🏠 Dashboard**: A central hub with an at-a-glance summary, AI-powered suggestions from Groq (LLaMA 3), and reminders for upcoming exams.
- **✍️ Add Activity**: Log daily activities like studying, projects, fitness, etc.
- **🎯 Add Goal**: Set short-term and long-term goals to stay focused.
- **📅 Add Exam**: Keep track of exam schedules.
- **⏰ Daily Routine**: A new page to build and manage your ideal daily schedule.
- **📚 History**: A searchable and filterable log of all your past activities.
- **📊 Analytics**: Visualize your performance with interactive charts (time per category, activity distribution, trends).
- **🔍 Deep Analysis**: A new AI-powered page where you can ask natural language questions about your performance and get a detailed, data-driven report.
- **🗃️ Data Persistence**: All data is stored locally in a SQLite database (`performance_tracker.db`).
- **📁 Refactored Code**: The codebase is now organized into a multi-page app structure, making it easier to maintain and extend.

## 🛠️ Tech Stack

- **Framework**: Streamlit (Multi-page)
- **Language**: Python
- **Database**: SQLite
- **Data Analysis**: Pandas
- **Plotting**: Plotly
- **AI**: Groq API (LLaMA 3)

## 🚀 How to Run Locally

### 1. Prerequisites

- Python 3.7+
- `pip` for package installation

### 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Create a Virtual Environment (Recommended)

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Get a Groq API Key

The AI features are powered by the Groq API.
1.  Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2.  Sign up for a free account.
3.  Create a new API key and copy it.

### 6. Run the Application

The app is now a multi-page application. The main entry point is `app.py`.

```bash
streamlit run app.py
```

The application will open in your default web browser. You can navigate between pages using the sidebar. You can enter your Groq API key in the sidebar to enable the AI features.

## ☁️ How to Deploy to Streamlit Cloud

Streamlit Cloud is the ideal platform for this app.

### 1. Push Your Code to a GitHub Repository

Ensure your entire project structure (`app.py`, `requirements.txt`, the `pages/` directory, the `utils/` directory, and this `README.md`) is pushed to a GitHub repository.

Create a `.gitignore` file to avoid committing unnecessary files:
```
# Database file
*.db

# Virtual environment
venv/
/venv/

# Python cache
__pycache__/
*.pyc

# Streamlit logs
streamlit_run*.log
```
Push this `.gitignore` to your repository as well.

### 2. Sign Up for Streamlit Cloud

Go to [https://share.streamlit.io/signup](https://share.streamlit.io/signup) and sign up using your GitHub account.

### 3. Deploy the App

1.  From your Streamlit Cloud workspace, click **"New app"**.
2.  Select the GitHub repository you created.
3.  Choose the correct branch (usually `main` or `master`).
4.  The "Main file path" should be `app.py`. Streamlit will automatically detect the `pages/` directory and create the multi-page navigation.
5.  Click **"Advanced settings..."** to add your Groq API Key as a secret. This is the recommended way to handle the API key for deployment.
    -   In the "Secrets" section, paste the following, replacing `"<your-groq-api-key>"` with your actual key:
        ```toml
        GROQ_API_KEY = "<your-groq-api-key>"
        ```
    -   Click **"Save"**.
6.  Click **"Deploy!"**.

Your application will be deployed and accessible via a public URL. The app will securely access the API key from the secrets you provided, so you won't need to enter it in the deployed version.
