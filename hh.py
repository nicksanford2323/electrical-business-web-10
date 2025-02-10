import requests
import json

# Apify API endpoint with your token included
url = "https://api.apify.com/v2/acts/compass~crawler-google-places/run-sync-get-dataset-items?token=apify_api_N0oTi4xJtkyopQGrq0xPRYI9lNX24Q1ArbOq"

# Input payload with the list of place IDs
payload = {
    "placeIds": [
        "ChIJF09EatdHiIgRGcgGB0NOmko",
        "ChIJIabfr7TGi4gRxxXnBfB9PVk",
        "ChIJNXlekSCbJ0ERjtG2r3D36CA"
    ]
}

headers = {
    "Content-Type": "application/json"
}

def main():
    try:
        # Make the POST request to run the actor synchronously
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error during request:", e)
        return

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return

    # Expecting a list of results, each representing a place
    if not isinstance(data, list):
        print("Unexpected data format:")
        print(json.dumps(data, indent=2))
        return

    # Process each place and print its photo URLs.
    for idx, item in enumerate(data, start=1):
        print(f"\n=== Place {idx}: {item.get('title', 'No title provided')} ===")

        # Option 1: Check for "images" field (each item should have an "imageUrl")
        images = item.get("images")
        if images and isinstance(images, list) and len(images) > 0:
            print("Images:")
            for image in images:
                url = image.get("imageUrl")
                if url:
                    print(" -", url)
            continue  # go to next place

        # Option 2: If no "images", check for "imageUrls" field (an array of URLs)
        image_urls = item.get("imageUrls")
        if image_urls and isinstance(image_urls, list) and len(image_urls) > 0:
            print("Image URLs:")
            for img_url in image_urls:
                print(" -", img_url)
            continue

        print("No photos found for this place.")

if __name__ == "__main__":
    main()
