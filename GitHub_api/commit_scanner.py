import requests

from database.connection import get_db_connection
from services.classification_service import classify_commit


def fetch_repositories(username, token):
    """Fetches all public repositories for the given GitHub username."""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"\nFetching repositories for {username}...")
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 200:
        return response.json()

    print(f"Error fetching repos. Status: {response.status_code}")
    return []


def fetch_commits(username, repo_name, token):
    """Fetches commits for one repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"  -> Scanning commits in '{repo_name}'...")
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 200:
        return response.json()

    return []


def save_to_database(repo_data, commits_data):
    """Saves one repository and its commits into SQL Server."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        repo_name = repo_data["name"]
        repo_url = repo_data["html_url"]

        cursor.execute("SELECT RepositoryID FROM Repositories WHERE Path = ?", repo_url)
        result = cursor.fetchone()

        if result:
            repo_id = result[0]
        else:
            cursor.execute(
                "INSERT INTO Repositories (Name, Path) OUTPUT INSERTED.RepositoryID VALUES (?, ?)",
                (repo_name, repo_url)
            )
            repo_id = cursor.fetchone()[0]

        new_commit_count = 0

        for commit in commits_data:
            commit_hash = commit["sha"]
            message = commit["commit"]["message"]
            author = commit["commit"]["author"]["name"]
            commit_date = commit["commit"]["author"]["date"]
            category = classify_commit(message)

            cursor.execute("SELECT CommitID FROM Commits WHERE CommitHash = ?", commit_hash)

            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO Commits
                       (CommitHash, Message, Author, CommitDate, RepositoryID, Category)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (commit_hash, message, author, commit_date, repo_id, category)
                )
                new_commit_count += 1

        conn.commit()
        print(f"     [Saved {new_commit_count} new commits to database]")

    except Exception as error:
        print(f"     [Database Error: {error}]")
        conn.rollback()

    finally:
        conn.close()


def run_scanner(username, token):
    """Runs the full GitHub scan."""
    repos = fetch_repositories(username, token)

    for repo in repos:
        commits = fetch_commits(username, repo["name"], token)

        if commits:
            save_to_database(repo, commits)

    print("\nScanning and Database Sync Complete!")
