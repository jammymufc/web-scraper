import requests
from bs4 import BeautifulSoup

def extract_statement(soup):
    # Find the statement text
    statement_tag = soup.find('div', class_='m-statement__quote')
    return statement_tag.get_text(strip=True) if statement_tag else "No statement found."

def extract_subject(soup):
    # Find the meta tag with name="keywords"
    subject_tag = soup.find('meta', {'name': 'keywords'})

    # Extract the content attribute value
    subject_content = subject_tag.get('content') if subject_tag else "No subjects found."
    
    return subject_content

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
            speaker_tag = soup.find('a', class_='m-statement__name')

            # Check if the name tag is found
            if speaker_tag:
                # Extract the name text
                speaker = speaker_tag.get_text(strip=True)

                # Extract the 'href' attribute value
                href_value = speaker_tag.get('href')

                # Extract the statement using the separate method
                statement = extract_statement(soup)

                # Extract the keywords using the separate method
                subjects = extract_subject(soup)

                return image_tag, href_value, speaker, statement, subjects
            else:
                print("No matching <a> tag found with the class 'm-statement__name'.")
        else:
            print("No matching parent element found on the page.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

# Example usage:
url_to_scrape = "https://www.politifact.com/factchecks/2024/jan/12/glenn-grothman/grothman-falsely-claims-birthright-citizenship-doe/"
result = extract_information(url_to_scrape)

if result:
    image_tag, href_value, speaker, statement, subjects = result
    print(f"Extracted image alt: {image_tag}")
    print(f"Extracted href value: {href_value}")
    print(f"Extracted name: {speaker}")
    print(f"Extracted statement: {statement}")
    print(f"Extracted subject/s: {subjects}")
else:
    print("Failed to extract information.")
