import sys

from flask import Flask, render_template, request

from GitHub_api.commit_scanner import run_scanner
from services.report_services import generate_activity_report, get_activity_report_data


app = Flask(__name__)


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
        run_scanner(username, token)

    report_data = get_activity_report_data()
    return render_template("report.html", report_data=report_data)


def show_report_page():
    """Shows saved GitHub activity data in the browser."""
    report_data = get_activity_report_data()
    return render_template("report.html", report_data=report_data)


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
            generate_activity_report()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


app.add_url_rule("/", "show_home_page", show_home_page, methods=["GET"])
app.add_url_rule("/scan", "scan_github_activity", scan_github_activity, methods=["GET", "POST"])
app.add_url_rule("/report", "show_report_page", show_report_page, methods=["GET"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        app.run(host="127.0.0.1", port=5001)
    else:
        run_cli_menu()
