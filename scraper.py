import urllib

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlopen
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
    response = requests.get(url,  headers)
    raw_html = response.content
    content = BeautifulSoup(raw_html, "html.parser")

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
            if str(url2).startswith("https://www.barnesandnoble.com/w/"):
                if "ean" in str(url):
                    print("Parse book info!")
                    ps.parse_book_info(content)
                else:
                    print("follow ", url2)
                    scrape(url2)
#
# def parse_book_info(content):
#     product_table = content.find_all("table", class_="plain centered")
#     print(product_table)
#
#     table_rows = product_table[0].find('tbody').findAll('tr')
#     item = {}
#     for row in table_rows:
#         print()
#         # print(row)
#         th = row.find('th').contents[0]
#         print("th: ", th)
#         if "Publisher" in th:
#             td = row.find('td').text
#             td = td.strip('\n')  # remove trailing new line
#         else:
#             td = row.find('td').contents[0]
#         print("td: ", td)
#         item[th]=td



#start scraper
#scrape('http://books.toscrape.com/index.html')
scrape('https://www.barnesandnoble.com/')
print("!!!!!!!!!!!!!!!")
for x in scraped_urls:
    print(x)



