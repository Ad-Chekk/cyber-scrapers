import requests
from bs4 import BeautifulSoup
import sys
import json

def scrape_cybersecurity_news():
    # Fix encoding issue for Windows
    sys.stdout.reconfigure(encoding='utf-8')

    url = "https://timesofindia.indiatimes.com/topic/cyber-security/news"

    # Fetch the page content
    try:
        page_request = requests.get(url)
        page_request.raise_for_status()  # Ensure the request was successful
        data = page_request.content
        soup = BeautifulSoup(data, "html.parser")

        news_list = []  # Store news in JSON format

        # Loop through the articles
        for articletag in soup.find_all('div', {'class': 'fHv_i o58kM'}):
            # Extract title
            title = articletag.get_text(strip=True)

            # Extract date (ensure correct parent scope for the date class)
            date_tag = articletag.find_next_sibling('div', {'class': 'ZxBIG'})
            date = date_tag.get_text(strip=True) if date_tag else "No date provided"

            # Extract description
            description_tag = articletag.find_next('p', {'class': 'oxXSK o58kM'})
            description_span = description_tag.find('span') if description_tag else None
            description = description_span.get_text(strip=True) if description_span else "No description provided"

            # Append to the news list
            news_list.append({
                "title": title,
                "date": date,
                "description": description
            })

            # Limit to the first 10 articles
            if len(news_list) >= 10:
                break

        # Save JSON data to a file
        with open("toi.json", "w", encoding="utf-8") as json_file:
            json.dump(news_list, json_file, ensure_ascii=False, indent=4)

        # Print JSON data
        print(json.dumps(news_list, ensure_ascii=False, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    scrape_cybersecurity_news()