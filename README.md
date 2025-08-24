# B.Tech CSE Performance Tracker & Analyzer v3.0

This is a powerful, multi-page Streamlit web application with a modern top-bar navigation, designed to help a B.Tech CSE student track activities, manage goals, build a daily routine, and gain deep, AI-powered insights into their performance.

## ✨ Features

- **🔝 Top Navigation**: A clean, modern UI with a horizontal navigation bar.
- **🏠 Dashboard**: A central hub with an at-a-glance summary, AI-powered suggestions, and reminders for upcoming exams.
- **✍️ Add Activity, Goal, Exam**: Log all aspects of your student life.
- **⏰ Daily Routine**: Build and manage your ideal daily schedule.
- **📚 History & Analytics**: Search your activity log and visualize your performance with interactive charts.
- **🔍 Deep Analysis**: An AI-powered page where you can ask natural language questions about your performance and get a detailed, data-driven report.
- **🗃️ Data Persistence**: All data is stored locally in a SQLite database (`performance_tracker.db`).

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **UI Components**: streamlit-option-menu
- **Language**: Python
- **Database**: SQLite
- **Data Analysis**: Pandas
- **Plotting**: Plotly
- **AI**: Groq API (LLaMA 3)

## 🚀 How to Run Locally

### 1. Prerequisites

- Python 3.7+
- `pip` for package installation

### 2. Clone the Repository & Install Dependencies

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

### 3. Get a Groq API Key

The AI features are powered by the Groq API.
1.  Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2.  Sign up for a free account and create a new API key.

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser with the new top navigation. You can enter your Groq API key in the sidebar on the Dashboard page to enable the AI features.

## ☁️ How to Deploy to Streamlit Cloud

Streamlit Cloud is the ideal platform for this app.

### 1. Push Your Code to a GitHub Repository

Ensure your entire project structure (`app.py`, `requirements.txt`, the `pages/` directory, the `utils/` directory, and this `README.md`) is pushed to a GitHub repository. A `.gitignore` file is recommended to exclude the database file and virtual environment.

### 2. Deploy the App

1.  From your Streamlit Cloud workspace, click **"New app"**.
2.  Select your GitHub repository and branch.
3.  The "Main file path" must be `app.py`.
4.  Click **"Advanced settings..."** to add your Groq API Key as a secret. This is the recommended way to handle the API key for deployment.
    -   In the "Secrets" section, paste: `GROQ_API_KEY = "<your-groq-api-key>"`
    -   Click **"Save"**.
5.  Click **"Deploy!"**.

Your application will be deployed and accessible via a public URL. The app will securely access the API key from the secrets you provided.
