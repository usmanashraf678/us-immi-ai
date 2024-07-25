# uscis_scraper/spiders/uscis_spider.py
import scrapy
import re

import os

class USCISSpider(scrapy.Spider):
    name = 'uscis_sitemap'
    allowed_domains = ['uscis.gov']
    start_urls = ['https://www.uscis.gov/sitemap']

    output_dir = "output"  # Define the output directory
    html_dir = os.path.join(output_dir, "htmls")
    pdf_dir = os.path.join(output_dir, "pdfs")

    def __init__(self, *args, **kwargs):
        super(USCISSpider, self).__init__(*args, **kwargs)
        # Create the directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)  

        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir)
        
        if not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir)
        
        self.counter = 0
        self.visited_urls = set()  # Keep track of visited URLs


    def parse(self, response):
        for a_tag in response.css('a'):
            href = a_tag.css('::attr(href)').get()
            text = a_tag.css('::text').get().strip() if a_tag.css('::text').get() else ''
            url = response.urljoin(href)
            if self.is_internal_link(url):
                yield scrapy.Request(url, callback=self.parse_page, meta={'link_text': text})

    def parse_page(self, response):
        # Check if the URL has been visited
        self.counter += 1

        link_text = response.meta.get('link_text', '')
        self.logger.info(f'Visiting item {self.counter}: {response.url} - Link text: {link_text}')
    

        with open(self.output_dir + '/visited_urls.txt', 'a') as f:
            f.write(f'{self.counter}: {link_text} {response.url}\n')
        
        if response.url in self.visited_urls:
            self.logger.info(f'Already visited: {response.url}')
            return
        
        self.visited_urls.add(response.url)


        # Check if the response is an HTML page
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')
        self.logger.info(f'Content-Type: {content_type}')
        if 'text/html' in content_type:
            normalized_link_text = self.normalize_filename(link_text)
            filename = os.path.join(self.html_dir, f'{self.counter}-uscis-{normalized_link_text}.html')
            body_size = len(response.body)
            
            with open(filename, 'wb') as f:
                self.logger.info(f'Saving HTML page: {filename} (size: {body_size} bytes)')
                f.write(response.body)
        else:
            # Handle non-HTML content (e.g., PDF)
            self.save_file(response)

    def save_file(self, response):
        # Save non-HTML content like PDFs
        path = response.url.split("/")[-1]
        file_path = os.path.join(self.pdf_dir, path)
        self.logger.info(f'Saving file {file_path}')
        # save name of the file in a text file:
        with open(self.pdf_dir + '/pdf_files.txt', 'a') as f:
            f.write(file_path + '\n')
        # with open(file_path, 'wb') as f:
            # f.write(response.body)

    def is_internal_link(self, url):
        return any(domain in url for domain in self.allowed_domains) and '/es/' not in url
    
    def normalize_filename(self, link_text):
        # Parse the link text and remove special characters from it
        normalized_link_text = re.sub(r'[<>:"/\\|?*]', '-', link_text)
        return normalized_link_text
