#scrapy spiders here:-
import scrapy

class CywareSpider(scrapy.Spider):
    name = 'cyware'
    start_urls = ['https://social.cyware.com/cyber-security-news-articles']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyware_data = []  # Variable to store scraped data

    def parse(self, response):
        # Extract the title, information, and threat type
        titles = response.css('.cy-card__title::text').getall()
        descriptions = response.css('.cy-card__description::text').getall()
        threat_types = response.css('.cursor-pointer.d-block.text-decoration-none.text-bold.text-primary::text').getall()

        # Zip the data and store in the list
        for title, description, threat_type in zip(titles, descriptions, threat_types):
            self.cyware_data.append({
                'title': title.strip(),
                'description': description.strip(),
                'threat_type': threat_type.strip(),
            })

        # Debug: Print to ensure data is captured
        self.log(f"Captured Cyware data: {self.cyware_data}")

        # Follow pagination if available
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        # Save data to a JSON file after the spider finishes
        with open('cyware_data.json', 'w') as f:
            import json
            json.dump(self.cyware_data, f, indent=4)
        self.log("Cyware data saved to cyware_data.json")

import json 
import scrapy
import json

class NciipcSpider(scrapy.Spider):
    name = "nciipc"
    start_urls = ["https://nciipc.gov.in/alert_and_Advisories.html"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nciipc_data = []  # Variable to store scraped data

    def parse(self, response):
        # Extracting titles with links
        titles = response.css('.confirmation')
        
        for title in titles:
            title_text = title.css('b::text').get()  # Extract title text (inside <b>)
            title_link = title.css('a::attr(href)').get()  # Extract link from <a> tag

            # Extracting the entire content inside <font class="advisoryFont">
            advisory_font_content = title.xpath('following-sibling::p/font[@class="advisoryFont"]//text()').getall()
            description_text = ''.join(advisory_font_content).strip()

            # Extracting severity (CVE ID) which is inside the <b> tag within the advisoryFont class
            severity = title.xpath('following-sibling::p/font[@class="advisoryFont"]/b/text()').get()

            self.nciipc_data.append({
                'title': title_text.strip() if title_text else None,
                'link': response.urljoin(title_link) if title_link else None,
                'description': description_text if description_text else None,
                'severity': severity.strip() if severity else None
            })

        # Saving data to JSON
        with open('nciipc_data.json', 'w') as f:
            json.dump(self.nciipc_data, f, indent=4)

        # Logging success
        self.log(f"Data saved to nciipc_data.json")

class ThreatPostSpider(scrapy.Spider):
    name = 'threatpost'
    allowed_domains = ['threatpost.com']
    start_urls = ['https://threatpost.com/']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            yield {
                'title': article.xpath('.//h2/a/text()').get(),
                'description': article.xpath('.//div[@class="excerpt"]/text()').get(),
                'url': article.xpath('.//h2/a/@href').get()
            }

        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


class CertSpider(scrapy.Spider):
    name = 'cert'
    allowed_domains = ['cert-in.org.in']
    start_urls = ['https://www.cert-in.org.in/']

    def parse(self, response):
        # Example: Extracting all text from paragraphs and headings
        for paragraph in response.xpath('//p/text()').getall():
            yield {'text': paragraph.strip()}

        for heading in response.xpath('//h3/text()').getall():
            yield {'heading': heading.strip()}

        # Follow pagination links if applicable (update selector as needed)
        next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)            
