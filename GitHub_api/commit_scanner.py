import requests
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_connection import get_db_connection

def fetch_repositories(username, token):
    """Fetches all repositories for the given user from GitHub."""
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"token {token}", 
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"\nFetching repositories for {username}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching repos. Status: {response.status_code}")
        return []

def fetch_commits(username, repo_name, token):
    """Fetches the latest commits for a specific repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    headers = {
        "Authorization": f"token {token}", 
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"  -> Scanning commits in '{repo_name}'...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return []

def save_to_database(repo_data, commits_data):
    """Saves the repository and its commits into the SQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        repo_name = repo_data['name']
        repo_url = repo_data['html_url']
        
        cursor.execute("SELECT ID FROM Repositories WHERE Path = ?", repo_url)
        result = cursor.fetchone()
        
        if result:
            repo_id = result[0] # Grab existing ID
        else:
            cursor.execute(
                "INSERT INTO Repositories (Name, Path) OUTPUT INSERTED.ID VALUES (?, ?)",
                (repo_name, repo_url)
            )
            repo_id = cursor.fetchone()[0]

       
        new_commit_count = 0
        for commit in commits_data:
            commit_hash = commit['sha']
            message = commit['commit']['message']
            author = commit['commit']['author']['name']
            date = commit['commit']['author']['date']
            
            
            cursor.execute("SELECT ID FROM Commits WHERE Hash = ?", commit_hash)
            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO Commits (Hash, Message, Author, Date, RepositoryID) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (commit_hash, message, author, date, repo_id)
                )
                new_commit_count += 1
        
        
        conn.commit()
        print(f"     [Saved {new_commit_count} new commits to database]")

    except Exception as e:
        print(f"     [Database Error: {e}]")
        conn.rollback()
    finally:
        conn.close()

def run_scanner(username, token):
    """Main function to run the full scanning process."""
    repos = fetch_repositories(username, token)
    
    for repo in repos:
       
        commits = fetch_commits(username, repo['name'], token)
        
        
        if commits:
            save_to_database(repo, commits)
            
    print("\n✅Scanning and Database Sync Complete!")

# Temporary test block
if __name__ == "__main__":
    
    test_username = "YOUR_USERNAME"
    test_token = "YOUR_PAT"
    
    if test_token == "YOUR_PAT":
        print("Waiting for PAT and Username to be added at the bottom of the script...")
    else:
        run_scanner(test_username, test_token)