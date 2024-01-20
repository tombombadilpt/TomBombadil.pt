import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote, urljoin
import keyboard

def save_paths_to_file(urls, destination_folder):
    file_path = os.path.join(destination_folder, 'paths.txt')
    with open(file_path, 'w') as file:
        file.write('\n'.join(urls))

def download_zip_files(base_url, destination_folder):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    zip_urls = []

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
                zip_filename = os.path.basename(urlparse(zip_url).path)
                simplified_name = unquote(zip_filename)
                zip_urls.append(zip_url)
                print(f"Last ZIP file found: {simplified_name}")

                # Check for key presses (s for stop, p for pause)
                if keyboard.is_pressed('s'):
                    print("Scrapping stopped by user.")
                    save_paths_to_file(zip_urls, destination_folder)
                    return
                elif keyboard.is_pressed('p'):
                    print("Scrapping paused. Press 'p' to resume.")
                    while not keyboard.is_pressed('p'):
                        pass  # Wait for 'p' to be pressed again

    save_paths_to_file(zip_urls, destination_folder)

if __name__ == "__main__":
    # Display information about the script creator and GitHub repository
    print("This script was created by JonPQ (https://www.reddit.com/user/JonPQ)")
    print("GitHub Repository: https://github.com/tombombadilpt/TomBombadil.pt/blob/main/lalala.py")

    # Explain pausing/resuming functionality to the user
    print("You can pause the scraping by pressing 'p'. To resume, press 'p' again.")
    print("You can stop the scraping at any time by pressing 's'.")

    # Ask the user for the necessary information
    base_url = input("Enter the URL of the main website: ")
    destination_folder = input("Enter the local path where the paths.txt file should be created: ")

    download_zip_files(base_url, destination_folder)
