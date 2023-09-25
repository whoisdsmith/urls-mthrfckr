![Banner](banner.png)

# URLS-MTHRFCKR

## Table of Contents

1. [Cleanr](###cleanr)
2. [CSVRL](###cvrl)
3. [HTMRL](###htmrl)
4. [MDURL](###mdurl)
5. [RDURL](###rdrl)

<!-- ABOUT THE PROJECT -->

This is a collection of python scripts that will:

- Clean your Bookmark files of non-ascii characters with cleanr.py (I use this because my collection of exported bookmarks always seems to have some bad unicode characters and this script fixes that) If you don;t have these issues than don't use it, but if you do use it, make sure to run this first.
- Dedupe, fetch url descriptions and url images for CSV files using cvrl.py
- Dedupe and fetch url descriptions for bookmark.html files using htmrl.py
- Dedupe and fetch url descriptions for Raindrop.io exported html files using raindrophtml.py
- Dedupe and fetch url descriptions for any markdown file using mdurl.py

### CLEANR

#### Overview

The File Cleanup Utility is a Python script that removes non-ASCII characters from various types of files including CSV, HTML, and Markdown. It normalizes non-ASCII characters to their closest ASCII equivalents or removes them entirely.

#### Features

- **Support for multiple file types**: CSV, HTML, and Markdown.
- **Logging**: Detailed logging to a `.log` file.
- **User-Friendly**: Interactive command-line interface for easy usage.
- **Statistics**: Shows the total number of changes made during the process.

#### Dependencies

- Python 3.x
- BeautifulSoup4 (`pip install beautifulsoup4`)

#### Installation

1. Clone the repository or download the script to your local machine.
2. Make sure Python is installed.
3. Install required Python packages.

```bash
pip install beautifulsoup4
```

#### Usage

Run the script in your terminal:

```bash
python file_cleanup.py
```

You will be prompted to enter the file path and specify the file type (csv, html, md).

#### Functions

- `remove_non_ascii(text: str) -> Tuple[str, int]` - Replaces non-ASCII characters in a given text string with their closest ASCII equivalent or removes them. Returns a tuple with the new text and the number of changes made.
- `process_csv(file_path: str) -> int` - Processes a CSV file to remove non-ASCII characters. Returns the total number of changes made.
- `process_html(file_path: str) -> int` - Processes an HTML file to remove non-ASCII characters using BeautifulSoup. Returns the total number of changes made.
- `process_md(file_path: str) -> int` - Processes a Markdown file to remove non-ASCII characters. Returns the total number of changes made.
- `main()` - The main function which orchestrates the file cleanup process based on user input.

#### Logs

Logs are saved in a file named `file_cleanup.log` in the same directory as the script.

---

### CSVRL

This script reads a CSV file containing bookmark information, processes the URLs, and writes the updated data to a new CSV file. It performs the following tasks:

- Normalizes the URLs to remove redundant protocols.
- Removes duplicate URLs.
- Fetches book descriptions from the URLs using BeautifulSoup.
- Fetches book cover images using BeautifulSoup.
- Writes the updated data to a new CSV file.

To use the script, follow these steps:

#### Instructions

1. Save the script wherever you wish.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is saved.
4. Run the script with the following command:

`python cvrl.py`

- The script will prompt you to enter the path to the CSV file.
- After providing the file path, the script will process the URLs.
- Fetch descriptions and cover images.
- Write the updated data to a new CSV file.
- Real time logging in the console as the script is running.
- It also creates a log file called url_processing.log

---

### HTMRL

This script processes an HTML bookmark file to deduplicate URLs and fetch missing descriptions.

#### Usage

To use this script:

1. Ensure you have Python 3 and the required modules installed:
   - BeautifulSoup
   - Requests
   - Logging

2. Save the `htmrl.py` script and run:

	```python
    python htmrl.py
    ```

3. Enter the path to your HTML bookmark file when prompted.
4. The script will process the file, removing duplicates and fetching descriptions.
5. Updated output will be saved to a new HTML file.
6. Progress and statistics will be logged to the console and bookmark_processing.log.

#### What it Does

- Normalizes URLs to remove duplicate protocols
- Removes duplicate bookmark URLs
- Fetches missing descriptions using Requests
- Writes updated bookmarks to a new HTML file
- Provides statistics and logging

#### Requirements

- Python 3
- BeautifulSoup
- Requests
- Logging

---

### MDURL

`mdurl.py` is a Python script that helps you manage URLs in your markdown files. It can fetch the description of a URL and normalize the URL for consistency.

#### Features

- Fetch Description - This script can fetch the description of a URL by sending a GET request to the URL and parsing the HTML response to find the meta description tag.
- Normalize URL - This script can normalize a URL by converting it to lowercase and removing the 'http://' or 'https://' prefix and trailing slashes.

#### Functions

- `fetch_description(url)` - This function sends a GET request to the provided URL and parses the HTML response to find the meta description tag. If the description is found, it is returned. If any error occurs during this process, it is logged and None is returned.
- `normalize_url(url)`  - This function normalizes the provided URL by converting it to lowercase, removing the 'http://' or 'https://' prefix, and removing any trailing slashes.

#### Dependencies

This script depends on the following Python libraries:

`requests` - For sending HTTP requests.  
`BeautifulSoup` - For parsing HTML responses.

Make sure to install these dependencies using pip

---

### RDURL

This Python script is designed to process an HTML bookmark file, removing duplicate bookmarks and fetching missing descriptions for bookmarks. The script uses the following Python modules:

- `bs4` (BeautifulSoup) For parsing the HTML bookmark file
- `requests` For fetching descriptions for bookmarks
- `logging` For logging errors and information
- `os` For file handling

#### Usage

To use this script, follow these steps:

1. Ensure that the required Python modules are installed ( `bs4` , `requests` , `logging` , and `os` ).
2. Run the script.
3. When prompted, enter the path to the HTML bookmark file to be processed.
4. The script will remove duplicate bookmarks and fetch missing descriptions, and save the updated HTML to a new file in the same directory as the original file.

#### Code Overview

- The script begins by importing the required Python modules ( `bs4` , `requests` , `logging` , and `os` ).
- Next, the script initializes logging, statistics counters, and a function to normalize URLs.
- The user is prompted for the path to the HTML bookmark file to be processed.
- The script then reads the HTML file using `BeautifulSoup` , and initializes a dictionary to hold unique URLs.
- The script iterates through all `<DT>` tags containing bookmarks, and extracts the URL and description (if available) for each bookmark.
- Duplicate URLs are removed, and missing descriptions are fetched using `requests` , if possible.
- Finally, the updated HTML is saved to a new file in the same directory as the original file, and statistics are displayed to the user.

---
