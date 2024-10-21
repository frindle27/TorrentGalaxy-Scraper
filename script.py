from bs4 import BeautifulSoup
import requests

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

            # Maybe add uploader?

            # Size
            size_column = row.find('span', class_='badge badge-secondary')
            if size_column:
                torrent['size'] = size_column.text.strip()

            # Seeders/Leechers
            seeds_column = row.find('font', color='green')
            leech_column = row.find('font', color='#ff0000')
            if seeds_column:
                torrent['seeders'] = seeds_column.text.strip()
            if leech_column:
                torrent['leechers'] = leech_column.text.strip()

            # Magnet link
            download_link = row.find('a', role='button')
            if download_link:
                torrent['link'] = download_link['href']

            if torrent:
                torrents.append(torrent)

        return torrents
    

torrentgalaxy = torrentgalaxy()

test_url = 'https://torrentgalaxy.to/torrents.php?c20=1&c21=1&c18=1&search=CamScanner&lang=0&nox=2#results'

html_content = torrentgalaxy.retrieve_url(test_url)

torrents = torrentgalaxy.parse_html(html_content)

for torrent in torrents:
    print(torrent['name'])
