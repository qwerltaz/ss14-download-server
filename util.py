"""Specific info retrieval functions."""

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_downloads_dir() -> str:
    """Returns the path to the user's downloads folder."""
    home = str(Path.home())
    downloads_path = os.path.join(home, 'Downloads')

    if os.path.exists(downloads_path):
        downloads_folder = downloads_path
    else:
        raise OSError("Downloads folder not found. Unsupported operating system?")

    return downloads_folder


def get_ss14_version() -> tuple[str, str]:
    """Get latest version number of ss14 from the website."""
    version_url = "https://wizards.cdn.spacestation14.com/fork/wizards"

    response = requests.get(version_url, timeout=20)

    if response.status_code != 200:
        raise ConnectionError(
            f"Could not connect to the versioning website. Status code: {response.status_code}"
        )

    soup = BeautifulSoup(response.text, 'html.parser')
    span = soup.find('span', class_='versionNumber')

    # Extract the date string
    date_tag = soup.find('time')
    date_string = date_tag.text.strip() if date_tag else "unknown date"

    if span:
        value = span.text
        return value, date_string
    else:
        raise KeyError("Could not find ss14 server version number.")
