import requests
from bs4 import BeautifulSoup
import re
import logging
import os

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('markdown_processing.log'),
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

# Function to fetch description from URL


def fetch_description(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        description = soup.find('meta', {'name': 'description'}) or soup.find(
            'meta', {'property': 'og:description'})

        if description:
            return description.get('content')
    except Exception as e:
        logging.error(f"Failed to fetch description for URL {url}: {e}")
        return None


# Prompt user for file location
file_location = input("Enter the path to the Markdown file: ")

try:
    # Read the Markdown file
    with open(file_location, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Dictionary to hold unique URLs
    unique_urls = {}

    # List to hold the updated lines
    updated_lines = []

    # Process each line in the Markdown file
    for line in lines:
        match = re.search(r'- \[(.*?)\]\((.*?)\) - (.+)', line)

        if match:
            total_entries += 1

            title, url, description = match.groups()
            normalized_url = normalize_url(url)

            if normalized_url in unique_urls:
                duplicates_removed += 1
                logging.info(f"Duplicate found and removed: {url}")
            else:
                unique_urls[normalized_url] = True

                if not description:
                    new_description = fetch_description(url)
                    if new_description:
                        line = line.replace(
                            f']({url}) -', f']({url}) - {new_description}')
                        descriptions_fetched += 1
                        logging.info(f"Description fetched for: {url}")

                updated_lines.append(line)
        else:
            # Add lines that don't match the Markdown link format as is
            updated_lines.append(line)

    # Save the updated Markdown to a new file in the same directory
    file_directory = os.path.dirname(file_location)
    new_file_name = f"updated_{os.path.basename(file_location)}"
    new_file_location = os.path.join(file_directory, new_file_name)

    with open(new_file_location, 'w', encoding='utf-8') as file:
        file.write(''.join(updated_lines))

    # Show statistics
    print(f"Total entries: {total_entries}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Descriptions fetched: {descriptions_fetched}")

except Exception as e:
    logging.error(f"An error occurred: {e}")
