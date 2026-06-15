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

        return {
            "total_repositories": total_repositories,
            "total_commits": total_commits,
            "categories": categories
        }

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
