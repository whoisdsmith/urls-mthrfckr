import requests
import re
from bs4 import BeautifulSoup


def fetch_description_and_title(url):
    """Fetch the description and title of a given URL."""
    try:
        # Sending a GET request to fetch the raw HTML content
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Fetch description meta tag
        description_tag = soup.find('meta', attrs={'name': 'description'}) or \
            soup.find('meta', attrs={'property': 'og:description'})

        # Fetch title tag
        title_tag = soup.find('title')

        description = "Description not available"
        title = "Unknown"

        if description_tag and 'content' in description_tag.attrs:
            description = description_tag['content']

        if title_tag:
            title = title_tag.string

        return description, title
    except Exception as e:
        return f"Error: {e}", "Error"


def main():
    # Prompt for a bulk list of URLs
    urls_input = input("Enter the URLs (can be plain or in markdown format): ")

    # Use regex to extract URLs. This will find both markdown and plain URLs
    url_patterns = re.findall(r'\[.*?\]\((.*?)\)|https?://\S+', urls_input)

    # Open a markdown file for writing with UTF-8 encoding
    with open('link_descriptions.md', 'w', encoding='utf-8') as f:
        for url in url_patterns:
            url = url.strip()

            # Fetch description and title
            description, title = fetch_description_and_title(url)

            # Write to markdown file
            f.write(f"- [{title}]({url}) - {description}\n")


if __name__ == "__main__":
    main()
