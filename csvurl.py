import csv
import requests
import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import os

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('url_processing.log'),
        logging.StreamHandler()
    ]
)

# Initialize statistics counters
total_entries = 0
duplicates_removed = 0
descriptions_fetched = 0
cover_images_fetched = 0

# Function to normalize URLs


def normalize_url(url):
    url = url.lower().replace('http://', '').replace('https://', '')
    return url.rstrip('/')

# Function to fetch cover image URL using BeautifulSoup


def fetch_cover_image(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            image_tag = soup.find('img')
            if image_tag and 'src' in image_tag.attrs:
                return image_tag['src']
        return None
    except Exception as e:
        logging.error(f"Failed to fetch cover image for URL {url}: {e}")
        return None


# Prompt user for file location
file_location = input("Enter the path to the CSV file: ")

# ... (rest of your code remains unchanged)

try:
    # Read CSV file into a dictionary
    with open(file_location, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        data = [row for row in reader]
        total_entries = len(data)

    logging.info(f"Read {total_entries} rows from {file_location}")

   # Remove duplicate URLs
    unique_urls = {}
    new_data = []
    for row in data:
        # Safeguard against None values
        url = row.get('url', '').strip() if row.get('url') else ''
        normalized_url = normalize_url(url)
        if normalized_url and normalized_url not in unique_urls:
            unique_urls[normalized_url] = True
            new_data.append(row)
        elif normalized_url:
            duplicates_removed += 1

    logging.info(
        f"Removed {duplicates_removed} duplicates. {len(new_data)} unique rows remaining")

    # Write updated data back to the original CSV file
    with open(file_location, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)

    logging.info(f"Wrote {len(new_data)} rows back to {file_location}")

    # Show statistics
    print(f"Total entries: {total_entries}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Descriptions fetched: {descriptions_fetched}")
    print(f"Cover images fetched: {cover_images_fetched}")

except Exception as e:
    logging.error(f"An error occurred: {e}")
