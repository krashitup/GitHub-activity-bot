from database.connection import get_db_connection


def get_activity_report_data():
    """Returns report data from SQL Server so CLI and Flask can both use it."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM Repositories")
        total_repositories = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Commits")
        total_commits = cursor.fetchone()[0]

        cursor.execute(
            "SELECT Category, COUNT(*) FROM Commits GROUP BY Category ORDER BY COUNT(*) DESC"
        )
        category_rows = cursor.fetchall()

        categories = []
        for row in category_rows:
            categories.append({
                "name": row[0] or "Other",
                "count": row[1]
            })

        # Feature 1: Repository List
        cursor.execute("SELECT RepositoryID, Name FROM Repositories ORDER BY Name")
        repositories = []
        for row in cursor.fetchall():
            repositories.append({
                "id": row[0],
                "name": row[1]
            })

        # Feature 7: Recent Activity
        cursor.execute("SELECT TOP 5 Message, CommitDate FROM Commits ORDER BY CommitDate DESC")
        recent_commits = []
        for row in cursor.fetchall():
            recent_commits.append({
                "message": row[0],
                "date": row[1].strftime('%d %b') if row[1] else "Unknown"
            })

        return {
            "total_repositories": total_repositories,
            "total_commits": total_commits,
            "categories": categories,
            "repositories": repositories,
            "recent_commits": recent_commits
        }

    finally:
        conn.close()

def get_repository_commits(repo_id):
    """Feature 2: Fetch all commits for a specific repository."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Name FROM Repositories WHERE RepositoryID = ?", (repo_id,))
        repo_row = cursor.fetchone()
        repo_name = repo_row[0] if repo_row else "Unknown Repository"

        cursor.execute("SELECT Message, CommitDate FROM Commits WHERE RepositoryID = ? ORDER BY CommitDate DESC", (repo_id,))
        commits = []
        for row in cursor.fetchall():
            commits.append({
                "message": row[0],
                "date": row[1].strftime('%d %b') if row[1] else "Unknown"
            })
        
        return {
            "repo_name": repo_name,
            "commits": commits
        }
    finally:
        conn.close()

def search_commits(query):
    """Feature 6: Search commit messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        search_term = f"%{query}%"
        cursor.execute("SELECT Message, CommitDate FROM Commits WHERE Message LIKE ? ORDER BY CommitDate DESC", (search_term,))
        results = []
        for row in cursor.fetchall():
            results.append({
                "message": row[0],
                "date": row[1].strftime('%d %b') if row[1] else "Unknown"
            })
        return results
    finally:
        conn.close()


def generate_activity_report():
    """Prints a simple report in the terminal."""
    try:
        report_data = get_activity_report_data()

        print("\n" + "=" * 50)
        print("GIT ACTIVITY DASHBOARD REPORT")
        print("=" * 50)
        print(f"Total Repositories Scanned: {report_data['total_repositories']}")
        print(f"Total Commits Found:        {report_data['total_commits']}")
        print("\n--- Commits by Category ---")

        for category in report_data["categories"]:
            print(f"  - {category['name']}: {category['count']}")

        print("=" * 50 + "\n")

    except Exception as error:
        print(f"Database Error: {error}")
