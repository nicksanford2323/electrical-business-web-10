import os
import sys
import shutil
import subprocess
import requests

def main():
    # 1. Read GitHub token from the environment variable
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not found.")
        sys.exit(1)

    # 2. GitHub username & repo name
    github_username = "nicksanford2323"
    new_repo_name = "electrical-business-web-10"

    # 3. Create a new repository on GitHub via API
    create_repo_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": new_repo_name,
        "private": False,  # Change to True if you want a private repo
        "description": "Vite + React site for electrical-business-web-7"
    }

    print(f"Creating a new repository '{new_repo_name}' under user '{github_username}'...")
    response = requests.post(create_repo_url, headers=headers, json=repo_data)

    if response.status_code == 201:
        print(f"Successfully created repository: {new_repo_name}")
    else:
        print(f"Error creating repository. Status code: {response.status_code}")
        print("Response:", response.json())
        sys.exit(1)

    # 4. Delete local .git folder (if it exists) to start fresh
    if os.path.isdir(".git"):
        print("\nRemoving existing .git folder—this will delete all commit history.")
        shutil.rmtree(".git")

    # 5. Initialize new Git repo, add all files, commit, push to new repo
    print("\nInitializing new git repository...")
    commands = [
        ["git", "init"],
        ["git", "add", "--all"],
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
    print("All your files have been pushed to the new repository.")

if __name__ == "__main__":
    main()
