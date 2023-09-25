from bs4 import BeautifulSoup
import requests
import logging
import os

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
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
    # Read HTML file
    with open(file_location, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')

    # Extract all links
    links = soup.find_all('a')
    total_entries = len(links)
    logging.info(f"Found {total_entries} bookmarks in {file_location}")

    # Remove duplicate URLs
    unique_urls = {}
    new_links = []

    for link in links:
        url = link.get('href', '').strip()
        normalized_url = normalize_url(url)

        if normalized_url and normalized_url not in unique_urls:
            unique_urls[normalized_url] = True
            new_links.append(link)
        else:
            duplicates_removed += 1
            link.extract()

    logging.info(
        f"Removed {duplicates_removed} duplicates. {len(new_links)} unique bookmarks remaining.")

    # Fetch missing descriptions
    for link in new_links:
        url = link.get('href', '').strip()
        description = link.string if link.string else ''

        if url and not description:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    parsed_url = urlparse(url)
                    link.string = f"Description for {parsed_url.netloc}"
                    descriptions_fetched += 1
            except Exception as e:
                logging.error(
                    f"Failed to fetch description for URL {url}: {e}")

    # Write the updated HTML back to a new file
    new_file_location = f"updated_{file_location}"
    with open(new_file_location, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    logging.info(f"Saved updated bookmarks to {new_file_location}")

    # Show statistics
    print(f"Total entries: {total_entries}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Descriptions fetched: {descriptions_fetched}")

except Exception as e:
    logging.error(f"An error occurred: {e}")
