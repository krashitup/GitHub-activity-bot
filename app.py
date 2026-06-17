import sys

from flask import Flask, render_template, request, session, redirect, url_for

from GitHub_api.commit_scanner import run_scanner
from services.report_services import (
    generate_activity_report, 
    get_activity_report_data,
    get_repository_commits,
    search_commits
)


app = Flask(__name__)
app.secret_key = "github_activity_secret_key"


def show_home_page():
    """Shows the scan form in the browser."""
    return render_template("index.html")


def scan_github_activity():
    """Reads form input and starts the GitHub scan."""
    if request.method == "GET":
        return render_template("index.html")

    username = request.form.get("username")
    token = request.form.get("token")

    if username and token:
        session["username"] = username
        run_scanner(username, token)

    current_user = session.get("username")
    if not current_user:
        return redirect(url_for("show_home_page"))

    return redirect(url_for("show_report_page"))


def show_report_page():
    """Shows saved GitHub activity data in the browser."""
    username = session.get("username")
    if not username:
        return redirect(url_for("show_home_page"))

    report_data = get_activity_report_data(username)
    return render_template("report.html", report_data=report_data)


def show_repository_page(repo_id):
    """Shows commits for a specific repository."""
    username = session.get("username")
    if not username:
        return redirect(url_for("show_home_page"))

    repo_data = get_repository_commits(repo_id, username)
    if not repo_data:
        return "Unauthorized or Repository Not Found", 403

    return render_template("repo_commits.html", repo_data=repo_data)


def search_activity():
    """Searches for commits matching a query."""
    username = session.get("username")
    if not username:
        return redirect(url_for("show_home_page"))

    query = request.args.get('q', '')
    results = search_commits(query, username) if query else []
    return render_template("search.html", query=query, results=results)


def run_cli_menu():
    """Shows a simple terminal menu for scanning and reporting."""
    while True:
        print("\nGitHub Activity Dashboard")
        print("1. Scan GitHub activity")
        print("2. Generate report")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter GitHub username: ")
            token = input("Enter GitHub Personal Access Token: ")
            run_scanner(username, token)

        elif choice == "2":
            username = input("Enter GitHub username for report: ")
            generate_activity_report(username)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


app.add_url_rule("/", "show_home_page", show_home_page, methods=["GET"])
app.add_url_rule("/scan", "scan_github_activity", scan_github_activity, methods=["GET", "POST"])
app.add_url_rule("/report", "show_report_page", show_report_page, methods=["GET"])
app.add_url_rule("/repository/<int:repo_id>", "show_repository_page", show_repository_page, methods=["GET"])
app.add_url_rule("/search", "search_activity", search_activity, methods=["GET"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        app.run(host="127.0.0.1", port=5001)
    else:
        run_cli_menu()
