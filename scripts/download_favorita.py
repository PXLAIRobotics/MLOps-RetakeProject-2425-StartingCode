import os
import zipfile
import shutil
import py7zr
from kaggle.api.kaggle_api_extended import KaggleApi

def prompt_user_action(path):
    print(f"Directory '{path}' already exists and contains files.")
    while True:
        choice = input("Do you want to overwrite existing files? (y/n): ").lower()
        if choice in ['y', 'yes']:
            return "overwrite"
        elif choice in ['n', 'no']:
            return "skip"
        else:
            print("Please enter 'y' or 'n'.")

def clear_directory(dir_path):
    for f in os.listdir(dir_path):
        file_path = os.path.join(dir_path, f)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def extract_7z_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".7z"):
            archive_path = os.path.join(directory, file)
            print(f"Extracting {file}...")
            with py7zr.SevenZipFile(archive_path, mode='r') as archive:
                archive.extractall(path=directory)
            os.remove(archive_path)
            print(f"Extracted and removed: {file}")

def download_favorita_dataset():
    competition = "favorita-grocery-sales-forecasting"
    base_dir = "/data/raw_data"
    output_dir = os.path.join(base_dir, competition)
    os.makedirs(output_dir, exist_ok=True)

    # Check if directory contains files
    if os.listdir(output_dir):
        action = prompt_user_action(output_dir)
        if action == "skip":
            print("Skipping download. Existing files kept.")
            return
        elif action == "overwrite":
            print("Clearing existing files...")
            clear_directory(output_dir)

    api = KaggleApi()
    api.authenticate()

    print(f"Downloading dataset '{competition}'...")
    api.competition_download_files(competition, path=output_dir)

    zip_path = os.path.join(output_dir, f"{competition}.zip")
    if os.path.exists(zip_path):
        print("Extracting zip file...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        os.remove(zip_path)
        print(f"ZIP extracted and removed.")
    else:
        print("Download failed or zip file not found.")
        return

    # Now extract all .7z files inside the folder
    extract_7z_files(output_dir)

    print(f"All data is ready in: {output_dir}")

if __name__ == "__main__":
    download_favorita_dataset()
