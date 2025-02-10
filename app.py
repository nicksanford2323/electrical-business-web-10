import json
import csv

def main():
    # File path for your JSON file (adjust the path if necessary)
    input_filename = "46.json"
    # Output CSV filename
    output_filename = "business_data112.csv"

    # Base URL for preview links; we'll append the place ID as a query string parameter.
    base_preview_url = "https://79f7ed2b-4a25-41e2-be82-8a3341ae0aa1-00-3expw1nxlehl5.kirk.replit.dev/BAMAELECTRIC/"

    # Open and load the JSON data from file
    with open(input_filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Open the CSV file for writing
    with open(output_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # Write the CSV header
        header = ["business_name", "phone", "reviews_link", "reviews_count", "city", "preview_link"]
        writer.writerow(header)

        # Process each business entry in the JSON data.
        for place_id, details in data.items():
            # Get the business name from the outer key "businessName"
            business_name = details.get("businessName", "")

            # Get businessInfo dict (if missing, default to an empty dict)
            business_info = details.get("businessInfo", {})

            # Extract phone, reviews_link, review count, and city from the businessInfo dict
            phone = business_info.get("phone", "")
            reviews_link = business_info.get("reviews_link", "")
            reviews_count = business_info.get("reviews", "")
            city = business_info.get("city", "")

            # Construct the preview link by appending the place ID with '?id='
            preview_link = f"{base_preview_url}?id={place_id}"

            # Write the row to the CSV file
            writer.writerow([business_name, phone, reviews_link, reviews_count, city, preview_link])

    print(f"Data extracted and saved to {output_filename}")

if __name__ == "__main__":
    main()
