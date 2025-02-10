import os
import sys
import base64
import json
import re
import requests

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
GITHUB_USERNAME = "nicksanford2323"
REPO_NAME = "business-data-fixed2"
FILE_PATH = "data.json"  # If it's in a subfolder, e.g. "folder/data.json"
COMMIT_MESSAGE = "Fix logo URLs by removing sXX-p-k-no-ns-nd snippet"

# Read token from Replit Secrets
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

# API base URLs
GET_CONTENT_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
# We'll use the same URL for PUT requests (GitHub content API)

# ------------------------------------------------------------------------------
# Helper function to remove the snippet from the logo URL
# ------------------------------------------------------------------------------
def remove_logo_snippet(logo_url: str) -> str:
    """
    Removes the 'sXX-p-k-no-ns-nd' snippet (with optional trailing slash)
    from the Google logo URL. Example:
      '.../s44-p-k-no-ns-nd/photo.jpg' -> '.../photo.jpg'
    """
    return re.sub(r's\d+-p-k-no-ns-nd/?', '', logo_url)

# ------------------------------------------------------------------------------
# 1. GET the existing file from GitHub
# ------------------------------------------------------------------------------
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

print(f"Fetching {FILE_PATH} from {REPO_NAME}...")
response = requests.get(GET_CONTENT_URL, headers=headers)

if response.status_code == 200:
    file_content = response.json()
    # Extract base64-encoded content
    encoded_content = file_content["content"]
    sha_value = file_content["sha"]
else:
    print(f"Error: Could not fetch {FILE_PATH}. HTTP {response.status_code}")
    print(response.json())
    sys.exit(1)

# Decode from base64 to string
decoded_str = base64.b64decode(encoded_content).decode("utf-8")

# Parse JSON
try:
    data = json.loads(decoded_str)
except json.JSONDecodeError as e:
    print("Error decoding JSON:", str(e))
    sys.exit(1)

# ------------------------------------------------------------------------------
# 2. Transform the data (clean up logos)
# ------------------------------------------------------------------------------
changed_count = 0

for place_id, place_data in data.items():
    if "businessInfo" in place_data:
        biz_info = place_data["businessInfo"]
        if "logo" in biz_info and biz_info["logo"]:
            original_logo = biz_info["logo"]
            cleaned_logo = remove_logo_snippet(original_logo)
            if cleaned_logo != original_logo:
                biz_info["logo"] = cleaned_logo
                changed_count += 1

print(f"Logos cleaned: {changed_count} changed.")

# ------------------------------------------------------------------------------
# 3. Encode updated JSON & PUT back to GitHub
# ------------------------------------------------------------------------------
updated_json_str = json.dumps(data, indent=2, ensure_ascii=False)
updated_base64 = base64.b64encode(updated_json_str.encode("utf-8")).decode("utf-8")

payload = {
    "message": COMMIT_MESSAGE,
    "content": updated_base64,
    "sha": sha_value
}

print(f"Committing updated {FILE_PATH} to GitHub...")

put_resp = requests.put(GET_CONTENT_URL, headers=headers, json=payload)

if put_resp.status_code in (200, 201):
    print("Success! data.json updated and committed to the repo.")
else:
    print(f"Error updating file. HTTP {put_resp.status_code}")
    print(put_resp.json())
    sys.exit(1)
