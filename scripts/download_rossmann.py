import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_rossmann_dataset():
    dataset = "rossmann-store-sales"
    competition = "rossmann-store-sales"
    output_dir = "/data/raw_data/rossmann-store-sales/"
    os.makedirs(output_dir, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    print("Downloading dataset...")
    api.competition_download_files(competition, path=output_dir)

    zip_path = os.path.join(output_dir, f"{competition}.zip")
    if os.path.exists(zip_path):
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        os.remove(zip_path)
        print(f"Files extracted to: {output_dir}")
    else:
        print("Download failed or zip file not found.")

if __name__ == "__main__":
    download_rossmann_dataset()
