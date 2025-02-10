import os
import requests
import base64
import time

def create_branch_if_not_exists(owner, repo, token, new_branch, source_branch="main"):
    """
    Checks if new_branch exists; if not, creates it from source_branch.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Get the SHA of the source branch (e.g., main)
    get_ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{source_branch}"
    resp = requests.get(get_ref_url, headers=headers)
    if resp.status_code != 200:
        print(f"❌ Could not get SHA for {source_branch}. Response: {resp.text}")
        return False

    source_sha = resp.json()["object"]["sha"]

    # 2. Check if new_branch already exists
    new_ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{new_branch}"
    resp_new = requests.get(new_ref_url, headers=headers)

    if resp_new.status_code == 200:
        print(f"✅ Branch '{new_branch}' already exists.")
        return True  # Nothing to do, branch exists
    elif resp_new.status_code == 404:
        # 3. Create the new branch from the source SHA
        create_ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
        ref_data = {
            "ref": f"refs/heads/{new_branch}",
            "sha": source_sha
        }
        resp_create = requests.post(create_ref_url, headers=headers, json=ref_data)
        if resp_create.status_code in [200,201]:
            print(f"✅ Created new branch '{new_branch}' from '{source_branch}'")
            return True
        else:
            print(f"❌ Failed to create branch '{new_branch}': {resp_create.text}")
            return False
    else:
        print(f"❌ Unexpected error checking branch '{new_branch}': {resp_new.text}")
        return False

def update_file(url, headers, encoded_content, branch, github_path, current_sha=None, retry=0):
    update_data = {
        "message": f"Update {github_path} in {branch}",
        "content": encoded_content,
        "branch": branch
    }
    if current_sha:
        update_data["sha"] = current_sha

    response = requests.put(url, headers=headers, json=update_data)
    if response.status_code in [200, 201]:
        print(f"✅ Successfully updated {github_path} in {branch}")
        return True
    elif response.status_code == 409 and retry < 3:
        print(f"⚠️ Conflict updating {github_path} in {branch}; retrying...")
        get_resp = requests.get(url, headers=headers)
        if get_resp.status_code == 200:
            new_sha = get_resp.json()["sha"]
            return update_file(url, headers, encoded_content, branch, github_path, current_sha=new_sha, retry=retry+1)
        else:
            print(f"❌ Failed to get new SHA for {github_path} in {branch}")
            return False
    else:
        print(f"❌ Failed to update {github_path} in {branch}")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def update_github_files():
    token = os.environ['GITHUB_TOKEN']
    owner = "nicksanford2323"
    repo = "electrical-business-web-1"  
    new_branch = "gh-page"        # The new branch name you want

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Make sure the new branch exists (create if needed)
    branch_ok = create_branch_if_not_exists(owner, repo, token, new_branch, source_branch="main")
    if not branch_ok:
        print("❌ Branch creation failed; aborting updates.")
        return

    files = {
        "src/App.jsx": "src/App.jsx",
        "src/App.css": "src/App.css",
        "src/components/Header.jsx": "src/components/Header.jsx",
        "src/components/Header.css": "src/components/Header.css",
        "src/components/Hero.jsx": "src/components/Hero.jsx",
        "src/components/Hero.css": "src/components/Hero.css",
        "src/components/About.jsx": "src/components/About.jsx",
        "src/components/About.css": "src/components/About.css",
        "src/components/Services.jsx": "src/components/Services.jsx",
        "src/components/Services.css": "src/components/Services.css",
        "src/components/Reviews.jsx": "src/components/Reviews.jsx",
        "src/components/Reviews.css": "src/components/Reviews.css",
        "src/components/Gallery.jsx": "src/components/Gallery.jsx",
        "src/components/Gallery.css": "src/components/Gallery.css",
        "src/components/Contact.jsx": "src/components/Contact.jsx",
        "src/components/Contact.css": "src/components/Contact.css",
        "src/components/Footer.jsx": "src/components/Footer.jsx",
        "src/components/Footer.css": "src/components/Footer.css",
        "src/components/LoadingScreen.jsx": "src/components/LoadingScreen.jsx",
        "src/components/LoadingScreen.css": "src/components/LoadingScreen.css",
        "vite.config.js": "vite.config.js",
        "package.json": "package.json"
    }

    print(f"\n🔄 Updating branch: {new_branch}")
    for github_path, local_path in files.items():
        print(f"\nUpdating {github_path} in {new_branch}...")
        try:
            with open(local_path, 'r', encoding='utf-8') as file:
                content = file.read()

            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{github_path}?ref={new_branch}"

            # Try to fetch current SHA on that new branch
            get_resp = requests.get(url, headers=headers)
            if get_resp.status_code == 200:
                current_sha = get_resp.json()["sha"]
            else:
                current_sha = None

            update_file(url, headers, encoded_content, new_branch, github_path, current_sha=current_sha)
            time.sleep(0.5)  # Slight delay

        except Exception as e:
            print(f"❌ Error updating {github_path} in {new_branch}: {str(e)}")

def force_pages_rebuild():
    # Optional if you want to force a rebuild
    token = os.environ['GITHUB_TOKEN']
    owner = "nicksanford2323"
    repo = "electrical-business-web-1"
    new_branch = "gh-page"  # The same branch you'd set as your pages branch

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # If you have GH Pages set to new_branch, update a dummy file there
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/rebuild-trigger"
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    content = f"Force rebuild at {timestamp}"
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    update_data = {
        "message": "Force GitHub Pages rebuild",
        "content": encoded_content,
        "branch": new_branch
    }

    try:
        response = requests.put(url, headers=headers, json=update_data)
        if response.status_code in [200, 201]:
            print("✅ Successfully triggered Pages rebuild")
            return True
        else:
            print("❌ Failed to trigger Pages rebuild")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting update process...")
    update_github_files()

    print("\n📦 (Optional) Forcing GitHub Pages rebuild from new branch...")
    force_pages_rebuild()
    print("\n✨ Done! Check your new branch for updates, then configure GH Pages to use it if needed.")
