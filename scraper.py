import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlopen
# #from __future__ import print_function
# import pysolr
# import datetime
# from datetime import datetime
import parser as ps

scraped_urls=[]
#counter =0
def scrape(url ):

    url = url #relativ URL
    #Avoid 403 Errors
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    #response = requests.get(url, timeout =5)
    response = requests.get(url,  headers)
    raw_html = response.content
    content = BeautifulSoup(raw_html, "lxml")

    #crawl other urls on page:
    for item in content.find_all("a", href=True):
        #avoid cycles
        url2 = item['href']
        url2 = urljoin(url, url2)  # Actual URL
        #print(url2)
        if url2 in scraped_urls:
            print("already visited ", url2)
        else:
            scraped_urls.append(url2)
            #url2 = urljoin(url, url2) #Actual URL
            print("URL2!!!!!!!: ", url2)
            if str(url).startswith("https://www.barnesandnoble.com/w/"):
                if "ean" in str(url):
                    print("Parse book info for page: ", url2)
                    response = requests.get(url2, timeout=5)
                    content_url2 = BeautifulSoup(response.content, "html.parser")
                    ps.parse_book_info(content_url2)
                else:
                    print("follow ", url2)
                    scrape(url2)

# def parse_book_info(content):
#     # find all html tables oc class "pain centered and parse book info"
#     item = {}
#     title = content.find("h1", class_="pdp-header-title").contents[0]
#     item['Title'] = title
#
#
#     product_table = content.find_all("table", class_="plain centered")
#     #print(product_table)
#     table_rows = product_table[0].find('tbody').findAll('tr')
#
#     for row in table_rows:
#         print()
#         # print(row)
#         th = row.find('th').contents[0]
#         print("th: ", th)
#         if "Publisher" in th: #publisher row has a different format because of a url
#             td = row.find('td').text
#             td = td.strip('\n')  # remove trailing new line
#         else:
#             td = row.find('td').contents[0]
#         print("td: ", td)
#         item[th]=td
#
#     index_item(item)


# def index_item(item):
#     #item is a dictionary
#     # solr = pysolr.Solr('http://localhost:8983/solr/web', timeout=10)
#     #
#     # solr.add([
#     #     {
#     #         "title": "xx",
#     #         "authors": ["aaa", "bbb", "ccc"],
#     #         "isbn": item['ISBN-13:'],
#     #         "publisher": item['Publisher:'],
#     #         "publication_date": datetime.strptime(item['Publication date:'],'%m/%d/%Y') ,
#     #         "pages": item['Pages:'],
#     #         "sales_rank": item['Sales rank:'],
#     #         "product_dimensions": ['Product dimensions:']
#     #     },
#     # ])
#     # solr.commit()
#
#     pass


#start scraper
#scrape('http://books.toscrape.com/index.html')
scrape('https://www.barnesandnoble.com/')
print("!!!!!!!!!!!!!!!")
for x in scraped_urls:
    print(x)



