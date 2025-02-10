import os
import subprocess
import requests
import sys

# ------------------------------------------------------------------------------
# 1. READ ENVIRONMENT VARIABLES
# ------------------------------------------------------------------------------
GITHUB_USERNAME = "nicksanford2323"   # <-- Set your GitHub username here
REPO_NAME = "BAMAELEC"               # <-- The new repository name you want
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# If the token isn't set, print an error and exit.
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# 2. CREATE (OR CONFIRM) NEW REPO ON GITHUB
# ------------------------------------------------------------------------------
create_repo_url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
payload = {
    "name": REPO_NAME,
    "private": False,         # or True if you want it private
    "description": "A React app deployed with GitHub Pages"
}

print(f"Creating repository '{REPO_NAME}' on GitHub...")

response = requests.post(create_repo_url, headers=headers, json=payload)

if response.status_code == 201:
    print(f"Successfully created the repository '{REPO_NAME}'!")
elif response.status_code == 422:
    # 422 usually means the repo already exists.
    print(f"Repository '{REPO_NAME}' already exists or cannot be created.")
else:
    print("Error creating repository:")
    print(response.json())
    sys.exit(1)

# ------------------------------------------------------------------------------
# 3. CREATE A 'saban' FILE IF IT DOESN'T EXIST
# ------------------------------------------------------------------------------
file_path = "saban"
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("This is the saban file.\n")
    print("Created 'saban' file.")
else:
    print("'saban' file already exists.")

# ------------------------------------------------------------------------------
# 4. INITIALIZE GIT (IF NOT ALREADY) AND PUSH TO GITHUB
# ------------------------------------------------------------------------------
# If you’ve already set up Git, you can skip the init steps.

# Check if .git directory exists
if not os.path.isdir(".git"):
    print("Initializing a new git repository...")
    subprocess.run(["git", "init"], check=True)

# Always ensure we’re on 'main' branch (rename from master if needed)
subprocess.run(["git", "checkout", "-B", "main"], check=True)

print("Adding files to git...")
subprocess.run(["git", "add", "."], check=True)

print("Committing files...")
subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

print("Setting remote origin and pushing to GitHub...")
remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
subprocess.run(["git", "remote", "remove", "origin"], check=False)
subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

# ------------------------------------------------------------------------------
# 5. INSTALL, BUILD, AND DEPLOY VIA NPM
# ------------------------------------------------------------------------------
print("Installing NPM dependencies...")
subprocess.run(["npm", "install"], check=True)

print("Building with Vite (npm run build)...")
subprocess.run(["npm", "run", "build"], check=True)

print("Deploying to GitHub Pages (npm run deploy)...")
deploy_result = subprocess.run(["npm", "run", "deploy"], check=False)

if deploy_result.returncode == 0:
    print("\nDeployment to GitHub Pages successful!")
    print(f"Your site should be at: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}")
else:
    print("\nDeployment step encountered an error. Check logs above.")
    sys.exit(1)
