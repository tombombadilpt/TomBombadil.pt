import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote, urljoin

def download_file(url, destination_folder):
    response = requests.get(url, stream=True)
    file_name = os.path.join(destination_folder, unquote(os.path.basename(urlparse(url).path)))

    # Check if the destination directory exists, create it if not
    os.makedirs(destination_folder, exist_ok=True)

    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def download_zip_files(base_url, destination_folder):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        page_url = link['href']

        # Add the base URL prefix if the URL is not complete
        if not page_url.startswith('http'):
            page_url = urljoin(base_url, page_url)

        # Ignore URLs that do not follow the expected pattern
        if not page_url.startswith('https://archive.org/download/retroachievements_collection_v5/Mega%20Drive/'):
            continue

        try:
            page_response = requests.get(page_url)
            page_response.raise_for_status()  # Check if there was any error accessing the page
        except requests.exceptions.RequestException as e:
            print(f"Error accessing page {page_url}: {e}")
            continue

        page_soup = BeautifulSoup(page_response.text, 'html.parser')

        # Assuming the zip file links are direct download links on the page
        for zip_link in page_soup.find_all('a', href=True):
            zip_url = zip_link['href']

            # Add the base URL prefix if the zip file URL is not complete
            if not zip_url.startswith('http'):
                zip_url = urljoin(page_url, zip_url)

            if zip_url.lower().endswith('.zip'):
                try:
                    download_file(zip_url, destination_folder)
                except Exception as e:
                    print(f"Error downloading file {zip_url}: {e}")

if __name__ == "__main__":
    # Display a message indicating the script creator
    print("This script was created by JonPQ (https://www.reddit.com/user/JonPQ)")

    # Ask the user for the necessary information
    base_url = input("Enter the URL of the main website: ")
    destination_folder = input("Enter the local path where the files should be downloaded: ")

    download_zip_files(base_url, destination_folder)
