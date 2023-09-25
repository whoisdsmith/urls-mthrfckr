from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse
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

# Function to normalize URLs


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.netloc.rstrip('/')}{parsed_url.path.rstrip('/')}"

# Function to merge folders and remove empty folders


def merge_and_clean_folders(soup):
    folders = {}
    empty_folders = []

    # Iterate through DT tags, which usually represent folder items
    for dt in soup.find_all('dt'):
        folder_name_tag = dt.find('h3')

        if folder_name_tag:
            folder_name = folder_name_tag.string
            folder_contents = dt.find_next_sibling('dl')

            if folder_contents is not None:  # Check added here
                content_list = folder_contents.find_all('dt')

                # Merge folders with the same name
                if folder_name in folders:
                    folders[folder_name].extend(content_list)
                else:
                    folders[folder_name] = content_list

                # Mark folder as empty if it has no contents
                if len(content_list) == 0:
                    empty_folders.append(dt)
            else:
                logging.warning(
                    f"Folder {folder_name} has no content (DL tag is missing).")
                empty_folders.append(dt)

    # Delete empty folders
    for folder in empty_folders:
        folder.decompose()

    # Update the original soup object to reflect merged folders
    for folder_name, contents in folders.items():
        original_folder = soup.find('h3', string=folder_name)
        if original_folder:
            sibling_dl = original_folder.find_next_sibling('dl')
            if sibling_dl:
                sibling_dl.clear()
                for content in contents:
                    sibling_dl.append(content)
            else:
                logging.warning(f"Folder {folder_name} has no DL tag.")


# Prompt user for file location
file_location = input("Enter the path to the HTML bookmark file: ")

if os.path.isfile(file_location) and file_location.endswith('.html'):
    try:
        # Read HTML file
        with open(file_location, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'lxml')

        # Merge folders and remove empty folders
        merge_and_clean_folders(soup)

        # Extract all links
        links = soup.find_all('a')
        total_entries = len(links)
        logging.info(f"Found {total_entries} bookmarks in {file_location}")

        # Remove duplicate URLs
        unique_urls = set()
        new_links = []

        for link in links:
            url = link.get('href', '').strip()
            normalized_url = normalize_url(url)

            if normalized_url and normalized_url not in unique_urls:
                unique_urls.add(normalized_url)
                new_links.append(link)
            else:
                duplicates_removed += 1
                link.extract()

        logging.info(
            f"Removed {duplicates_removed} duplicates. {len(new_links)} unique bookmarks remaining.")

        # Split the original filepath into components
        drive, path = os.path.splitdrive(file_location)
        path, filename = os.path.split(path)

        # Replace invalid characters in the filename
        new_filename = f"updated_{filename.replace(':', '_')}"

        # Join the components back into a new filepath
        new_file_location = os.path.join(drive, path, new_filename)

        with open(new_file_location, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        logging.info(f"Saved updated bookmarks to {new_file_location}")

        # Show statistics
        print(f"Total entries: {total_entries}")
        print(f"Duplicates removed: {duplicates_removed}")

    except (FileNotFoundError, IOError) as e:
        logging.error(f"An error occurred: {e}")
else:
    logging.error("Invalid path or file is not an HTML file.")
