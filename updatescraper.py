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
        
        # Extract context information
        context_divs = soup.select('div.m-statement__desc')
        contexts = [context.get_text(strip=True) for context in context_divs]

        for quote_a, context in zip(quote_as, contexts):
            # Extract statement text
            statement_text = quote_a.get_text(strip=True)

            # Construct the full URL of the statement page
            statement_url = urljoin(person_url, quote_a['href'])

            statement_details = {
                'text': statement_text,
                'url': statement_url,
                'context': context
            }

            statements.append(statement_details)
            print(f"Scraped Statement: {statement_details}")

        # Extract scorecard information
        scorecard_items = soup.select('div.m-scorecard__item')
        scorecards = []

        for scorecard_item in scorecard_items:
            scorecard_title = scorecard_item.select_one('h4.m-scorecard__title').get_text(strip=True)
            scorecard_value = scorecard_item.find('div', {'class': 'm-scorecard__bar'}).get('data-scorecard-bar', '')
            scorecard_checks = scorecard_item.select_one('p.m-scorecard__checks a').get_text(strip=True)
            scorecard_url = scorecard_item.select_one('p.m-scorecard__checks a')['href']

            scorecard_details = {
                'title': scorecard_title,
                'value': scorecard_value,
                'checks': scorecard_checks,
                'url': urljoin(person_url, scorecard_url)
            }

            scorecards.append(scorecard_details)
            print(f"Scraped Scorecard: {scorecard_details}")

        return {'statements': statements, 'scorecards': scorecards}

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {person_url}: {e}")
        return None

def load_existing_data(file_path):
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
        return existing_data
    except FileNotFoundError:
        return {'people': {}}

def save_data(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def scrape_and_update_data(person_url, existing_data):
    # Scraping logic here to get the latest data
    new_data = scrape_person_statements(person_url)

    # Check for changes and update existing data
    if 'statements' in new_data:
        person_name = new_data['name']
        existing_data['people'][person_name] = existing_data['people'].get(person_name, {})
        existing_statements = existing_data['people'][person_name].get('statements', [])
        new_statements = new_data['statements']

        # Compare the new statements with existing ones
        for new_statement in new_statements:
            if new_statement not in existing_statements:
                existing_statements.append(new_statement)

        existing_data['people'][person_name]['statements'] = existing_statements

        # Save the updated data
        save_data('data.json', existing_data)

if __name__ == "__main__":
    test_person_url = "https://www.politifact.com/personalities/eric-adams/"
    existing_data = load_existing_data('new_people_details.json')

    # Scrape and update data
    scrape_and_update_data(test_person_url, existing_data)
