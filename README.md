# B.Tech CSE Performance Tracker & Analyzer

This is a Streamlit web application designed to help a B.Tech CSE student track their activities, manage goals, schedule exams, and get AI-powered insights to improve their performance.

## Features

- **Dashboard**: A central hub with AI-powered suggestions from Groq (using the LLaMA model) and reminders for upcoming exams.
- **Add Activity**: Log daily activities like studying, projects, fitness, etc.
- **Add Goal**: Set short-term and long-term goals to stay focused.
- **Add Exam**: Keep track of exam schedules.
- **Analytics**: Visualize your performance with interactive charts (time per category, activity distribution, trends).
- **History**: A searchable and filterable log of all your past activities.
- **Data Persistence**: All data is stored locally in a SQLite database (`performance_tracker.db`).
- **Export**: Export your activity history to a CSV file.

## Tech Stack

- **Framework**: Streamlit
- **Language**: Python
- **Database**: SQLite
- **Data Analysis**: Pandas
- **Plotting**: Plotly
- **AI Suggestions**: Groq API (LLaMA 3)

## How to Run Locally

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

You can either set the API key as an environment variable or enter it directly in the app's sidebar.

```bash
streamlit run app.py
```

The application will open in your default web browser.

## How to Deploy to Streamlit Cloud

Streamlit Cloud offers a free and easy way to deploy your app.

### 1. Push Your Code to a GitHub Repository

Make sure your `app.py`, `requirements.txt`, and this `README.md` are in a public or private GitHub repository. The app will create the SQLite database file (`performance_tracker.db`) on the server, but it's good practice to add it to your `.gitignore` file to avoid committing the database itself.

Create a `.gitignore` file with the following content:
```
*.db
venv/
__pycache__/
```

### 2. Sign Up for Streamlit Cloud

Go to [https://share.streamlit.io/signup](https://share.streamlit.io/signup) and sign up using your GitHub account.

### 3. Deploy the App

1.  From your Streamlit Cloud workspace, click **"New app"**.
2.  Select the GitHub repository you created.
3.  Choose the correct branch (usually `main` or `master`).
4.  The "Main file path" should be `app.py`.
5.  Click **"Advanced settings..."** to add your Groq API Key as a secret.
    -   In the "Secrets" section, paste the following, replacing `"<your-groq-api-key>"` with your actual key:
        ```toml
        GROQ_API_KEY = "<your-groq-api-key>"
        ```
    -   Click **"Save"**.
6.  Click **"Deploy!"**.

Your application will be deployed and accessible via a public URL. Any data you add will be stored on the server instance. Note that on the free tier, the app may sleep after a period of inactivity, but the database will persist.
