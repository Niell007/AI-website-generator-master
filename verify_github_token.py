from github import Github, GithubException
import os
from dotenv import load_dotenv

def verify_token_permissions():
    """Verify GitHub token has required permissions"""
    load_dotenv()
    
    token = os.environ.get('GITHUB_ACCESS_TOKEN')
    if not token:
        print("❌ Error: GITHUB_ACCESS_TOKEN not found in .env file")
        return False
    
    try:
        g = Github(token)
        user = g.get_user()
        
        print(f"✓ Authenticated as: {user.login}")
        print("\nTesting permissions...")
        
        # Test repository access
        try:
            test_repo_name = "test-repo-delete-me"
            print("Testing repository creation...")
            repo = user.create_repo(
                test_repo_name,
                description="Test repository - will be deleted",
                auto_init=True,
                private=True
            )
            print("✓ Repository creation: Success")
            
            print("Testing repository deletion...")
            repo.delete()
            print("✓ Repository deletion: Success")
            
            print("\n✓ All permissions verified successfully!")
            return True
            
        except GithubException as e:
            if e.status == 403:
                print(f"❌ Permission denied: {e.data.get('message', '')}")
                print("\nRequired permissions:")
                print("- repo (Full control of private repositories)")
                print("- workflow (Update GitHub Action workflows)")
                print("- delete_repo (Delete repositories)")
            else:
                print(f"❌ Error testing permissions: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying token: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔑 Verifying GitHub token permissions...")
    verify_token_permissions() 