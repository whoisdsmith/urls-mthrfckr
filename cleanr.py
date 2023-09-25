import csv
import logging
import unicodedata
from pathlib import Path
from bs4 import BeautifulSoup

# Initialize logging
logging.basicConfig(filename='file_cleanup.log', level=logging.INFO)

def remove_non_ascii(text):
    """
    Replace non-ASCII characters with their closest ASCII equivalent or remove them.
    """
    new_text = []
    changes = 0
    for char in text:
        normalized_char = unicodedata.normalize('NFD', char)
        ascii_char = normalized_char.encode('ascii', 'ignore').decode('ascii')
        if char != ascii_char:
            changes += 1
        new_text.append(ascii_char)
    return ''.join(new_text), changes

def process_csv(file_path):
    """
    Process a CSV file to remove non-ASCII characters.
    """
    # Initialize change counter
    total_changes = 0
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            data = list(reader)
            
        new_data = []
        for row in data:
            new_row = []
            for cell in row:
                new_cell, changes = remove_non_ascii(cell)
                new_row.append(new_cell)
                total_changes += changes
            new_data.append(new_row)
            
        with open(file_path, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(new_data)
            
        return total_changes

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1

def process_html(file_path):
    """
    Process an HTML file to remove non-ASCII characters.
    """
    # Initialize change counter
    total_changes = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            soup = BeautifulSoup(infile, 'html.parser')
        
        for string in soup.stripped_strings:
            new_string, changes = remove_non_ascii(string)
            string.replace_with(new_string)
            total_changes += changes
            
        with open(file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(str(soup))
            
        return total_changes

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1

def process_md(file_path):
    """
    Process a Markdown file to remove non-ASCII characters.
    """
    # Initialize change counter
    total_changes = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        new_content, total_changes = remove_non_ascii(content)
        
        with open(file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(new_content)
            
        return total_changes

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return -1

def main():
    file_path = input("Please enter the path to the file: ")
    file_type = input("Please enter the file type (csv, html, md): ").strip().lower()
    p = Path(file_path)
    
    if not p.is_file():
        logging.error(f"File {file_path} does not exist.")
        print("Invalid file path. Please check the log for more details.")
        return

    if file_type == 'csv':
        changes = process_csv(file_path)
    elif file_type == 'html':
        changes = process_html(file_path)
    elif file_type == 'md':
        changes = process_md(file_path)
    else:
        print("Unsupported file type.")
        return

    if changes >= 0:
        print(f"Total changes made: {changes}")
    else:
        print("An error occurred while processing the file. Please check the log for more details.")

if __name__ == "__main__":
    main()

