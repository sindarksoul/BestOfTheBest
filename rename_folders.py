import os
import re
import logging
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

def rename_folders(target_path):
    """Renames folders inside target directory while preserving internal data"""
    try:
        if not validate_directory(target_path):
            return

        # Ensure `target_folder_path.txt` is updated with the latest path
        script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        target_folder_file = os.path.join(script_dir, "target_folder_path.txt")
        with open(target_folder_file, "w", encoding="utf-8") as file:
            file.write(target_path)

        logging.basicConfig(
            filename=os.path.join(target_path, "debug.txt"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        folders = sorted(os.listdir(target_path))
        renamed_count = 0
        for index, folder in enumerate(tqdm(folders, desc="Renaming folders"), start=1):
            folder_path = os.path.join(target_path, folder)
            if os.path.isdir(folder_path):
                new_name = f"folder{index}"
                new_path = os.path.join(target_path, new_name)

                # Ensure new name is unique
                if os.path.exists(new_path):
                    logging.warning(f"Skipping {folder}: {new_name} already exists.")
                    continue

                os.rename(folder_path, new_path)
                renamed_count += 1
                logging.info(f"Renamed: {folder} -> {new_name}")
                print(f"Renamed: {folder} -> {new_name}")

        logging.info(f"Renamed {renamed_count} folders successfully.")
        print(f"Renamed {renamed_count} folders successfully.")

    except Exception as e:
        logging.error(f"Error encountered: {e}")
        print(f"Error encountered: {e}")

if __name__ == "__main__":
    target_directory = input("Enter the target folder path: ").strip()
    rename_folders(target_directory)
