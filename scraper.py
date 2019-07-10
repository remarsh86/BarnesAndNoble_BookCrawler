import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import parser as ps
import re
import time



class Scraper():

    pages_visited=[]
    isbns=[]


    def scrape(self, url, links_todo):
        self.pages_visited.append(url)

        print("scraped urls: ", self.pages_visited)
        print("links_todo: ", links_todo)
        for x in self.pages_visited:
            if x in links_todo:
                print("oh no: the following book is in linked_todo and scraped_urls: ", x)

        #url = url
        #Avoid 403 Errors
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        response = requests.get(url,  headers)
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

        # print("how many links")
        # print(content.find_all("a", href=True))

        #scrape other urls on page:
        for item in content.find_all("a", href=True):
            #avoid cycles
            relative_url = item['href']
            full_url = urljoin(url, relative_url)  # Actual URL
            print("URL2!!!!!!!: ", full_url)


            if full_url in self.pages_visited:
                print("already visited")
            elif str(full_url).startswith("https://www.barnesandnoble.com/w/"):

                if (str(full_url) not in links_todo)  and ((len(links_todo)+1)<1000):
                    #print("apend to list")
                    #found_urls.append(str(full_url))
                    links_todo.append(str(full_url))

        return links_todo


#start scraper
links_todo = ['https://www.barnesandnoble.com/']
scraper = Scraper()
while(links_todo and (len(links_todo)<1000)):#until list is emtpy, keep crawling
    print("length of links_todo: ", len(links_todo))
    #url = links_todo.pop() #returns last element and removes that element from the list
    url = links_todo.pop(0)  # returns first element and removes that element from the list
    print("length of links_todo after pop: ", len(links_todo))

    #back off from server if delays pop up
    #t0 = time.time()

    try:
        print("parse this page: ", url)
        # new_urls = scraper.scrape(url, links_todo)
        # links_todo += new_urls
        links_todo = scraper.scrape(url, links_todo)

    except:
        print("Connection error")

    time.sleep(5)
    # response_delay = time.time() -t0
    # time.sleep(10*response_delay)





