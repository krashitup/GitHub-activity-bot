import requests

def test_github_connection(username, token):
    """
    Tests the connection to the GitHub API using a Personal Access Token.
    """
   #official github url

    url = f"https://api.github.com/users/{username}/repos"
    

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"Connecting to GitHub for user: {username}...")
    

    response = requests.get(url, headers=headers)
    

    if response.status_code == 200:
       
        repos = response.json()
        print(f"Connection Successful! Found {len(repos)} public/private repositories.")
        
        print("\nHere are a few of your repositories:")
       
        for repo in repos[:5]:  
            print(f" - {repo['name']}")
    else:
        print(f"Failed to connect. Status Code: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    
    test_username = "__YOUR_USERNAME__"
    test_token = "__YOUR_PAT_TOKEN__"
    
    test_github_connection(test_username, test_token)