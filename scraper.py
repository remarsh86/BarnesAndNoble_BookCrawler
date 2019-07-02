import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlopen
import parser as ps
import re

class scraper():



    scraped_urls=[]
    isbns=[]
    #counter =0
    def scrape(self, url ):

        url = url
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


        #scrape other urls on page:
        for item in content.find_all("a", href=True):
            #avoid cycles
            url2 = item['href']
            #print(url2)
            url2 = urljoin(url, url2)  # Actual URL
            print("URL2!!!!!!!: ", url2)
            #scraped_urls.append(url2)
            if url2 in self.scraped_urls:
                print("already visited")
            else:
                self.scraped_urls.append(url2)
                # url2 = urljoin(url, url2) #Actual URL
                # print("URL2!!!!!!!: ", url2)
                # scraped_urls.append(url2)
                if str(url2).startswith("https://www.barnesandnoble.com/w/"):
                    # if "ean" in str(url):
                    #     print("Parse book info!")
                    #     ps.parse_book_info(content)
                    # else:
                    #     print("follow ", url2)
                    #     self.scrape(url2)
                     print("follow ", url2)
                     self.scrape(url2)


#start scraper
#scrape('http://books.toscrape.com/index.html')

scraper = scraper()
scraper.scrape('https://www.barnesandnoble.com/')
print("!!!!!!!!!!!!!!!")
for x in scraper.scraped_urls:
    print(x)



