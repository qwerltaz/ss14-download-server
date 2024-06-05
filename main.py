"""Download new version and update ss14 server folder."""

import json
import os
import shutil
import zipfile

import requests

import util


def main() -> None:
    """Download new version and update ss14 server folder."""

    with open("config.json", "r", encoding='utf-8') as file:
        config = json.load(file)

    downloads_dir = config["downloads_override"]
    if os.path.isdir(downloads_dir):
        print(f"Downloads dir: {downloads_dir}")
    else:
        downloads_dir = util.get_downloads_dir()
        print(f"Config downloads override dir not found, using default: '{downloads_dir}'")

    version, version_date = util.get_ss14_version()

    url = f"https://cdn.centcomm.spacestation14.com/builds/wizards/builds/{version}/SS14.Server_win-x64.zip"

    print(f"Downloading version {version}\nfrom {version_date}")
    response = requests.get(url, stream=True, timeout=20)

    if response.status_code != 200:
        print(f"Error occurred while downloading the server: {response.status_code}")
        return

    save_path = os.path.join(downloads_dir, "SS14.Server_win-x64.zip")

    # Open the file in binary mode and write the contents from the response
    with open(save_path, "wb") as server_zip:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, server_zip)

    print("Unpacking downloaded server...")

    # Extract the contents of the zip file
    extract_path = save_path.replace(".zip", "")

    if os.path.isdir(extract_path):
        shutil.rmtree(extract_path)

    with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Delete the zip file
    os.remove(save_path)

    print("Downloaded to: " + extract_path)


main()
