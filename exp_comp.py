import requests
from bs4 import BeautifulSoup
import json

def scrape_expresscomputer_cybersecurity():
    url = "https://www.expresscomputer.in/tag/cybersecurity/"

    try:
        # Fetch the page content
        page_request = requests.get(url)
        page_request.raise_for_status()  # Ensure the request was successful
        data = page_request.content
        soup = BeautifulSoup(data, "html.parser")

        results = []
        print("Latest Cybersecurity News from Express Computer:")

        # Loop through the articles
        for post in soup.find_all('div', {'class': 'post-content'}):
            # Extract title and URL
            a_tag = post.find('a', {'class': 'post-url post-title'})
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            url = a_tag['href']

            # Extract incident date
            time_tag = post.find('span', {'class': 'time'}).find('time', {'class': 'post-published updated'})
            incident_date = time_tag.get_text(strip=True) if time_tag else "No date provided"

            # Extract description (summary)
            description_tag = post.find('div', {'class': 'post-summary'})
            description = description_tag.get_text(strip=True) if description_tag else "No description provided"

            # Save the data in the desired format
            result = {
                "title": title,
                "description": description,
                "url": url,
                "incident_date": incident_date
            }
            results.append(result)

            # Print the details
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # Save results to a JSON variable
        scraped_data_json = json.dumps(results, indent=2, ensure_ascii=False)

        return scraped_data_json

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

if __name__ == "__main__":
    json_data = scrape_expresscomputer_cybersecurity()
    if json_data:
        print("\nScraped Data in JSON Format:")
        print(json_data)
