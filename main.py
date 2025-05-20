"""Download new version and update ss14 server folder."""

import json
import os
import shutil
import zipfile
import subprocess

import requests

import cvar
import util


def main() -> None:
    """Download new version and update ss14 server folder."""

    downloads_dir = cvar.DOWNLOADS_OVERRIDE
    if os.path.isdir(downloads_dir):
        print(f"Downloads dir: {downloads_dir}")
    else:
        downloads_dir = util.get_downloads_dir()
        print(f"Downloads override dir not found, using default: '{downloads_dir}'")

    version, version_date = util.get_ss14_version()

    url = f"https://wizards.cdn.spacestation14.com/fork/wizards/version/{version}/file/SS14.Server_win-x64.zip"

    print(f"Downloading version {version}\nfrom {version_date}")
    response = requests.get(url, stream=True, timeout=60)

    if response.status_code != 200:
        print(f"Error occurred while downloading the server: {response.status_code}")
        return

    zip_path = os.path.join(downloads_dir, "SS14.Server_win-x64.zip")

    with open(zip_path, "wb") as server_zip:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, server_zip)

    print("Unpacking downloaded server...")

    server_path = zip_path.replace(".zip", "")

    if os.path.isdir(server_path):
        shutil.rmtree(server_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(server_path)

    os.remove(zip_path)

    print("Downloaded to: " + server_path)
    
    # Start server and game.
    server_exe_name = "Robust.Server.exe"
    subprocess.run(f'start "Robust server" /d "{server_path}" {server_exe_name}', shell=True)
    subprocess.run('start "" steam://rungameid/1482520', shell=True)


if __name__ == '__main__':
    main()
