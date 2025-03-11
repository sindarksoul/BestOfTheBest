# PYKILLER_REWORK

## Overview

This tool automates the process of renaming folders, compiling data, and extracting credentials. It consists of three main modules:

1. `rename_folders.exe`
2. `compile_data.exe`
3. `dline.exe`

The `main.exe` supervises the entire process flow.

## Usage

### Step 1: Run `main.exe`

Run the `main.exe` executable to start the process. The tool will guide you through the following steps:

1. **Rename Folders**: The tool will prompt you to enter the target folder path. It will then rename all subfolders and sub-subfolders recursively.
2. **Compile Data**: The tool will extract data from the renamed folders and generate `compilation.txt`, `jobdone.txt`, and `debug.txt` in the target folder.
3. **Extract Credentials**: The tool will prompt you to enter a keyword for final extraction from `compilation.txt`. It will generate the final output file `filtered_credentials.txt` in the program root folder.

### Step 2: Check Output Files

- `target_folder_path.txt`: Contains the path of the target folder.
- `debug.txt`: Contains logs for debugging purposes.
- `compilation.txt`: Contains structured log data.
- `jobdone.txt`: Contains extracted credentials in `user:pass` format.
- `filtered_credentials.txt`: Contains filtered credentials based on the entered keyword.

## Requirements

- Python 3.x
- `tqdm` library (for progress bars)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/YOUR_USERNAME/PYKILLER_REWORK.git
    ```

2. Navigate to the project directory:

    ```sh
    cd PYKILLER_REWORK
    ```

3. Install the required library:

    ```sh
    pip install tqdm
    ```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.