import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlopen
import parser as ps
import re



class Scraper():

    scraped_urls=[]
    isbns=[]


    def scrape(self, url):
        print("scraped urls: ", self.scraped_urls[:5])
        self.scraped_urls.append(url)
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
        found_urls = []
        #scrape other urls on page:
        for item in content.find_all("a", href=True):
            #avoid cycles
            relative_url = item['href']
            full_url = urljoin(url, relative_url)  # Actual URL
            print("URL2!!!!!!!: ", full_url)


            if full_url in self.scraped_urls:
                print("already visited")
            elif str(full_url).startswith("https://www.barnesandnoble.com/w/"):
                #     print("Add url to list", full_url)
                #     #self.scrape(url2)
                #     found_urls.append(full_url)
                print("apend to list")
                found_urls.append(str(full_url))
        print("what is in list found_urls?", found_urls)
        return found_urls


#start scraper
links_todo = ['https://www.barnesandnoble.com/']
scraper = Scraper()
while(links_todo):#until list is emtpy, keep crawling
    url = links_todo.pop() #returns last element and removes that element from the list
    new_urls = scraper.scrape(url)
    links_todo += new_urls


    print("!!!!!!!!!!!!!!!")
    print("links to do: ", links_todo)



