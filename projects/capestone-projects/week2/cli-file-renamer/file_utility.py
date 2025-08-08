# Project 2: Command-Line Interface (CLI) File Renamer
# Objective: Create a Python script that renames files in a specified directory based on a pattern or a new prefix/suffix.
from pathlib import Path
import shutil
#  Generate a folder report


def report_generator(source_folder_path):
    source_folder = Path(source_folder_path)
    Report_file = Path(source_folder / "Report.txt")
    with open(Report_file, "w") as file:
        file.write(f"----Directory Content.----\n\n")
        try:
            for item in source_folder.iterdir():
                if item.is_file():
                    file.write(f"  {item.name}\n")
                    print(f" -Found File: {item.name}")
                elif item.is_dir():
                    file.write(f"Directory:{item.name}\n")
                    print(f"Found Directory: {item.name}")
            print(f"Your Report has been generated at {source_folder.name}")
        except PermissionError:
            print("\nError: Permission denied. Please check folder permissions.")
        except Exception as e:
            # A generic exception catch is good for unexpected errors.
            print(f"\nAn unexpected error occurred during renaming: {e}")


def file_renamer(source_folder_path, new_name):
    source_folder = Path(source_folder_path)
    destination_folder = Path(source_folder / new_name)
    print(f"Starting to work on {source_folder.resolve()} now.")
    print(f"Starting to work on {destination_folder.resolve()} now.")

    if not source_folder.is_dir():
        print(
            f"Error: The path '{source_folder_path}' is not a valid directory.")
        return

    # Check if the destination folder exists, and if not, create it.
    if not destination_folder.exists():
        print(
            f"Destination folder '{destination_folder.name}' does not exist. Creating it now.")
        destination_folder.mkdir()
    print(f"\nStarting file processing and moving...")

    try:

        for item in source_folder.iterdir():
            if item.is_file():
                new_file = f"{item.stem}_{new_name}{item.suffix}"
                new_path = destination_folder / new_file
                item.rename(new_path)
                print(
                    f"Renamed and moved '{item.name}' to '{new_path.name}'\n")
            elif item.is_dir():
                print(f"Directory Found: {item.name}")
    except FileExistsError:
        print(f"That file does not exist. ")


def Safe_duplicate(source_folder_path, destination_folder_path):
    source_folder = Path(source_folder_path)
    destination_folder = Path(destination_folder_path)
    try:
        if destination_folder.exists():
            print(f"{destination_folder} already exists.\n Aborting...")
        else:
            shutil.copytree(source_folder, destination_folder)
            print(
                f"Backup successful. Folder '{source_folder.name}' copied to '{destination_folder.name}'.")
    except FileNotFoundError:
        print(
            f"Error: The source folder '{source_folder_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


while True:
    print("--- File System Tool ---")
    print("1. Generate a folder report")
    print("2. Rename and move files")
    print("3. Safely duplicate a folder")
    print("4. Exit")
    try:
        selection = float(input("\nSelect an operation: "))
        if 0 < selection < 5:
            if selection == 4:
                print(f"\nExiting the program. Good Bye!\n")
                break
            elif selection == 1:
                source_folder_path = input(
                    "Please provide the source folder: ")
                report_generator(source_folder_path)
            elif selection == 2:
                source_folder_path = input("Please provide the source folder:")
                new_name = input(
                    "Please provide the new name for files to append:")
                file_renamer(source_folder_path, new_name)

            elif selection == 3:
                source_folder_path = input(
                    "Please provide the source folder: ")
                destination_folder_path = input(
                    "Please provide the destination folder: ")
                Safe_duplicate(source_folder_path, destination_folder_path)
        else:
            print(f"\nPlease select a number from the range.\n")
    except ValueError:
        print("\nPlease select a number for the opration.\n")
    except Exception as e:
        print(f"An unexpected error occured: {e}")
