import threading 
import os
from queue import Queue
from crawler import Crawler
from functions import *

PROJECT_NAME = 'asesdtu'
HOME_PAGE = 'http://asesdtu.com/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = os.path.join(PROJECT_NAME, 'queue.txt')
CRAWLED_LIST = os.path.join(PROJECT_NAME, 'crawled_list.txt')
NUMBER_OF_THREADS = 8

queue = Queue()
Crawler(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)

# job of workers
def work():
    while True:
        url = queue.get()
        Crawler.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# Creating workers
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()

# Create job for each queue links
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# If links in queue, crawl them
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + ' links left')
        create_jobs()

create_workers()
crawl()
