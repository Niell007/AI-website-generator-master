from github_utils import get_repo
import os
from dotenv import load_dotenv

def test_github_connection():
    load_dotenv()
    
    # Get credentials from environment
    token = os.environ.get('GITHUB_ACCESS_TOKEN')
    repo_name = os.environ.get('GITHUB_REPO_NAME')
    
    if not token or not repo_name:
        print("Error: Missing GitHub credentials in .env file")
        return False
        
    try:
        repo = get_repo(token, repo_name)
        print(f"Successfully connected to GitHub repository: {repo.full_name}")
        print(f"Clone URL: {repo.clone_url}")
        return True
    except Exception as e:
        print(f"Error connecting to GitHub: {str(e)}")
        return False

if __name__ == "__main__":
    test_github_connection() 