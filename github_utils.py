from github import Github, BadCredentialsException, UnknownObjectException, GithubException
import os
import time

def verify_token_scopes(github):
    """Verify that the token has the required scopes"""
    try:
        auth = github.get_user().get_authorization(os.environ['GITHUB_ACCESS_TOKEN'])
        required_scopes = {'repo', 'workflow', 'delete_repo'}
        actual_scopes = set(auth.scopes if auth else [])
        missing_scopes = required_scopes - actual_scopes
        if missing_scopes:
            raise Exception(f"Token is missing required scopes: {', '.join(missing_scopes)}")
        return True
    except Exception as e:
        print(f"Error verifying token scopes: {str(e)}")
        return False

def get_repo(access_token, repo_name):
    try:
        github = Github(access_token)
        user = github.get_user()
        
        # Verify credentials and scopes
        try:
            username = user.login
            print(f"Authenticated as GitHub user: {username}")
            if not verify_token_scopes(github):
                raise Exception("Token lacks required permissions. Please check GitHub token scopes.")
        except Exception as e:
            raise BadCredentialsException(f"GitHub authentication failed: {str(e)}")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Try to get existing repo
                try:
                    repo = user.get_repo(repo_name)
                    print(f"Successfully connected to existing repository: {repo_name}")
                    return repo
                except UnknownObjectException:
                    # Create new repo if it doesn't exist
                    print(f"Repository '{repo_name}' not found. Creating new repository...")
                    try:
                        repo = user.create_repo(
                            name=repo_name,
                            description="Generated website using Cloudflare AI",
                            private=False,
                            auto_init=True,
                            gitignore_template="Python"
                        )
                        print(f"Successfully created new repository: {repo_name}")
                        # Wait for repository to be fully created
                        time.sleep(5)
                        return repo
                    except GithubException as create_error:
                        error_message = create_error.data.get('message', str(create_error))
                        if create_error.status == 403:
                            print(f"Error: Permission denied. GitHub message: {error_message}")
                            print("Please ensure your token has the 'repo' and 'workflow' permissions")
                            raise Exception("GitHub token lacks required permissions")
                        elif create_error.status == 422:
                            print(f"Repository '{repo_name}' already exists but is not accessible")
                            raise Exception("Repository exists but is not accessible")
                        else:
                            print(f"Error creating repository: {error_message}")
                            if attempt == max_retries - 1:
                                raise
                            time.sleep(2)
                            continue
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to access/create repository after {max_retries} attempts: {str(e)}")
                time.sleep(2)
                
    except BadCredentialsException as e:
        raise Exception(
            f"GitHub authentication failed: {str(e)}\n\n"
            "Please ensure your token has these permissions:\n"
            "- repo (Full control of private repositories)\n"
            "- workflow (Update GitHub Action workflows)\n"
            "- delete_repo (Delete repositories)\n\n"
            "You can create a new token at: https://github.com/settings/tokens"
        )
    except Exception as e:
        raise Exception(f"GitHub Error: {str(e)}")