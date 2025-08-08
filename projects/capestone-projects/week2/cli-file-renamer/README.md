# File System CLI Tool

A command-line interface (CLI) tool written in Python for common file system operations, including generating folder reports, renaming and moving files, and safely duplicating folders.
## Installation

This tool is a single Python script and does not require any special installation. Simply download the `file_utility.py` file.

### Requirements

* **Python 3.x**

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved `file_utility.py`.
3.  Run the script using the following command:

    ```bash
    python file_utility.py
    ```

4.  Follow the on-screen menu to select an operation.

## Available Operations

The tool provides the following functions:

1.  **Generate a folder report:**
    * Prompts for a source folder path.
    * Creates a `Report.txt` file in the source folder, listing all files and subdirectories.

2.  **Rename and move files:**
    * Prompts for a source folder path and a new name to append to file names.
    * Creates a new subfolder inside the source folder with the provided name.
    * Moves all files from the source folder into this new subfolder, appending the new name to each file.

3.  **Safely duplicate a folder:**
    * Prompts for a source folder path and a destination folder path.
    * Copies the entire contents of the source folder to the destination.
    * **This operation is "safe" because it will abort if the destination folder already exists, preventing accidental overwrites.**

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Author

* Ameer Hamza