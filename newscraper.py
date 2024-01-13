import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def scrape_people_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        print(f"Request Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> tags with class 'c-chyron__value' that are within an <a> tag
        name_as = soup.select('div.c-chyron__value a')

        # Find all <div> tags with class 'c-chyron__subline'
        party_affiliation_divs = soup.select('div.c-chyron__subline')

        people_details = []

        for name_a, party_affiliation_div in zip(name_as, party_affiliation_divs):
            # Extract name
            name = name_a.get_text(strip=True)

            # Extract party affiliation
            party_affiliation = party_affiliation_div.get_text(strip=True) if party_affiliation_div else "None"

            # Construct the person's URL
            person_url = urljoin(url, name_a['href'])

            # Scrape the statements from the person's page
            statements = scrape_person_statements(person_url)

            person_details = {
                'name': name,
                'party_affiliation': party_affiliation,
                'statements': statements
            }

            people_details.append(person_details)
            print(f"Scraped Details: {person_details}")

        return people_details

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def scrape_person_statements(person_url):
    try:
        response = requests.get(person_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        print(f"Request Status Code for {person_url}: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        statements = []

        # Find all <a> tags within <div> tags with class 'm-statement__quote'
        quote_as = soup.select('div.m-statement__quote a')

        for quote_a in quote_as:
            # Extract statement text
            statement_text = quote_a.get_text(strip=True)

            # Construct the full URL of the statement page
            statement_url = urljoin(person_url, quote_a['href'])

            statement_details = {
                'text': statement_text,
                'url': statement_url
            }

            statements.append(statement_details)
            print(f"Scraped Statement: {statement_details}")

        return statements

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {person_url}: {e}")
        return None

if __name__ == "__main__":
    url_to_scrape = "https://www.politifact.com/personalities/"
    output_file_path = "new_people_details.json"

    details = scrape_people_details(url_to_scrape)
    if details:
        with open(output_file_path, 'w') as json_file:
            json.dump(details, json_file, indent=2)
        print(f"Details exported to {output_file_path}")
    else:
        print("Failed to scrape details.")
