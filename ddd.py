import os
import sys
import requests
import json
import base64
import logging

# ---------------------------------------------------------------------------------
# LOGGING SETUP
# ---------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,  # Set to logging.INFO if you want less detail
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------
# CONFIGURE THESE
# ---------------------------------------------------------------------------------
GITHUB_USERNAME = "nicksanford2323"       # Your GitHub username
REPO_NAME = "business-data-fixed2"       # Your repo name
ABOUT_FILEPATH = "about.json"            # Path in the repo to about.json
DATA_FILEPATH = "data.json"              # Path in the repo to data.json
COMMIT_MESSAGE = "Merged about_us from about.json into data.json"

# In Replit, store GITHUB_TOKEN in Secrets
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    logger.error("Error: GITHUB_TOKEN not found in environment variables.")
    sys.exit(1)

logger.debug(f"GITHUB_USERNAME={GITHUB_USERNAME}, REPO_NAME={REPO_NAME}")
logger.debug(f"ABOUT_FILEPATH={ABOUT_FILEPATH}, DATA_FILEPATH={DATA_FILEPATH}")
logger.debug(f"GITHUB_TOKEN found? {'YES' if GITHUB_TOKEN else 'NO'}")

# GitHub API base
API_BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


# ---------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------------

def get_file_from_github(filepath):
    """
    Fetches a file from GitHub repo via the contents API.
    Returns a tuple (decoded_str, sha).
    """
    url = f"{API_BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    logger.debug(f"Attempting GET {url}")
    resp = requests.get(url, headers=HEADERS)
    logger.debug(f"Response code: {resp.status_code}")
    if resp.status_code == 200:
        j = resp.json()
        content_base64 = j.get("content")
        sha = j.get("sha")
        if not content_base64 or not sha:
            logger.error(f"Missing 'content' or 'sha' in JSON response: {j}")
            sys.exit(1)
        decoded_str = base64.b64decode(content_base64).decode("utf-8")
        logger.debug(f"Successfully fetched {filepath}, length={len(decoded_str)} chars")
        return decoded_str, sha
    else:
        logger.error(f"Error fetching {filepath}: HTTP {resp.status_code}")
        logger.error(resp.json())
        sys.exit(1)

def put_file_to_github(filepath, new_content_str, old_sha):
    """
    PUT (commit) a file back to GitHub with new content & commit message.
    """
    url = f"{API_BASE_URL}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    logger.debug(f"Attempting PUT {url}")
    encoded_content = base64.b64encode(new_content_str.encode("utf-8")).decode("utf-8")
    payload = {
        "message": COMMIT_MESSAGE,
        "content": encoded_content,
        "sha": old_sha
    }
    logger.debug(f"Payload for PUT:\n{json.dumps(payload)[:500]}... (truncated)")

    resp = requests.put(url, headers=HEADERS, json=payload)
    logger.debug(f"Response code: {resp.status_code}")
    if resp.status_code in (200, 201):
        logger.info(f"Successfully updated {filepath} in GitHub.")
    else:
        logger.error(f"Error updating {filepath}: HTTP {resp.status_code}")
        logger.error(resp.json())
        sys.exit(1)

def merge_about_data(about_data, main_data):
    """
    Merges the 'about_us' text from about_data into main_data's 'sections.aboutUs' array.
    Returns (updated_main_data, match_count, update_count).
    """
    match_count = 0
    update_count = 0

    for place_id, about_obj in about_data.items():
        # about_obj should have "about_us"
        if "about_us" not in about_obj:
            logger.debug(f"No 'about_us' for place_id={place_id}, skipping.")
            continue

        about_text = about_obj["about_us"].strip()
        if not about_text:
            logger.debug(f"'about_us' empty for place_id={place_id}, skipping.")
            continue

        if place_id in main_data:
            match_count += 1

            # Ensure sections.aboutUs exists
            main_data[place_id].setdefault("sections", {})
            main_data[place_id]["sections"].setdefault("aboutUs", [])

            about_us_list = main_data[place_id]["sections"]["aboutUs"]

            # Skip if exact text already there
            already_exists = any(
                (item.get("reason", "").strip() == about_text)
                for item in about_us_list
            )

            if not already_exists:
                about_us_list.append({
                    "imageIndex": "",
                    "reason": about_text
                })
                update_count += 1
                logger.debug(f"Appended about_us text to place_id={place_id}")
        else:
            logger.debug(f"place_id={place_id} not in data.json, skipping merge.")

    return main_data, match_count, update_count


# ---------------------------------------------------------------------------------
# MAIN LOGIC
# ---------------------------------------------------------------------------------

def main():
    # 1) Fetch about.json
    logger.info(f"Fetching {ABOUT_FILEPATH} from GitHub...")
    about_str, about_sha = get_file_from_github(ABOUT_FILEPATH)
    about_data = json.loads(about_str)

    # 2) Fetch data.json
    logger.info(f"Fetching {DATA_FILEPATH} from GitHub...")
    data_str, data_sha = get_file_from_github(DATA_FILEPATH)
    main_data = json.loads(data_str)

    # 3) Merge about_us text
    logger.info("Merging about_us fields...")
    merged_data, match_count, update_count = merge_about_data(about_data, main_data)

    logger.info(f"Found {match_count} matching place IDs.")
    logger.info(f"Appended new about_us entries for {update_count} IDs (no duplicates).")

    # 4) Convert merged result back to JSON
    merged_str = json.dumps(merged_data, indent=2, ensure_ascii=False)

    # 5) PUT updated data.json back to GitHub
    logger.info(f"Updating {DATA_FILEPATH} in GitHub...")
    put_file_to_github(DATA_FILEPATH, merged_str, data_sha)

    logger.info("Done.")


if __name__ == "__main__":
    main()
