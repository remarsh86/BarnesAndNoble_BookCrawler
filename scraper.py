import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
#from urllib.request import urlopen
import parser as ps
import re

from socket import error as SocketError
import errno
#For getting pool of proxies - https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
from itertools import cycle
import traceback
from lxml.html import fromstring



class Scraper():

    pages_visited=[]
    isbns=[]


    def scrape(self, url, links_todo, proxy):
        print("scraped urls: ", self.pages_visited)
        print("links_todo: ", links_todo)
        for x in self.pages_visited:
            if x in links_todo:
                print("oh no: the following book is in linked_todo and scraped_urls: ", x)
        self.pages_visited.append(url)
        #url = url
        #Avoid 403 Errors
        # headers = requests.utils.default_headers()
        # headers.update({
        #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        # })
        #response = requests.get(url,  headers)
        response = requests.get(url, proxies = {'http':proxy})
        raw_html = response.content
        content = BeautifulSoup(raw_html, "html.parser")

        print("What is this url? ", url)
        if "ean=" in str(url):
            try:
                isbn = re.search(r'ean=([0-9]{13})', str(url)).group(1)
                if isbn not in self.isbns:
                    self.isbns.append(isbn)
                    print("Parse book info!")
                    ps.parse_book_info(content)
                else:
                    print("already parsed that book")
            except:
                print("curious, no isbn ")
        else:
            try:
                #isbn = re.search(r'([0-9]{13})', str(url)).group(1)
                isbn = re.search(r'([0-9]{10})', str(url)).group(1)

                if isbn not in self.isbns:
                    self.isbns.append(isbn)
                    print("Parse book info!")
                    ps.parse_book_info(content)
                else:
                    print("already parsed that book")
            except:
                print("curious, no isbn ")


        #scrape other urls on page:
        found_urls = self.crawl(content, links_todo, url)
        return found_urls

    def crawl(self, content,  links_todo, url):
        # print("how many links")
        # print(content.find_all("a", href=True))
        found_urls = []
        for item in content.find_all("a", href=True):
            # avoid cycles
            relative_url = item['href']
            full_url = urljoin(url, relative_url)  # Actual URL
            print("URL2!!!!!!!: ", full_url)

            if full_url in self.pages_visited:
                print("already visited")
            elif str(full_url).startswith("https://www.barnesandnoble.com/w/"):

                if (str(full_url) not in links_todo) and (str(full_url) not in found_urls) and (
                        (len(links_todo) + len(found_urls)) < 20000):
                    print("apend to list")
                    found_urls.append(str(full_url))
        print("what is in list found_urls?", found_urls)
        return found_urls





def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text) #fromstring has attribute 'xpath'
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        print("i", i.xpath('.//td[7]/text()'))

        # if i.xpath('.//td[7][contains(text(),"yes")]'):
        # Grabbing IP and corresponding PORT
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
        print(proxy)
    return proxies

#start scraper
links_todo = ['https://www.barnesandnoble.com/']
proxies = get_proxies()
proxy_pool = cycle(proxies)
scraper = Scraper()
while(links_todo and (len(links_todo)<20000)):#until list is emtpy, keep crawling
    print("length of links_todo: ", len(links_todo))
    url = links_todo.pop() #returns last element and removes that element from the list
    print("length of links_todo after pop: ", len(links_todo))

    #rotate proxies
    for i in range (1, 11):
        proxy = next(proxy_pool) # get random next proxy

        try:
            new_urls = scraper.scrape(url, links_todo, proxy)
        #except SocketError as e:
            # if e.errno != errno.ECONNRESET:
            #     raise  # Not error we are looking for
            # pass  # Handle error here.
        except:
            print("Skipping. Connection error")

        links_todo += new_urls


    # print("!!!!!!!!!!!!!!!")
    # print("links to do: ", links_todo)



