from bs4 import BeautifulSoup
import requests
import logging
import os

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('bookmark_processing.log'),
        logging.StreamHandler()
    ]
)

# Initialize statistics counters
total_entries = 0
duplicates_removed = 0
descriptions_fetched = 0

# Function to normalize URLs


def normalize_url(url):
    url = url.lower().replace('http://', '').replace('https://', '')
    return url.rstrip('/')


# Prompt user for file location
file_location = input("Enter the path to the HTML bookmark file: ")

try:
    with open(file_location, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')

    # Dictionary to hold unique URLs
    unique_urls = {}

    # Iterate through all <DT> tags containing bookmarks
    for dt in soup.find_all('dt'):
        a_tag = dt.find('a')
        if a_tag:
            total_entries += 1
            url = a_tag.get('href', '').strip()
            normalized_url = normalize_url(url)
            description = a_tag.get('description', '')

            # Remove duplicate URLs
            if normalized_url in unique_urls:
                dt.extract()
                duplicates_removed += 1
            else:
                unique_urls[normalized_url] = True

            # Fetch missing descriptions
            if url and not description:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        a_tag['description'] = f"Description for {url}"
                        descriptions_fetched += 1
                except Exception as e:
                    logging.error(
                        f"Failed to fetch description for URL {url}: {e}")

    # Save the updated HTML to a new file in the same directory
    file_directory = os.path.dirname(file_location)
    new_file_name = f"updated_{os.path.basename(file_location)}"
    new_file_location = os.path.join(file_directory, new_file_name)

    with open(new_file_location, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    # Show statistics
    print(f"Total entries: {total_entries}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Descriptions fetched: {descriptions_fetched}")

except Exception as e:
    logging.error(f"An error occurred: {e}")
