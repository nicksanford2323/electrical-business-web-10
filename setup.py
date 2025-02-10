import os
import requests
import base64
import json

# Your GitHub settings
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = "nicksanford2323"
REPO_NAME = "electric"

# GitHub API headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def create_file(path, content):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{path}'
    content_bytes = content.encode('utf-8')
    base64_content = base64.b64encode(content_bytes).decode('utf-8')

    data = {
        'message': f'Add {path}',
        'content': base64_content
    }

    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 201

def setup_repo():
    # Create repository if it doesn't exist
    repo_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}'
    repo_data = {
        'name': REPO_NAME,
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }

    response = requests.get(repo_url, headers=headers)
    if response.status_code == 404:
        create_response = requests.post('https://api.github.com/user/repos', headers=headers, json=repo_data)
        if create_response.status_code != 201:
            print("Failed to create repository")
            return False

    # Create necessary files
    vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/electric/',
})'''

    workflow_yml = '''name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

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

      - name: Install Dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: dist'''

    # Create files
    files_to_create = {
        'vite.config.js': vite_config,
        '.github/workflows/deploy.yml': workflow_yml
    }

    for path, content in files_to_create.items():
        if '/' in path:
            # Create directory structure if needed
            dir_path = path.rsplit('/', 1)[0]
            os.makedirs(dir_path, exist_ok=True)

        if create_file(path, content):
            print(f"Created {path}")
        else:
            print(f"Failed to create {path}")

    # Enable GitHub Pages
    pages_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages'
    pages_data = {
        'source': {
            'branch': 'gh-pages',
            'path': '/'
        }
    }
    response = requests.post(pages_url, headers=headers, json=pages_data)
    if response.status_code in [201, 204]:
        print("GitHub Pages enabled successfully")
    else:
        print("Failed to enable GitHub Pages")

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Please set GITHUB_TOKEN environment variable")
    else:
        setup_repo()