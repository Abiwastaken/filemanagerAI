import os
import csv
from datetime import datetime
import extract_info_from_files
def create_file_list_csv(root_folder, output_csv):
    
    existing_files = set()
    # 1. Read existing file paths into a set for fast lookup
    try:
        with open(output_csv, 'r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            # Check if the file has content before trying to skip the header
            if os.path.getsize(output_csv) > 0:
                next(csv_reader)
            for row in csv_reader:
                if row:
                    existing_files.add(row[0])
    except (IOError, UnicodeDecodeError, csv.Error) as e:
        print(f"Error reading existing CSV: {e}. Starting with a new file.")
        existing_files.clear()

    # 2. Append new files to the CSV
    with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header only if the file is new
        if os.path.getsize(output_csv) == 0:
            csv_writer.writerow(['File Path', 'Type'])

        for dirpath, dirnames, filenames in os.walk(root_folder):
            # --- Filtering of invisible and .apps
             # Identify app packages to be counted as files
            app_packages = [d for d in dirnames if d.endswith('.app')]
             # Remove app packages and hidden files from dirnames to stop the walk
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and not d.endswith('.app')]

            # --- Writing Files and Folders to CSV ---
            # Write a row for each app package (treated as a single file)
            for app_name in app_packages:
                full_path = os.path.join(dirpath, app_name)
                if full_path not in existing_files:
                    # info = get_file_info(full_path)
                    csv_writer.writerow([full_path, 'File'])
                    existing_files.add(full_path)
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                if full_path not in existing_files:
                    csv_writer.writerow([full_path, 'Folder'])
                    existing_files.add(full_path)
            
            for filename in filenames:
                if not filename.startswith('.'):
                    full_path = os.path.join(dirpath, filename)
                    if full_path not in existing_files:
                        csv_writer.writerow([full_path, 'File'])
                        existing_files.add(full_path)




def cleanup_csv(file_path):
    if os.path.exists(file_path):
        confirm = input(f" Are you sure you want to erase '{file_path}' and start fresh? (y/n): ").strip().lower()
        if confirm == "y":
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['File Path', 'Type', 'Size (bytes)', 'Last Modified', 'File Type'])
            print(f"Successfully cleaned up '{file_path}'.")
            return True
        else:
            print("Cleanup aborted. File was not modified.")
            return False
    else:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['File Path', 'Type', 'Size (bytes)', 'Last Modified', 'File Type'])
        print(f"Created new CSV '{file_path}' with header.")
        return True


TEST_FOLDER = "/Users/abi/Desktop/desktop 2.0/foldermanagerai/test folder"
OUTPUT_FILE = "file_list.csv"
 
def initial_check_initiator(manage_folder, csv_file):
    if os.path.exists(manage_folder):
        if cleanup_csv(csv_file):  # only continue if cleanup succeeded
            create_file_list_csv(manage_folder, csv_file)
            print(f"Successfully created '{csv_file}' with a list of all files and folders.")
        else:
            print("Process halted due to cleanup cancellation.")
    else:
        print(f"Error: The folder '{manage_folder}' does not exist.")






initial_check_initiator(TEST_FOLDER,OUTPUT_FILE)