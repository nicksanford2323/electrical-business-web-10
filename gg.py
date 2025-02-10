import os
import sys
import subprocess
import requests

def main():
    # 1. Read environment variable for your GitHub token
    #    In Replit, set a secret environment variable called "GITHUB_TOKEN"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not found.")
        sys.exit(1)

    # 2. Set your GitHub username and the new repository name
    github_username = "nicksanford2323"
    new_repo_name = "electrical-business-web-5"  # or any name you prefer

    # 3. Create the repository on GitHub via API
    create_repo_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": new_repo_name,
        "private": False,
        "description": "Vite + React site for an electrical business"
    }

    print(f"Creating a new repository '{new_repo_name}' under user '{github_username}'...")
    response = requests.post(create_repo_url, headers=headers, json=repo_data)

    if response.status_code == 201:
        print(f"Successfully created repository: {new_repo_name}")
    else:
        print(f"Error creating repository. Status code: {response.status_code}")
        print("Response:", response.json())
        sys.exit(1)

    # 4. Initialize local Git repo and push code
    # Make sure this script is run from the root of your project folder
    print("\nInitializing git repository locally...")
    commands = [
        ["git", "init"],
        ["git", "add", "-A"],
        ["git", "commit", "-m", "Initial commit"],
        ["git", "branch", "-M", "main"],
        [
            "git", "remote", "add", "origin",
            f"https://{github_username}:{token}@github.com/{github_username}/{new_repo_name}.git"
        ],
        ["git", "push", "-u", "origin", "main"]
    ]

    for cmd in commands:
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)

    print(f"\nDone! Your new repo is at: https://github.com/{github_username}/{new_repo_name}")

    # 5. (Optionally) Enable GH Pages if you'd like to do a direct main-branch deploy
    #    or you can rely on your GH Pages build branch. For example:
    #    PUT /repos/{owner}/{repo}/pages
    #    If you want to push your built `dist/` folder to a gh-pages branch manually,
    #    you can script that as well. See instructions below.

if __name__ == "__main__":
    main()
