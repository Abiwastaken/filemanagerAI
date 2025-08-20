import os
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
        file_info['last_modified'] = datetime.fromtimestamp(mod_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        file_info['file_type'] = os.path.splitext(file_path)[1].lower()
    except (OSError, ValueError):
        file_info['size'] = -1
        file_info['last_modified'] = 'N/A'
        file_info['file_type'] = 'N/A'
    return file_info