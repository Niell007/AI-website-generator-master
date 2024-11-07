from dotenv import load_dotenv
import os
import subprocess
from github_utils import get_repo
from openai_utils import generate_html
from beautifulsoup import generate_images
import tempfile
import shutil
import datetime
import time

# Load environment variables from .env file
load_dotenv()

def get_prompt_template(style, input_text):
    current_year = datetime.datetime.now().year
    return (
        f"Create a professional website using {style} framework based on this description: '{input_text}'\n\n"
        f"Requirements:\n"
        f"- Include proper HTML5 structure\n"
        f"- Add CSS styling within a <style> tag\n"
        f"- Create responsive design\n"
        f"- Include at least 2 images with style attributes (height and width in pixels)\n"
        f"- Each image must have a detailed alt text (100+ words)\n"
        f"- Add at least 2 paragraphs of relevant content\n"
        f"- Include footer with copyright {current_year} and social links\n\n"
        f"Respond only with the complete HTML code."
    )

def clean_image_directory(local_directory):
    images_path = os.path.join(local_directory, "images")
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    os.makedirs(images_path)

def make_changes_and_push(input_text, style):
    # Validate environment variables
    required_vars = ['GITHUB_ACCESS_TOKEN', 'GITHUB_REPO_NAME', 'GIT_USER_EMAIL', 'GIT_USER_NAME']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise Exception(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Get environment variables
    github_token = os.environ['GITHUB_ACCESS_TOKEN']
    repo_name = os.environ['GITHUB_REPO_NAME']
    git_email = os.environ['GIT_USER_EMAIL']
    git_name = os.environ['GIT_USER_NAME']

    try:
        # Set up repository with retry logic
        max_retries = 3
        repo = None
        last_error = None
        
        for attempt in range(max_retries):
            try:
                repo = get_repo(github_token, repo_name)
                if repo and hasattr(repo, 'clone_url'):
                    break
            except Exception as e:
                last_error = e
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)
        
        if not repo or not hasattr(repo, 'clone_url'):
            raise Exception(f"Failed to initialize repository after {max_retries} attempts. Last error: {str(last_error)}")

        commit_message = f"Add HTML file based on input text: {input_text}"

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            local_directory = os.path.join(temp_dir, "cloned_repo")
            
            # Ensure clone URL is properly formatted
            clone_url = repo.clone_url.replace('https://', f'https://{github_token}@')
            
            # Clone the repository with retries
            clone_success = False
            for attempt in range(max_retries):
                try:
                    print(f"Attempting to clone repository (attempt {attempt + 1}/{max_retries})")
                    result = subprocess.run(
                        f"git clone --depth 1 {clone_url} {local_directory}",
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    clone_success = True
                    break
                except subprocess.CalledProcessError as e:
                    print(f"Clone attempt {attempt + 1} failed: {e.stderr}")
                    if attempt == max_retries - 1:
                        raise Exception(f"Failed to clone repository: {e.stderr}")
                    time.sleep(2)
            
            if not clone_success:
                raise Exception("Failed to clone repository after multiple attempts")

            # Generate HTML content using Cloudflare Workers AI
            prompt = get_prompt_template(style, input_text)
            html_content = generate_html(prompt)

            # Clean and prepare images directory
            clean_image_directory(local_directory)

            # Generate images using Cloudflare AI
            html_content = generate_images(html_content, local_directory)

            # Add the script to the HTML content
            script_tag = '''<script 
                            id="clhac43dd0002q0vl8ue830mv"
                            data-name="databerry-chat-bubble"
                            src="https://databerry-one.vercel.app/js/chat-bubble.js"
                            ></script>'''
            html_content = html_content.replace("</body>", f"{script_tag}</body>")

            # Configure git
            subprocess.run(f"git -C {local_directory} config user.email {git_email}", shell=True, check=True)
            subprocess.run(f"git -C {local_directory} config user.name {git_name}", shell=True, check=True)

            # Add, commit, and push the changes
            with open(os.path.join(local_directory, "index.html"), "w") as f:
                f.write(html_content)

            # Git operations with error handling
            try:
                subprocess.run(f"git -C {local_directory} add .", shell=True, check=True)
                subprocess.run(
                    f'git -C {local_directory} commit -m "{commit_message}"',
                    shell=True,
                    check=True
                )
                subprocess.run(f"git -C {local_directory} push", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise Exception(f"Git operation failed: {e.stderr}")

    except Exception as e:
        raise Exception(f"Failed to process request: {str(e)}")


# if __name__ == "__main__":
#     # Code to be executed when the script is run as the main program

#     # Get input from user
#     input_text = input("Enter text to generate HTML content: ")

#     # Make changes and push to GitHub
#     make_changes_and_push(input_text)

