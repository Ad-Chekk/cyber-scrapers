import requests
from bs4 import BeautifulSoup
import sys
import json
import os

def scrape_indianexpress_cybersecurity():
    # Fix encoding issue for Windows
    sys.stdout.reconfigure(encoding='utf-8')

    url = "https://indianexpress.com/about/cyber-security/"
    
    # Fetch the page content
    try:
        page_request = requests.get(url)
        page_request.raise_for_status()  # Ensure the request was successful
        data = page_request.content
        soup = BeautifulSoup(data, "html.parser")

        news_list = []  # Store news in JSON format

        # Load existing data if the file exists
        if os.path.exists("ind_exp.json"):
            with open("ind_exp.json", "r", encoding="utf-8") as json_file:
                try:
                    news_list = json.load(json_file)
                except json.JSONDecodeError:
                    news_list = []  # Start fresh if the file is corrupted or empty

        # Loop through the articles
        for divtag in soup.find_all('div', {'class': 'img-context'}):
            # Extract title
            h3_tag = divtag.find('h3', {'class': ''})
            if not h3_tag:
                continue

            a_tag = h3_tag.find('a')
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            url = a_tag['href']

            # Extract date and description
            p_tags = divtag.find_all('p')
            date = p_tags[0].get_text(strip=True) if len(p_tags) > 0 else "No date provided"
            description = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "No description provided"

            # Append to the news list
            news_list.append({
                "title": title,
                "url": url,
                "date": date,
                "description": description
            })

            # Limit to the first 10 articles
            if len(news_list) >= 10:
                break

        # Save JSON data to a file
        with open("ind_exp.json", "w", encoding="utf-8") as json_file:
            json.dump(news_list, json_file, ensure_ascii=False, indent=4)

        # Print JSON data
        print(json.dumps(news_list, ensure_ascii=False, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    scrape_indianexpress_cybersecurity()
