import os
import re
import time
from datetime import datetime
import sys
from tqdm import tqdm

def validate_directory(path):
    """Validates the target directory path."""
    if not os.path.exists(path):
        print("Invalid directory path.")
        return False
    if not os.path.isdir(path):
        print("The path is not a directory.")
        return False
    return True

# Get target folder path from target_folder_path.txt
root_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
target_folder_file = os.path.join(root_dir, "target_folder_path.txt")

if not os.path.exists(target_folder_file):
    print("Error: target_folder_path.txt not found.")
    sys.exit()

with open(target_folder_file, "r", encoding="utf-8") as f:
    target_folder = f.read().strip()

# Ensure target folder exists
if not validate_directory(target_folder):
    sys.exit()

compilation_file = os.path.join(root_dir, "compilation.txt")

if not os.path.exists(compilation_file):
    print("Error: compilation.txt not found in the program root folder.")
    sys.exit()

# Output files
filtered_credentials_file = os.path.join(root_dir, "filtered_credentials.txt")
debug_log = os.path.join(root_dir, "debug.txt")

# Prompt user for the keyword
keyword = input("Enter keyword (e.g., mega.nz, github.com, onedrive.com): ").strip().lower()

# Generate all possible URL formats
url_variants = [
    f"http://{keyword}",
    f"https://{keyword}",
    f"http://www.{keyword}",
    f"https://www.{keyword}"
]

# Log start time
start_time = time.time()

# Logging function
def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(debug_log, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} {message}\n")

# Processing starts
log_message(f"Processing started for keyword: {keyword}")

try:
    extracted_credentials = []

    with open(compilation_file, "r", encoding="utf-8") as file:
        data = file.read()

        # Find all entries with USER and PASS
        matches = re.findall(r"URL:\s*(https?://\S+)\s*USER:\s*([\w\.\-\@]+)\s*PASS:\s*([\S]+)", data, re.IGNORECASE)

        for url, user, password in tqdm(matches, desc="Extracting credentials"):
            if any(url.startswith(variant) for variant in url_variants):
                extracted_credentials.append(f"{user}:{password}")

    # Save results
    if extracted_credentials:
        with open(filtered_credentials_file, "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(extracted_credentials))
        
        log_message(f"Successfully extracted {len(extracted_credentials)} credentials.")
        print(f"Done! {len(extracted_credentials)} credentials saved in filtered_credentials.txt")
    else:
        log_message("No matching credentials found.")
        print("No matching credentials found.")

except Exception as e:
    log_message(f"Error occurred: {str(e)}")
    print(f"Error: {e}")

# Log completion time
end_time = time.time()
log_message(f"Processing completed in {end_time - start_time:.2f} seconds.")
