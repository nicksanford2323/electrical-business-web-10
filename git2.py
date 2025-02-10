import os
import requests
import base64
import time

def update_css_files():
    token = os.environ['GITHUB_TOKEN']
    owner = "nicksanford2323"
    repo = "electrical-business-web-1"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Only the CSS files that failed
    files = {
        "src/components/Reviews.css": "src/components/Reviews.css",
        "src/components/Gallery.css": "src/components/Gallery.css",
        "src/components/Header.css": "src/components/Header.css"
    }

    branches = ['main', 'gh-pages']

    for branch in branches:
        print(f"\n🔄 Updating CSS files in branch: {branch}")

        for github_path, local_path in files.items():
            print(f"\nUpdating {github_path} in {branch}...")

            try:
                if os.path.exists(local_path):
                    # Read the file content
                    with open(local_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                    # Encode content
                    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

                    # Get current file (if exists) to get its SHA
                    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{github_path}?ref={branch}"
                    response = requests.get(url, headers=headers)

                    # Prepare update data
                    if response.status_code == 200:
                        current_file = response.json()
                        update_data = {
                            "message": f"Fix: Update {github_path} in {branch}",
                            "content": encoded_content,
                            "sha": current_file["sha"],
                            "branch": branch
                        }
                    else:
                        update_data = {
                            "message": f"Fix: Add {github_path} in {branch}",
                            "content": encoded_content,
                            "branch": branch
                        }

                    # Try to update/create the file
                    response = requests.put(url, headers=headers, json=update_data)

                    if response.status_code in [200, 201]:
                        print(f"✅ Successfully updated {github_path} in {branch}")
                    else:
                        print(f"❌ Failed to update {github_path} in {branch}")
                        print(f"Status code: {response.status_code}")
                        print(f"Response: {response.text}")
                else:
                    print(f"⚠️ File not found: {local_path}")

            except Exception as e:
                print(f"❌ Error with {github_path}: {str(e)}")

            # Add longer delay between updates to avoid conflicts
            time.sleep(1)

def force_pages_rebuild():
    token = os.environ['GITHUB_TOKEN']
    owner = "nicksanford2323"
    repo = "electrical-business-web-1"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/rebuild-trigger"
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    content = f"Force rebuild at {timestamp}"
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    update_data = {
        "message": "Force GitHub Pages rebuild",
        "content": encoded_content,
        "branch": "gh-pages"
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
    print("🚀 Starting CSS file updates...")
    update_css_files()
    print("\n📦 Forcing GitHub Pages rebuild...")
    force_pages_rebuild()
    print("\n✨ Done! Site should update in a few minutes.")
    print("🌐 Check https://nicksanford2323.github.io/electrical-business-web-1/")