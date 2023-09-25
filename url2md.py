import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_description_and_title(url):
    """Fetch the description and title of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        description_tag = soup.find('meta', attrs={'name': 'description'}) or \
            soup.find('meta', attrs={'property': 'og:description'})
        title_tag = soup.find('title')

        description = "Description not available"
        title = "Unknown"

        if description_tag and 'content' in description_tag.attrs:
            description = description_tag['content']

        if title_tag:
            title = title_tag.string

        return url, title, description

    except requests.exceptions.RequestException as e:
        return url, "Error", f"Error: {e}"
    except AttributeError as e:
        return url, "Error", f"Error: {e}"


def main():
    urls_input = input("Enter the URLs (can be plain or in markdown format): ")

    url_patterns = re.findall(
        r'(?:\[.*?\]\()?(https?://\S+)(?:\))?', urls_input)

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.now().strftime('%Y-%m-%d')

    link_data = []

    for url in url_patterns:
        url = url.strip()

        url, title, description = fetch_description_and_title(url)
        link_data.append((url, title, description))

    # Sort the data based on the title
    link_data.sort(key=lambda x: x[1])

    with open('link_descriptions.md', 'w', encoding='utf-8') as f:
        # Write the current date as an h3 heading at the beginning of the markdown file
        f.write(f"### {current_date}\n\n")

        for url, title, description in link_data:
            f.write(f"- [{title}]({url}) - {description}\n")


if __name__ == "__main__":
    main()
