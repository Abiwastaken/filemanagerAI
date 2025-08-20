import os 
import csv
from datetime import datetime

def get_file_info(file_path):
    """
    Returns a dictionary of metadata for a given file.
    
    Args:
        file_path (str): The full path to the file.
        
    Returns:
        dict: A dictionary containing 'size', 'last_modified', and 'file_type'.
    """
    file_info = {}
    try:
        file_info['size'] = os.path.getsize(file_path)
        mod_timestamp = os.path.getmtime(file_path)
        create_timestamp = os.path.getctime(file_path)
        file_info['creation_date'] = datetime.fromtimestamp(create_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        file_info['last_modified'] = datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        file_info['file_type'] = os.path.splitext(file_path)[1].lower()
    except (OSError, ValueError):
        file_info['size'] = -1
        file_info['last_modified'] = 'N/A'
        file_info['file_type'] = 'N/A'
        file_info['creation_date'] = 'N/A'
    return file_info
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
                    info = get_file_info(full_path)
                    csv_writer.writerow([full_path, 'File', info['size'], info['creation_date'], info['last_modified'],  info['file_type']])
                    existing_files.add(full_path)
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                if full_path not in existing_files:
                    csv_writer.writerow([full_path, 'Folder', '', '', '', ''])
                    existing_files.add(full_path)
            
            for filename in filenames:
                if not filename.startswith('.'):
                    full_path = os.path.join(dirpath, filename)
                    if full_path not in existing_files:
                        info_file = get_file_info(full_path)
                        csv_writer.writerow([full_path, 'File', info_file['size'], info_file['creation_date'], info_file['last_modified'], info_file['file_type']])
                        existing_files.add(full_path)
