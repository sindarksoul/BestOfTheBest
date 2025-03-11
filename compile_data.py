import os
import re
import logging
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

def extract_credentials(data):
    """Extracts user:pass or email:pass from the given text (STRICTLY for jobdone.txt)"""
    credentials = []
    for match in re.finditer(r"(?:USER|EMAIL):\s*([\w\.\-\@]+)\s*\nPASS:\s*([\S]+)", data, re.IGNORECASE):
        credentials.append(f"{match.group(1)}:{match.group(2)}")  # STRICTLY formatted as user:pass or email:pass
    return credentials

def get_target_folder():
    """Fetch the target folder path from rename_folders.py output"""
    script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    rename_folders_log = os.path.join(script_dir, "target_folder_path.txt")  # File created by rename_folders.py

    if os.path.exists(rename_folders_log):
        with open(rename_folders_log, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        print("ERROR: Target folder path file not found! Ensure rename_folders.py has executed successfully.")
        return None

def compile_data():
    """Recursively processes all subfolders (at ANY depth) to extract credentials"""
    target_path = get_target_folder()
    if not target_path:
        return  # Stop execution if no valid target folder

    try:
        start_time = datetime.now()

        if not validate_directory(target_path):
            return

        # Define file paths (STRICTLY in root of target folder)
        compilation_file = os.path.join(target_path, "compilation.txt")
        jobdone_file = os.path.join(target_path, "jobdone.txt")
        debug_file = os.path.join(target_path, "debug.txt")

        # Ensure root files exist before writing
        for file in [compilation_file, jobdone_file, debug_file]:
            open(file, 'w').close()

        # Configure logging (STRICTLY logs in target folder)
        logging.basicConfig(
            filename=debug_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        compiled_data = []  # Stores structured log data (SOFT, URL, USER, PASS)
        extracted_credentials = []  # Stores user:pass and email:pass only (jobdone.txt)
        processed_files = 0

        # Recursively search for "All Passwords.txt" & "Passwords.txt" inside **ALL** subfolders
        for root, _, files in tqdm(os.walk(target_path), desc="Processing folders"):
            for file in files:
                if file in ["All Passwords.txt", "Passwords.txt"]:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                        # Extract credentials (STRICTLY for jobdone.txt)
                        extracted_credentials.extend(extract_credentials(content))

                        # Store full structured data for compilation.txt
                        compiled_data.append(content)

                        processed_files += 1
                        logging.info(f"Successfully processed: {file_path}")
                        print(f"Successfully processed: {file_path}")

                    except Exception as e:
                        logging.error(f"Failed to process {file_path}: {e}")
                        print(f"Failed to process {file_path}: {e}")

        # **WRITE compilation.txt (Structured Data with ALL details)**
        if compiled_data:
            with open(compilation_file, "w", encoding="utf-8") as comp_file:
                comp_file.write("\n\n".join(compiled_data))  # Store FULL structured logs (SOFT, URL, USER, PASS)
            logging.info(f"Compilation completed: {compilation_file}")

        # **WRITE jobdone.txt (ONLY user:pass format)**
        if extracted_credentials:
            with open(jobdone_file, "w", encoding="utf-8") as job_file:
                job_file.write("\n".join(extracted_credentials) + "\n")  # Strictly user:pass or email:pass
            logging.info(f"Extracted credentials saved: {jobdone_file}")

        # **LOG the process summary in debug.txt**
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logging.info(f"Processed {processed_files} files. Completed in {duration:.2f} seconds.")
        print(f"Processed {processed_files} files. Completed in {duration:.2f} seconds.")

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        print(f"Error encountered: {e}")

if __name__ == "__main__":
    compile_data()

