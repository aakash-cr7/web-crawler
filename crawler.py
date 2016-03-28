from urllib.request import urlopen
import os
from link_finder import LinkFinder
from functions import *

class Crawler:
    
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_list = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        Crawler.project_name = project_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = os.path.join(Crawler.project_name ,'queue.txt')
        Crawler.crawled_file = os.path.join(Crawler.project_name, 'crawled_list.txt')
        self.init()
        self.crawl_page('First Crawler', Crawler.base_url)
    
    @staticmethod
    def init():
        create_directory(Crawler.project_name)
        # Add base_url so that the crawler knows where to start i.e. home page
        create_files(Crawler.project_name, Crawler.base_url)
        Crawler.queue_set = file_to_set(Crawler.queue_file)
        Crawler.crawled_set = file_to_set(Crawler.crawled_file)

    @staticmethod
    def gather_links_from_page(page_url):
        html = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                raw_response = response.read()
                html = raw_response.decode('utf-8')

            finder = LinkFinder(Crawler.base_url, page_url)
            finder.feed(html)
        except Exception as e:
            print('Error')
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def crawl_page(thread, page_url):
        if page_url not in Crawler.crawled_set:
            print(thread + ' crawling ' + page_url)
            print('Queue set ' + str(len(Crawler.queue_set)) + '| Crawled set ' + str(len(Crawler.crawled_set)))
            print(Crawler.gather_links_from_page(page_url))
            Crawler.add_links_to_queue(Crawler.gather_links_from_page(page_url))
            # Move current url from the queue to the crawled set
            Crawler.queue_set.remove(page_url)
            Crawler.crawled_set.add(page_url)
            Crawler.update_files()

    
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Crawler.queue_set:
                continue
            if url in Crawler.crawled_set:
                continue
            if Crawler.domain_name != get_domain_name(url):
                continue
            Crawler.queue_set.add(url)

    # Converts current sets to files
    @staticmethod
    def update_files():
        set_to_file(Crawler.queue_set, Crawler.queue_file)
        set_to_file(Crawler.crawled_set, Crawler.crawled_file)

