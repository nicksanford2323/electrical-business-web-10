import os
import requests
import subprocess
from datetime import datetime

# GitHub configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = "Nicksanford2323"
BASE_REPO_NAME = "electrical-business-web"
REPO_NAME = None  # Will be set after finding unique name

# GitHub API headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def check_repo_exists(repo_name):
    """Check if a repository already exists"""
    url = f'https://api.github.com/repos/{USERNAME}/{repo_name}'
    response = requests.get(url, headers=headers)
    return response.status_code == 200

def generate_unique_repo_name():
    """Generate a unique repository name"""
    counter = 1
    while True:
        repo_name = f"{BASE_REPO_NAME}-{counter}"
        if not check_repo_exists(repo_name):
            return repo_name
        counter += 1

def create_repo():
    """Create a new repository on GitHub"""
    global REPO_NAME
    REPO_NAME = generate_unique_repo_name()

    print(f"Attempting to create repository: {REPO_NAME}")

    url = 'https://api.github.com/user/repos'
    data = {
        'name': REPO_NAME,
        'description': 'Electrical Business Website',
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True,
        'auto_init': True
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Successfully created repository: {REPO_NAME}")
        return True
    else:
        print(f"Failed to create repository: {response.status_code}")
        print(response.json())
        return False

def setup_files():
    """Create necessary configuration files"""
    if not REPO_NAME:
        print("Error: Repository name not set")
        return False

    try:
        # Create vite.config.js
        vite_config = f"""
import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  base: '/{REPO_NAME}/',
}})
""".strip()

        with open('vite.config.js', 'w') as f:
            f.write(vite_config)
        print("Created vite.config.js")

        # Update package.json
        package_json = f"""{{
  "name": "react-javascript",
  "version": "1.0.0",
  "type": "module",
  "description": "React TypeScript on Replit, using Vite bundler",
  "homepage": "https://{USERNAME}.github.io/{REPO_NAME}",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {{
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "gh-pages": "^6.3.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.0"
  }}
}}""".strip()

        with open('package.json', 'w') as f:
            f.write(package_json)
        print("Updated package.json")

        # Create GitHub Actions workflow
        os.makedirs('.github/workflows', exist_ok=True)
        workflow_yml = """
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install Dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Deploy
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: dist
          branch: gh-pages
""".strip()

        with open('.github/workflows/deploy.yml', 'w') as f:
            f.write(workflow_yml)
        print("Created GitHub Actions workflow")
        return True

    except Exception as e:
        print(f"Error setting up files: {e}")
        return False

def setup_git():
    """Set up git and push to GitHub"""
    if not REPO_NAME:
        print("Error: Repository name not set")
        return False

    try:
        # Initialize git if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)

        # Create .gitignore
        with open('.gitignore', 'w') as f:
            f.write("""
node_modules/
dist/
.DS_Store
.env
.env.local
*.log
""".strip())

        # Configure git
        subprocess.run(['git', 'config', 'user.name', USERNAME], check=True)
        subprocess.run(['git', 'config', 'user.email', 'noreply@github.com'], check=True)

        # Remove existing remote if it exists
        try:
            subprocess.run(['git', 'remote', 'remove', 'origin'], check=False)
        except:
            pass

        # Add new remote
        remote_url = f'https://{GITHUB_TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git'
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)

        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)

        # Commit
        subprocess.run(['git', 'commit', '-m', 'Initial setup with deployment configuration'], check=True)

        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'main', '--force'], check=True)

        print("Successfully pushed to GitHub")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub token with: export GITHUB_TOKEN=your_token_here")
        return

    print("Starting deployment process...")

    # Create repository
    if not create_repo():
        return

    # Setup necessary files
    if not setup_files():
        return

    # Setup git and push
    if setup_git():
        print(f"""
Setup completed successfully!

Your repository has been created and configured:
1. Repository URL: https://github.com/{USERNAME}/{REPO_NAME}
2. Website URL (after deployment): https://{USERNAME}.github.io/{REPO_NAME}

Next steps:
1. Go to https://github.com/{USERNAME}/{REPO_NAME}/settings
2. Scroll down to "Pages"
3. For "Source", select "Deploy from a branch"
4. For "Branch", select "gh-pages" and "/(root)"
5. Click "Save"
6. Wait a few minutes for the deployment to complete

The site should be live shortly after following these steps!
""")
    else:
        print("Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()