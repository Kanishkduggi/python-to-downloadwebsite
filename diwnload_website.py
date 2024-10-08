import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import shutil

def download_website(url, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    def download_resource(resource_url, folder_name):
        try:
            resource_url = urljoin(url, resource_url)
            resource_response = requests.get(resource_url, stream=True)
            resource_response.raise_for_status()

            resource_path = os.path.join(output_dir, folder_name, os.path.basename(resource_url))
            os.makedirs(os.path.dirname(resource_path), exist_ok=True)

            with open(resource_path, 'wb') as resource_file:
                shutil.copyfileobj(resource_response.raw, resource_file)

            print(f"Downloaded: {resource_url}")
            return os.path.join(folder_name, os.path.basename(resource_url))  # Return local path
        except Exception as e:
            print(f"Failed to download {resource_url}: {e}")
            return None

    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            local_img_path = download_resource(img_url, 'images')
            if local_img_path:
                img['src'] = local_img_path  

    html_filename = os.path.join(output_dir, 'index.html')
    with open(html_filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))  

    print(f"Website downloaded to {output_dir}")

def main():
    url = input("Enter the website URL: ").strip()
    output_dir = input("Enter the output directory path: ").strip()
    print("\nProcessing...")
    download_website(url, output_dir)
if __name__ == "__main__":
    main()