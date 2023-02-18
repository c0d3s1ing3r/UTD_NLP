import sys
import requests
import argparse
import random
import os
from rest import RestEndpoint
import bs4

class WebCrawler:

    def __init__(self, initial_url: str):
        self.initial_url = RestEndpoint(initial_url, 'GET')
        self.visited_urls = set()
        self.to_visit_urls = set()
    
    def crawl(self, max_links: int = 15, seed: int = None) -> None:
        self.to_visit_urls.add(self.initial_url.url)
        if seed is not None:
            random.seed(seed)
        
        while len(self.to_visit_urls) > 0 and len(self.visited_urls) < max_links:
            # choose a random url from the set to visit
            url = random.choice(list(self.to_visit_urls))
            print('Visiting URL: {}'.format(url))
            response = requests.get(url)
            if response.status_code == 200:
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                urls = [link.get('href') for link in soup.find_all('a')]
                # filter out any urls that are not http or https
                urls = [url for url in urls if url != None and url.startswith('http')]
                for url in urls:
                    if url not in self.visited_urls and url not in self.to_visit_urls:
                        self.to_visit_urls.add(url)
                # dump the text from this page to a file
                # use the page title as the filename
                title = soup.find('title').text
                # filter characters that are not allowed in filenames
                title = ''.join([c for c in title if c.isalnum() or c == ' ']).rstrip()
                # only write the file if the text is not empty
                if soup.text != '':
                    with open('./visited_pages/{}.txt'.format(title), 'w', encoding='utf-8') as f:
                        f.write(soup.text)
                    # remove the url from the to_visit_urls set and add it to the visited_urls set
                    try:
                        self.to_visit_urls.remove(url)
                        self.visited_urls.add(url)
                    except KeyError:
                        print('Error: URL {} not found in to_visit_urls'.format(url))
                else:
                    print('Error: No text found on page {}'.format(url))
                    self.to_visit_urls.remove(url)
            else:
                print('Error visiting URL: {}'.format(url))
                self.to_visit_urls.remove(url)

    def report(self) -> None:
        print('Visited URLs:')
        for url in self.visited_urls:
            print(url)
        print('Other found URLs:')
        for url in self.to_visit_urls:
            print(url)

def main(url: str):
    # clear the visited pages directory of all txt files
    for file in os.listdir('./visited_pages'):
        if file.endswith('.txt'):
            os.remove('./visited_pages/{}'.format(file))
    web_crawler = WebCrawler(url)
    web_crawler.crawl()
    web_crawler.report()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('url', type=str, help='Initial URL')
    args = parser.parse_args()

    main(args.url)


