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

def crawl(url, content):
    #crawl other urls on page:
    for item in content.find_all("a", href=True):
        #avoid cycles
        url2 = item['href'] #relative url
        url2 = urljoin(url, url2)  # Actual URL
        #print("URL2!!!!!!!: ", url2)
        if url2 in scraped_urls:
            print("already visited ", url2)
        else:
            #scraped_urls.append(url2)
            #only crawl barnesandnoble sites
            if (str(url2).startswith("https://www.barnesandnoble.com/w/")):
                if ('javascript' not in str(url2)):
                    print("follow ", url2)
                    scrape(url2)
            else:
                print("don't follow: ", url2)


def scrape(url ):
    print("what is in scraped_url: ")
    for x in scraped_urls:
        print(x)
    url = url

    #Avoid 403 Errors
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    #response = requests.get(url, timeout =5)
    response = requests.get(url,  headers)
    raw_html = response.content
    content = BeautifulSoup(raw_html, "lxml")

    if str(url) not in scraped_urls:
        scraped_urls.append(url)
        print("!!!!! in else!!!!")
        # if str(url).startswith("https://www.barnesandnoble.com/w/"): # this could be a book detail page
        if "ean" in str(url):
            print("Parse book info for page: ", url)
            # response = requests.get(url, timeout=5)
            # content_url2 = BeautifulSoup(response.content, "html.parser")
            # ps.parse_book_info(content_url2)
            ps.parse_book_info(content)

        crawl(url, content)


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

#scrape('https://www.barnesandnoble.com/reviews/england-under-the-normans-and-angevins-1066-1272-h-w-c-davis/1101964326?ean=9781411446687')
print("!!!!!!!!!!!!!!!")
for x in scraped_urls:
    print(x)



