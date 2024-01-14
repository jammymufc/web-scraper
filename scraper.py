import requests
from bs4 import BeautifulSoup
import json


def extract_context(soup):
    # Find the context element
    context_tag = soup.find('div', class_='m-statement__desc')

    # Extract the context text
    context_text = context_tag.get_text(strip=True) if context_tag else "No context found."

    return context_text

def extract_states_from_text(article_text, state_editions):
    # List of US states
    us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
                 "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
                 "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
                 "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                 "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                 "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

    # Extract state names from the text
    text_states = [state for state in us_states if state.lower() in article_text.lower()]

    # Remove states from state editions
    for edition in state_editions:
        state_link = edition.find('a')
        if state_link:
            state_name = state_link.get_text(strip=True)
            if state_name in text_states:
                text_states.remove(state_name)

    return text_states

def count_occurrences(text, keywords):
    # Count occurrences of each keyword in the text
    occurrences = {keyword: text.lower().count(keyword) for keyword in keywords}
    return occurrences

def determine_party_affiliation(occurrences):
    # Determine party affiliation based on occurrences
    if occurrences['democrat'] > occurrences['republican']:
        return 'party_affiliation: democrat'
    elif occurrences['republican'] > occurrences['democrat']:
        return 'party_affiliation: republican'
    else:
        return 'party_affiliation: unknown'

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

        # Find the main content area (you may need to adjust this selector)
        main_content = soup.find('main')

        # Check if the main content is found
        if main_content:
            # Find the parent element of the <img> tag within the main content
            parent_element = main_content.find('div', class_='m-statement__meter')

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

                    # Extract state information
                    article_text = ' '.join([p.get_text(strip=True) for p in main_content.find_all('p')])

                    # Extract state editions
                    state_editions = main_content.select('div.m-togglist__panel a')

                    text_states = extract_states_from_text(article_text, state_editions)

                    # Count occurrences of 'democrat' and 'republican'
                    keywords = ['democrat', 'republican']
                    occurrences = count_occurrences(article_text, keywords)

                    # Determine party affiliation
                    party_affiliation = determine_party_affiliation(occurrences)
                    
                    # Extract context information using the new function
                    context = extract_context(soup)

                    return image_tag, href_value, speaker, statement, subjects, text_states, occurrences, party_affiliation, context
                else:
                    print("No matching <a> tag found with the class 'm-statement__name'.")
            else:
                print("No matching parent element found within the main content.")
        else:
            print("No main content found on the page.")
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")


# Load the JSON data
with open('people_details.json', 'r') as json_file:
    people_details = json.load(json_file)

# Example usage:
url_to_scrape = "https://www.politifact.com/factchecks/2024/jan/12/donald-trump/trumps-claim-that-millions-of-immigrants-are-signi/"
result = extract_information(url_to_scrape)

if result:
    image_tag, href_value, speaker, statement, subjects, text_states, occurrences, _, context = result

    # Find the speaker in the JSON data
    speaker_info = None
    for person in people_details:
        if person["name"] == speaker:
            speaker_info = person
            break

    if speaker_info:
        party_affiliation = speaker_info.get('party_affiliation', 'Party affiliation not found.')
        print(f"Extracted label: {image_tag}")
        print(f"Extracted href value: {href_value}")
        print(f"Extracted speaker: {speaker}")
        print(f"Extracted statement: {statement}")
        print(f"Extracted subject/s: {subjects}")
        print(f"Extracted states: {text_states}")
        print(f"Party Affiliation: {party_affiliation}")
        print(f"Extracted context: {context}")
    else:
        print(f"Speaker '{speaker}' not found in the JSON data.")
else:
    print("Failed to extract information.")
