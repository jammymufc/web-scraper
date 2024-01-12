import requests
from bs4 import BeautifulSoup
import re

def extract_information(url):
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

            # Traverse through the HTML structure to find the <a> tag with the specified title
            a_tag = None
            for li_tag in soup.find_all('li', class_='m-list__item'):
                a_tag_candidate = li_tag.find('a', class_='c-tag')
                if a_tag_candidate and 'title' in a_tag_candidate.attrs and 'Nikki Haley' in a_tag_candidate['title']:
                    a_tag = a_tag_candidate
                    break

            # Check if the <a> tag is found
            if a_tag:
                # Extract the 'href' attribute value
                href_value = a_tag.get('href')

                # Extract the name from the URL using regular expressions
                match = re.search(r'/personalities/([^/]+)/?$', href_value)
                if match:
                    name = match.group(1)
                    return image_tag, href_value, name
                else:
                    print("Failed to extract name from URL.")
            else:
                print("No matching <a> tag found with the specified title.")
        else:
            print("No matching parent element found on the page.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example usage:
url_to_scrape = "https://www.politifact.com/factchecks/2024/jan/11/nikki-haley/the-missing-facts-from-nikki-haleys-claim-about-bo/"  # Replace with your actual URL
result = extract_information(url_to_scrape)

if result:
    image_tag, href_value, name = result
    print(f"Extracted image tag: {image_tag}")
    print(f"Extracted href value: {href_value}")
    print(f"Extracted name: {name}")
else:
    print("Failed to extract information.")
