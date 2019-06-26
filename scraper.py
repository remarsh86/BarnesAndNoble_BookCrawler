import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlopen

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
    #print(raw_html)
    content = BeautifulSoup(raw_html, "html.parser")
    #print("URL: ", response.url)
    #print("!!!!!!!!!content: ",  content)
    # a_tag = content.find("a")
    # print(a_tag)



    #scrape other urls on page:
    for item in content.find_all("a", href=True):
        #avoid cycles
        url2 = item['href']
        print(url2)
        if url2 in scraped_urls:
            print()
        else:
            scraped_urls.append(url2)
            url2 = urljoin(url, url2) #Actual URL
            print("URL2!!!!!!!: ", url2)
            if str(url2).startswith("https://www.barnesandnoble.com"):
                if "ean" in str(url):
                    print("Parse book info!")
                    parse_book_info(content)
                else:
                    print("follow ", url2)
                    scrape(url2)

def parse_book_info(content):
    product_table = content.find_all("table", class_="plain centered")
    print(product_table)

    table_rows = product_table[0].find('tbody').findAll('tr')
    item = {}
    for row in table_rows:
        print()
        # print(row)
        th = row.find('th').contents[0]
        print("th: ", th)
        if "Publisher" in th:
            td = row.find('td').text
            td = td.strip('\n')  # remove trailing new line
        else:
            td = row.find('td').contents[0]
        print("td: ", td)
        item[th]=td


def index_item():
    # curl - X
    # POST - H
    # 'Content-Type: application/json' 'http://localhost:8983/solr/my_collection/update/json/docs' - -data - binary
    # '
    # {
    #     "id": "1",
    #     "title": "Doc 1"
    # }
    # '

    # req = urllib.Request(url='http://localhost:8983/solr/web/update/json?commit=true',
    #                       data={})
    # req.add_header('Content-type', 'application/json')
    # f = urlopen(req)

    pass


#start scraper
#scrape('http://books.toscrape.com/index.html')
scrape('https://www.barnesandnoble.com/')
print("!!!!!!!!!!!!!!!")
for x in scraped_urls:
    print(x)



