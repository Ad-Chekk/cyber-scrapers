import requests
from bs4 import BeautifulSoup
import json

def extract_all_data(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return {"error": f"Failed to fetch page: {response.status_code}"}

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract metadata
        metadata = {
            "title": soup.title.string if soup.title else "No Title",
            "description": "",
            "keywords": ""
        }
        meta_tags = soup.find_all("meta")
        for tag in meta_tags:
            if "name" in tag.attrs:
                if tag.attrs["name"].lower() == "description":
                    metadata["description"] = tag.attrs.get("content", "")
                if tag.attrs["name"].lower() == "keywords":
                    metadata["keywords"] = tag.attrs.get("content", "")

        # Extract all visible text
        visible_text = ' '.join([element.get_text(strip=True) for element in soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a'])])

        # Extract all links
        links = [{"text": link.get_text(strip=True), "href": link.get('href')} for link in soup.find_all('a') if link.get('href')]

        # Extract structured data into sections
        structured_data = []
        for section in soup.find_all(['div', 'section']):
            text = section.get_text(strip=True)
            if text:
                structured_data.append(text)

        # Compile results
        data = {
            "metadata": metadata,
            "visible_text": visible_text,
            "links": links,
            "sections": structured_data
        }

        return json.dumps(data, indent=4)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    url = input("Enter the URL to scrape: ")
    
    print(extract_all_data(url))
