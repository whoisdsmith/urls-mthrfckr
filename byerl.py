import re
import logging
from collections import OrderedDict

# Configure logging to write logs to a file and to the console
logging.basicConfig(filename="remove_duplicates.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Add a logging handler to print log messages to the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Function to remove duplicate URLs


def remove_duplicate_urls(content):
    url_dict = OrderedDict()
    duplicates = 0

    # Use regex to match http:// and https://, excluding trailing backslashes
    url_pattern = re.compile(r"https?://[^\s\)\]\>]+")

    # Find all URLs
    urls = url_pattern.findall(content)
    logging.info(f"Total URLs found: {len(urls)}")

    # Check for duplicates and only keep one out of each duplicate group
    for url in urls:
        url = re.sub(r"/$", "", url)  # Remove trailing backslash if exists
        if url not in url_dict:
            url_dict[url] = 1
        else:
            url_dict[url] += 1
            duplicates += 1
            # Remove one instance of the duplicate URL
            content = content.replace(url, "", 1)

    logging.info(f"Total duplicates found and removed: {duplicates}")

    return content, len(urls), duplicates


# Main function
if __name__ == "__main__":
    # Prompt for the input of a markdown file
    markdown_file_path = input("Enter the path of the markdown file: ")

    try:
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        logging.info("Reading markdown file...")

        # Remove duplicate URLs
        new_content, total_urls, duplicates = remove_duplicate_urls(content)

        # Write the new content back to the file
        with open(markdown_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        logging.info(
            "Successfully removed duplicates and updated markdown file.")
        print(f"Total URLs: {total_urls}, Duplicates Removed: {duplicates}")

    except FileNotFoundError:
        logging.error(f"File {markdown_file_path} not found.")
        print("File not found. Please check the file path.")
