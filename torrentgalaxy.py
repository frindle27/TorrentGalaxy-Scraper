from bs4 import BeautifulSoup
from novaprinter import prettyPrinter
import requests
import threading

class torrentgalaxy(object):
    url = 'https://torrentgalaxy.to/'
    name = 'TorrentGalaxy'
    supported_categories = {
        'all': '',
        'anime': 'c28=1',
        'apps': 'c20=1&c21=1&c18=1',
        'books': 'c13=1&c19=1&c12=1&c14=1&c15=1',
        'docus': 'c9=1',
        'games': 'c43=1&c10=1',
        'movies': 'c3=1&c46=1&c45=1&c42=1&c4=1&c1=1',
        'music': 'c22=1&c26=1&c23=1&c25=1&c24=1',
        'other': 'c17=1&c40=1&c37=1&c33=1',
        'tv': 'c41=1&c5=1&c11=1&c6=1&c7=1',
        'xxx': 'c48=1&c35=1&c47=1&c34=1',
    }

    def retrieve_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status() # Raises HTTPError for bad HTTP response (e.g., 404 or 500)
            return response.text # Return the HTML content of the page
        
        except requests.exceptions.HTTPError as e:
            print(f'Error fetching URL {url}: {e}')
            return None

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        torrents = [] # List of all torrents, each torrent is a dictionary

        # Each row is a torrent
        for row in soup.find_all('div', class_='tgxtablerow'):
            torrent = {}

            # Name and link
            title_column = row.find('a', class_='txlight')
            if title_column:
                torrent['name'] = title_column['title']
                torrent['desc_link'] = self.url + title_column['href']

            # Size
            size_column = row.find('span', class_='badge badge-secondary')
            if size_column:
                torrent['size'] = size_column.text.strip()

            # Seeders/Leechers
            seeds_column = row.find('font', color='green')
            leech_column = row.find('font', color='#ff0000')
            if seeds_column:
                torrent['seeds'] = seeds_column.text.strip()
            if leech_column:
                torrent['leech'] = leech_column.text.strip()

            # Magnet link
            download_link = row.find('a', role='button')
            if download_link:
                torrent['link'] = download_link['href']

            if torrent:
                torrents.append(torrent)

        return torrents
    
    def get_number_of_pages(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        pagination = soup.find('ul', class_='pagination')

        if pagination:
            pages = pagination.find_all('li')
            if len(pages) > 1:
                return int(pages[-2].text) # The second last item is the last page number, the last one is a next button
            
        return 1
    
    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        query = str(what).replace(' ', '+')

        search_url = f'{self.url}torrents.php?search={query}&sort=seeders&order=desc'

        # Fetch the first page of results
        html_content = self.retrieve_url(search_url)
        if not html_content:
            return
        
        # Parse and print results from the first page
        torrents = self.parse_html(html_content)
        for torrent in torrents:
            torrent['engine_url'] = self.url # Add engine URL
            torrent['pub_date'] = -1
            prettyPrinter(torrent)

        # Handle pagination (fetch additional pages using multithreading)
        total_pages = self.get_number_of_pages(html_content)

        if total_pages > 1:
            threads = []

            for page in range(1, total_pages): # Pages are 0 indexed in torrentgalaxy.to
                page_url = f'{search_url}&page={page}'
                thread = threading.Thread(target=self.fetch_and_print_page, args=(page_url,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()

    def fetch_and_print_page(self, url):
        html_content = self.retrieve_url(url)

        if html_content:
            torrents = self.parse_html(html_content)

            for torrent in torrents:
                torrent['engine_url'] = self.url # Add engine URL
                prettyPrinter(torrent)
