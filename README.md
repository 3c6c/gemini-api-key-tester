# Gemini API Key Tester

This project provides a web interface and a command-line tool to test your Gemini API key.

## Features

-   **Web Interface:** A user-friendly web page to enter your API key and prompt.
-   **Command-Line Tool:** A standalone bash script for quick API tests from the terminal.
-   **Quick Install:** Download and run the CLI tool with a single command.

## Project Setup (Web Interface)

To run the web interface locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/3c6c/gemini-api-key-tester.git
    cd YOUR_REPOSITORY
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install Flask requests
    ```

4.  **Run the application:**
    ```bash
    python3 app.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:5000`.

## Command-Line Interface

The command-line interface (CLI) is a standalone bash script that allows you to quickly test your Gemini API key from the terminal without needing to clone the entire project.

### Quick Install & Run

You can download and run the script directly from GitHub using one of the following commands.

**Using curl:**
```bash
bash <(curl -s https://raw.githubusercontent.com/3c6c/gemini-api-key-tester/main/run_cli.sh)
```

**Using wget:**
```bash
bash <(wget -qO- https://raw.githubusercontent.com/3c6c/gemini-api-key-tester/main/run_cli.sh)
```

### Manual Usage

If you have cloned the repository, you can run the script directly.

```bash
./run_cli.sh [API_KEY]
./run_cli.sh -f FILE
```

**Arguments:**

*   `API_KEY`: Your Gemini API key. If not provided, you will be prompted to enter it interactively.
*   `-f FILE` or `--file FILE`: Path to a file containing lines in the format `owner:api_key`. Each key will be checked in turn, and the owner will be displayed with the result.

**File Format Example:**

```
# keys.txt
alice:AIzaSyA...abc
bob:AIzaSyB...xyz
```

**Examples:**

*   Run with a single API key:
    ```bash
    ./run_cli.sh "YOUR_API_KEY"
    ```

*   Run in batch mode with a file:
    ```bash
    ./run_cli.sh -f keys.txt
    ```

*   Run without any arguments (will prompt you for the API key):
    ```bash
    ./run_cli.sh
    ```

*   Display the help message:
    ```bash
    ./run_cli.sh -h
    ```

## ✨ Features

- API Key Validation: ✅ Quickly check if a Gemini API key is valid, expired, or has other issues.
- Local Key Storage: 🔐 Save API keys with custom names in a local SQLite database for easy access.
- Key Management: 📋 View a paginated list of saved keys, search for specific keys, and delete keys you no longer need.
- Dark/Light Mode: 🌓 A theme switcher allows you to toggle between light and dark modes, with your preference saved in local storage.
