from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links_set = set()

    def error(self, msg):
        pass

    def handle_starttag(self, tag, attrs):
        #print(tag)
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    # if value is relative url, combine it with base_url
                    url = parse.urljoin(self.base_url, value)
                    self.links_set.add(url)

    def page_links(self):
        return self.links

#finder = LinkFinder()
#finder.feed('<html><head><a hrf="https://www.google.com"></a></head></html>')
