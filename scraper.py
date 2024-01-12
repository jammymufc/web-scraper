import requests
from bs4 import BeautifulSoup
import re

def extract_statement(soup):
    # Find the statement text
    statement_tag = soup.find('div', class_='m-statement__quote')
    return statement_tag.get_text(strip=True) if statement_tag else "No statement found."

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

            # Find the <a> tag with the class 'm-statement__name'
            name_tag = soup.find('a', class_='m-statement__name')

            # Check if the name tag is found
            if name_tag:
                # Extract the name text
                name = name_tag.get_text(strip=True)

                # Extract the 'href' attribute value
                href_value = name_tag.get('href')

                # Extract the statement using the separate method
                statement = extract_statement(soup)

                return image_tag, href_value, name, statement
            else:
                print("No matching <a> tag found with the class 'm-statement__name'.")
        else:
            print("No matching parent element found on the page.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example usage:
url_to_scrape = "https://www.politifact.com/factchecks/2024/jan/11/nikki-haley/the-missing-facts-from-nikki-haleys-claim-about-bo/"
result = extract_information(url_to_scrape)

if result:
    image_tag, href_value, name, statement = result
    print(f"Extracted image alt: {image_tag}")
    print(f"Extracted href value: {href_value}")
    print(f"Extracted name: {name}")
    print(f"Extracted statement: {statement}")
else:
    print("Failed to extract information.")
