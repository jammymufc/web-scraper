import requests
from bs4 import BeautifulSoup

def extract_image_tag(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the parent element of the <img> tag
        parent_element = soup.find('div', class_='m-statement__meter')

        # Check if the parent element is found
        if parent_element:
            # Find the text associated with the image
            image_tag = parent_element.find('img', class_='c-image__original').get('alt')
            return image_tag
        else:
            print("No matching parent element found on the page.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example usage:
url_to_scrape = "https://www.politifact.com/factchecks/2024/jan/12/glenn-grothman/grothman-falsely-claims-birthright-citizenship-doe/"  # Replace with your actual URL
image_tag = extract_image_tag(url_to_scrape)

if image_tag:
    print(f"Extracted image tag: {image_tag}")
else:
    print("Failed to extract image tag.")
