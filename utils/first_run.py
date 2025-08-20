import os
import csv
from datetime import datetime
from create_file_list import create_file_list_csv




def cleanup_csv(file_path):
    if os.path.exists(file_path):
        confirm = input(f" Are you sure you want to erase '{file_path}' and start fresh? (y/n): ").strip().lower()
        if confirm == "y":
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['File Path', 'Type', 'Size (bytes)','Creation date', 'Last Modified', 'File Type'])
            print(f"Successfully cleaned up '{file_path}'.")
            return True
        else:
            print("Cleanup aborted. File was not modified.")
            return False
    else:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['File Path', 'Type', 'Size (bytes)', 'Creation date', 'Last Modified', 'File Type'])
        print(f"Created new CSV '{file_path}' with header.")
        return True


TEST_FOLDER = "/Users/abi/Desktop/desktop 2.0/foldermanagerai/test folder"
# This ensures the folder is created where the script is run.
current_directory = os.getcwd()

# Step 2: Define the path for the new 'data' folder.
data_folder_path = os.path.join(current_directory, "data")

# Step 3: Create the 'data' folder if it doesn't already exist.
# exist_ok=True prevents an error if the folder is already there.
os.makedirs(data_folder_path, exist_ok=True)

# Step 4: Define the final path for the CSV file inside the new folder.
OUTPUT_FILE = os.path.join(data_folder_path, "file_list.csv")


 
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