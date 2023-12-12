import os 
current_directory = os.getcwd()

from pathlib import Path

def list_files_and_directories(directory):
    path = Path(directory)
    for entry in path.iterdir():
        print(entry.name)
file_path=current_directory+"/AppAlch/.env"
list_files_and_directories(current_directory+"/AppAlch")

import os

def is_valid_file_path(file_path):
    return os.path.isfile(file_path)



if is_valid_file_path(file_path):
    print(f"The path '{file_path}' is a valid file.")
else:
    print(f"The path '{file_path}' is not a valid file.")