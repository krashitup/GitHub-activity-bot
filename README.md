# GitHub Activity Dashboard

GitHub Activity Dashboard is a beginner-friendly Python project that scans GitHub repositories, saves commit data in Microsoft SQL Server, classifies commits, and displays simple activity reports.

The project first supports a terminal menu, then adds a simple Flask web interface using only basic routes, HTML, and CSS.

## Technology Stack

- Python 3.14
- Microsoft SQL Server `localhost\SQLEXPRESS`
- `pyodbc`
- `requests`
- Flask
- HTML
- CSS
- GitHub API

## Project Structure

```text
github-activity-bot/
├── app.py
├── database/
│   └── connection.py
├── GitHub_api/
│   └── commit_scanner.py
├── services/
│   ├── classification_service.py
│   └── report_services.py
├── sql/
│   └── schema.sql
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   └── report.html
├── README.md
└── requirements.txt
```

## File Responsibilities

### `app.py`

This is the main project entry point.

Responsibility:

- Shows the CLI menu when you run `python app.py`
- Defines the Flask routes `/`, `/scan`, and `/report`
- Calls scanner and report service functions

How it interacts:

- Calls `run_scanner()` from `GitHub_api/commit_scanner.py`
- Calls report functions from `services/report_services.py`
- Sends report data to `templates/report.html`

### `database/connection.py`

This file owns the SQL Server connection.

Responsibility:

- Creates and returns a `pyodbc` database connection
- Keeps the connection string in one place

How it interacts:

- Used by scanner and report service files whenever they need SQL Server

### `GitHub_api/commit_scanner.py`

This file owns GitHub API scanning.

Responsibility:

- Fetches repositories from GitHub
- Fetches commits from each repository
- Saves repositories and commits to SQL Server
- Classifies each commit before saving it

How it interacts:

- Uses `requests` to call GitHub
- Uses `get_db_connection()` to save data
- Uses `classify_commit()` to choose commit categories

### `services/classification_service.py`

This file owns commit classification.

Responsibility:

- Reads a commit message
- Returns a simple category such as `Feature`, `Bug Fix`, `Documentation`, `Refactor`, or `Other`

How it interacts:

- Used by `commit_scanner.py` before a commit is inserted into SQL Server

### `services/report_services.py`

This file owns report data.

Responsibility:

- Reads total repositories from SQL Server
- Reads total commits from SQL Server
- Groups commits by category
- Prints a terminal report
- Returns report data for Flask

How it interacts:

- Used by `app.py` for both CLI reports and web reports

### `templates/index.html`

This file owns the scan page.

Responsibility:

- Displays the project title
- Shows GitHub username input
- Shows PAT input
- Posts the form to `/scan`

How it interacts:

- Flask renders it from the `/` route

### `templates/report.html`

This file owns the report page.

Responsibility:

- Displays total repositories
- Displays total commits
- Displays commit categories
- Displays a simple activity summary

How it interacts:

- Flask renders it from `/report` and `/scan`
- Receives `report_data` from `app.py`

### `static/css/style.css`

This file owns the page design.

Responsibility:

- Adds layout, spacing, colors, forms, buttons, and report table styles
- Does not contain JavaScript or external CSS frameworks

How it interacts:

- Linked by both HTML templates

## Setup

Install dependencies:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create the database tables by running `sql/schema.sql` in SQL Server Management Studio against the `GitActivityDB` database.

## Run The CLI

```powershell
.\venv\Scripts\python.exe app.py
```

Menu options:

- `1` scans GitHub activity
- `2` prints the report
- `3` exits

## Run The Flask App

```powershell
.\venv\Scripts\python.exe app.py web
```

Open this URL:

```text
http://127.0.0.1:5001/
```

Do not open `templates/index.html` directly in the browser.
Do not use VS Code Live Server for this project.
The form needs the Flask backend, so the URL must start with `http://127.0.0.1:5001/`.

## Test Checklist

- Run `python -m py_compile` to check Python syntax
- Open `/` and confirm the scan form appears
- Enter a GitHub username and PAT, then click scan
- Open `/report` and confirm totals and categories appear
- Run the CLI report option and confirm it prints the same data

## Notes

- This project uses simple functions instead of advanced architecture.
- It does not use SQLAlchemy, ORMs, blueprints, async code, decorators, or JavaScript frameworks.
- Keep your GitHub PAT private and do not commit it to Git.
