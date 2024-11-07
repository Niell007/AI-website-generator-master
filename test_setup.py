from dotenv import load_dotenv
import os
from github import Github
import requests

def test_environment():
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'GITHUB_ACCESS_TOKEN',
        'GITHUB_REPO_NAME',
        'GIT_USER_EMAIL',
        'GIT_USER_NAME',
        'CLOUDFLARE_API_KEY',
        'CLOUDFLARE_ACCOUNT_ID'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return False
        
    # Test GitHub token
    try:
        g = Github(os.getenv('GITHUB_ACCESS_TOKEN'))
        user = g.get_user()
        print(f"✓ GitHub: Authenticated as {user.login}")
    except Exception as e:
        print(f"❌ GitHub authentication failed: {str(e)}")
        return False
        
    # Test Cloudflare credentials
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('CLOUDFLARE_ACCOUNT_ID')}/ai/run",
            headers={
                "Authorization": f"Bearer {os.getenv('CLOUDFLARE_API_KEY')}",
                "Content-Type": "application/json"
            }
        )
        if response.status_code == 200:
            print("✓ Cloudflare: API credentials verified")
        else:
            print(f"❌ Cloudflare API check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Cloudflare API check failed: {str(e)}")
        return False
        
    return True

if __name__ == "__main__":
    print("Testing environment setup...")
    if test_environment():
        print("\n✓ All checks passed!")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.") 