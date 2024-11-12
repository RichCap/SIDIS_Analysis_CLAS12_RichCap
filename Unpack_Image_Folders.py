#!/usr/bin/env python3

import os
import argparse
import shutil
from MyCommonAnalysisFunction_richcap import *

def unpack_files(directory, delete_empty_dirs=False):
    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory, topdown=False):  # Use topdown=False to visit subdirectories before their parents
        # Filter for PNG and text files
        files_to_move = [file for file in files if(     file.lower().endswith('.png') or file.lower().endswith('.txt'))]
        other_files   = [file for file in files if(not (file.lower().endswith('.png') or file.lower().endswith('.txt')))]

        if(files_to_move):
            print(f"\n{color.BOLD}Found {color.UNDERLINE}{len(files_to_move)}{color.END_B} file(s) to move in directory: {color.BLUE}{root}{color.END}")
            user_response = input("Type 'yes' to move files, 'no' to skip, or 'print' to list files: ").strip().lower()

            if(user_response == 'print'):
                # List all files that would be moved
                for file in files_to_move:
                    print(f"{color.BOLD}Will move: {color.BGREEN}{os.path.join(root, file)}{color.END}")
                # Ask for user approval again, excluding the 'print' option
                user_response = input("Type 'yes' to move files or 'no' to skip: ").strip().lower()

            if(user_response in ['yes', 'y', 'Yes', 'Y', '']):
                for file in files_to_move:
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(os.getcwd(), file)

                    # Check if the file already exists in the destination
                    if(os.path.exists(destination_path)):
                        print(f"\n{color.Error}File {color.UNDERLINE}{file}{color.END}{color.Error} already exists in the destination. Skipping...{color.END}\n")
                        continue

                    # Move the file
                    shutil.move(source_path, destination_path)
                    print(f"{color.BBLUE}Moved: {color.BGREEN}{file}{color.END}")
            elif(user_response in ['no', 'n', 'No', 'N']):
                print(f"{color.RED}Skipping files in directory: {color.UNDERLINE}{color.BOLD}{root}{color.END}")
            else:
                print(f"\n{color.Error}Invalid input. Skipping files...{color.END}\n")

        # If there are other non-PNG and non-text files, list them as a note
        if(other_files):
            print(f"\n{color.BOLD}Note: Found {color.UNDERLINE}{len(other_files)}{color.END_B} non-PNG and non-text file(s) in directory: {color.BBLUE}{root}{color.END}")
            for file in other_files:
                print(f"Non-PNG or non-text file: {color.BOLD}{os.path.join(root, file)}{color.END}")

        # Check if the directory is empty and delete it if requested
        if(delete_empty_dirs and not os.listdir(root)):  # Check if the directory is empty
            user_response = input(f"\nDirectory {color.BOLD}{root}{color.END} is empty.\n\tType 'yes' to delete it or 'no' to keep it: ").strip().lower()
            if(user_response in ['yes', 'y', 'Yes', 'Y', '']):
                try:
                    os.rmdir(root)  # Remove the empty directory
                    print(f"{color.YELLOW}Deleted empty directory: {color.Error}{color.UNDERLINE}{root}{color.END}")
                except Exception as e:
                    print(f"{color.Error}Failed to delete directory {root}: {color.END_R}{e}{color.END}")
            else:
                print(f"Kept the empty directory: {root}")

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Unpack all PNG and text files from subdirectories into the current directory and list other files.")
    parser.add_argument("directory", help="The main directory to unpack files from")
    parser.add_argument("-rm", "-d", "-delete", "--delete-empty-dirs", action="store_true", help="Delete empty directories after moving files")
    args = parser.parse_args()

    print("\n")

    # Check if the directory exists
    if((not os.path.exists(args.directory)) or (not os.path.isdir(args.directory))):
        print(f"{color.Error}Error: The specified directory {color.UNDERLINE}{args.directory}{color.END}{color.Error} does not exist or is not a valid directory.{color.END}")
    else:
        # Ask for user approval before running
        user_response = input(f"Do you want to run the script on the directory {color.UNDERLINE}{args.directory}{color.END}? Type 'yes' to continue or 'no' to exit: ").strip().lower()
        if(user_response in ['yes', 'y', 'Yes', 'Y']):
            unpack_files(args.directory, delete_empty_dirs=args.delete_empty_dirs)
        else:
            print(f"{color.RED}Operation cancelled by the user.{color.END}")

    print("\nDone\n")
