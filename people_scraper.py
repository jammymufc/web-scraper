import requests
from bs4 import BeautifulSoup
import json

def scrape_people_names(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        print(f"Request Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with class 'c-chyron__value' within <div> tags with class 'c-chyron'
        chyron_values = soup.select('div.c-chyron__value a')

        people_names = []

        for chyron_value in chyron_values:
            name = chyron_value.get_text(strip=True)
            people_names.append(name)
            print(f"Scraped Name: {name}")

        return people_names

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    url_to_scrape = "https://www.politifact.com/personalities/"
    output_file_path = "people_names.json"

    names = scrape_people_names(url_to_scrape)
    if names:
        with open(output_file_path, 'w') as json_file:
            json.dump(names, json_file, indent=2)
        print(f"Names exported to {output_file_path}")
    else:
        print("Failed to scrape names.")
