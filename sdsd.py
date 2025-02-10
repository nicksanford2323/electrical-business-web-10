import os
import sys
import base64
import json
import requests

# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------
GITHUB_USERNAME = "nicksanford2323"
REPO_NAME = "business-data-fixed2"
DATA_JSON_PATH = "data.json"     # Path in your GitHub repo to data.json
LOL_JSON_LOCAL = "d.json"      # The local file in Replit with final about-us data
COMMIT_MESSAGE = "Merging about_us from lol.json into data.json"

# Must be set in Replit Secrets or environment
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

# GitHub API
API_BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def fetch_file_from_github(filepath):
    """
    Uses GitHub Contents API to GET a file (base64-encoded).
    Returns (content_str, sha).
    """
    url = f"{API_BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        j = resp.json()
        encoded_content = j["content"]
        sha_value = j["sha"]
        decoded_str = base64.b64decode(encoded_content).decode("utf-8")
        return decoded_str, sha_value
    else:
        print(f"Error fetching {filepath}: HTTP {resp.status_code}")
        print(resp.json())
        sys.exit(1)


def put_file_to_github(filepath, new_content_str, old_sha):
    """
    PUT (commit) a file back to GitHub with new content + commit message.
    """
    url = f"{API_BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    encoded = base64.b64encode(new_content_str.encode("utf-8")).decode("utf-8")
    payload = {
        "message": COMMIT_MESSAGE,
        "content": encoded,
        "sha": old_sha
    }
    resp = requests.put(url, headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        print(f"Successfully updated {filepath} on GitHub.")
    else:
        print(f"Error updating {filepath}: HTTP {resp.status_code}")
        print(resp.json())
        sys.exit(1)


def merge_about_data(lol_data, main_data):
    """
    Merges the 'about_us' text from lol_data into main_data's 'sections.aboutUs' array.
    Avoids duplicates if that text already exists.
    Returns the merged dict.
    """
    match_count = 0
    update_count = 0

    for place_id, about_obj in lol_data.items():
        if "about_us" not in about_obj:
            continue
        about_text = about_obj["about_us"].strip()
        if not about_text:
            continue

        if place_id in main_data:
            match_count += 1
            # Ensure main_data has .sections.aboutUs
            main_data[place_id].setdefault("sections", {})
            main_data[place_id]["sections"].setdefault("aboutUs", [])

            about_us_list = main_data[place_id]["sections"]["aboutUs"]

            # Check if exact text is already there
            already_exists = any(
                (item.get("reason", "").strip() == about_text)
                for item in about_us_list
            )
            if not already_exists:
                # Append as a new entry
                about_us_list.append({
                    "imageIndex": "",
                    "reason": about_text
                })
                update_count += 1
        # else: place_id not in main_data, skip

    print(f"Found {match_count} matching place IDs in data.json.")
    print(f"Added new about_us entries for {update_count} IDs (no duplicates).")
    return main_data


def main():
    # 1) Load local lol.json
    if not os.path.exists(LOL_JSON_LOCAL):
        print(f"Error: {LOL_JSON_LOCAL} does not exist locally.")
        sys.exit(1)

    with open(LOL_JSON_LOCAL, "r", encoding="utf-8") as f:
        lol_data = json.load(f)

    # 2) Fetch data.json from GitHub
    data_str, data_sha = fetch_file_from_github(DATA_JSON_PATH)
    main_data = json.loads(data_str)

    # 3) Merge
    merged_data = merge_about_data(lol_data, main_data)

    # 4) Encode merged as JSON
    merged_str = json.dumps(merged_data, indent=2, ensure_ascii=False)

    # 5) PUT back to GitHub
    put_file_to_github(DATA_JSON_PATH, merged_str, data_sha)

    print("Done merging about_us data into data.json on GitHub.")


if __name__ == "__main__":
    main()
