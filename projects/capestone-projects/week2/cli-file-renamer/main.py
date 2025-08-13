# main sctipt for the utility tool operational logic implimentation.
# Project 2: Command-Line Interface (CLI) File Utilities
# creates report.txt with all the files and directories in a specifies directory.
# Objective: Create a Python script that renames files in a specified directory based on a pattern or a new prefix/suffix.
from utility_ops import report_generator, file_renamer, Safe_duplicate

while True:  # initiates a loop to keep displaying the menu untill user chooses to exit.
    print("--- File System Tool ---")
    print("1. Generate a folder report")
    print("2. Rename and move files")
    print("3. Safely duplicate a folder")
    print("4. Exit")
    try:  # initiates error handeling
        # catches the user input and converts it into a float
        selection = float(input("\nSelect an operation: "))
        # checks the userinput to determine the option selection. raises a flag if the input is not from the menu.
        if 0 < selection < 5:
            if selection == 4:  # Catches the exit selection and terminates the program.
                print(f"\nExiting the program. Good Bye!\n")
                break
            # Catches the selction for the report generator and call the function with the given path.
            elif selection == 1:
                source_folder_path = input(
                    "Please provide the source folder: ")
                report_generator(source_folder_path)
            # Cathces the selction for file renamer and calls the renaming funtion.
            elif selection == 2:
                source_folder_path = input("Please provide the source folder:")
                new_name = input(
                    "Please provide the new name for files to append:")
                file_renamer(source_folder_path, new_name)

            # catches the selection for safe backup and call the fuction to initate the backup.
            elif selection == 3:
                source_folder_path = input(
                    "Please provide the source folder: ")
                destination_folder_path = input(
                    "Please provide the destination folder: ")
                Safe_duplicate(source_folder_path, destination_folder_path)
        else:
            # handels the userinput error if outside of the selction range.
            print(f"\nPlease select a number from the range.\n")
    # Handles the value error for the selection menu if user input is other then a number.
    except ValueError:
        print("\nPlease select a number for the opration.\n")
    # raises an exception and displays the error description to the user.
    except Exception as e:
        print(f"An unexpected error occured: {e}")
