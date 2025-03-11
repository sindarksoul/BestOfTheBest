import os
import subprocess
import shutil
import sys
import time
from tqdm import tqdm

def run_executable(executable, args=[]):
    """Runs an executable and waits for it to complete."""
    try:
        result = subprocess.run([executable] + args, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running {executable}: {e}")
        return False

def wait_for_file(filepath, timeout=300):
    """Waits for a file to be created within a specified timeout."""
    start_time = time.time()
    while not os.path.exists(filepath):
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for {filepath}")
            return False
        time.sleep(1)
    return True

def main():
    # Step 1: Run rename_folders.exe
    print("Running rename_folders.exe...")
    if not run_executable("rename_folders.exe"):
        print("rename_folders.exe failed. Check debug.txt for details.")
        return

    # Ensure target_folder_path.txt is created
    script_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    target_folder_file = os.path.join(script_dir, "target_folder_path.txt")
    if not wait_for_file(target_folder_file):
        print("Error: target_folder_path.txt not found.")
        return

    with open(target_folder_file, "r", encoding="utf-8") as f:
        target_folder = f.read().strip()

    # Step 2: Run compile_data.exe
    print("Running compile_data.exe...")
    if not run_executable("compile_data.exe"):
        print("compile_data.exe failed. Check debug.txt for details.")
        return

    # Ensure compilation.txt is created
    compilation_file = os.path.join(target_folder, "compilation.txt")
    if not wait_for_file(compilation_file):
        print("Error: compilation.txt not found in the target folder.")
        return

    # Step 3: Transfer compilation.txt to the program root folder
    destination_file = os.path.join(script_dir, "compilation.txt")
    shutil.move(compilation_file, destination_file)
    print("Moved compilation.txt to the program root folder.")

    # Step 4: Run dline.exe
    print("Running dline.exe...")
    if not run_executable("dline.exe"):
        print("dline.exe failed. Check debug.txt for details.")
        return

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
