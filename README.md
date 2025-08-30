# 🧪 Gemini API Key Tester

This is a web-based tool for testing and managing Google Gemini API keys. It provides a simple interface to send a test prompt to the Gemini API and view the response. The application also allows for storing, viewing, and managing multiple API keys.

## 🚀 How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/gemini-api-key-tester.git
    cd gemini-api-key-tester
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install Flask requests
    ```

3.  **Initialize the database:**
    ```bash
    flask init-db
    ```

4.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`.

## 📂 Project Structure

```
.
├── static/
│   └── style.css
├── templates/
│   └── api_test.html
├── .gitignore
├── app.py
└── database.db
```

*   **`static/`**: 🎨 Contains static files like CSS, and in the future, could contain JavaScript or images.
*   **`templates/`**: 📄 Holds the HTML templates that are rendered by Flask.
*   **`app.py`**: 🐍 The main Flask application file containing the server-side logic.
*   **`database.db`**: 💾 The SQLite database file where API keys are stored. This file is created when the application is first run.

## ✨ Features

*   **API Key Validation**: ✅ Quickly check if a Gemini API key is valid, expired, or has other issues.
*   **Local Key Storage**: 🔐 Save API keys with custom names in a local SQLite database for easy access.
*   **Key Management**: 📋 View a paginated list of saved keys, search for specific keys, and delete keys you no longer need.
*   **Dark/Light Mode**: 🌓 A theme switcher allows you to toggle between light and dark modes, with your preference saved in local storage.

## 🛠️ Technologies and Libraries

*   **[Flask](https://flask.palletsprojects.com/)**: A lightweight WSGI web application framework in Python.
*   **[Requests](https://requests.readthedocs.io/en/latest/)**: A simple, yet elegant, HTTP library for Python.
*   **[SQLite](https://www.sqlite.org/index.html)**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
*   **System Fonts**: The UI uses a system font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto...`) for a native look and feel across different operating systems and for performance.
