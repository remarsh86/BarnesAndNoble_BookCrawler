import datetime
from datetime import datetime
import indexer as ix



def parse_book_info(content):
    # find all html tables oc class "pain centered and parse book info"
    item = {}

    #parse title
    try:
        title = content.find("h1", class_="pdp-header-title").contents[0]
        item['title'] = title
    except:
        print("No title for this item.")

    #parse authors
    try:
        authors_list = []
        authors = content.find('span', class_="contributors").contents
        for i in authors:
            try:
                if i.contents[0] not in authors_list:
                    print(str(i.contents[0]), '\n')
                    authors_list.append(i.contents[0])

            except:
                # print(i, '\n')
                pass
        item['authors']=authors_list
    except:
        print("No authors for this item.")

    #parse all other fields
    try:
        product_table = content.find_all("table", {'class': "plain centered"})

        print(product_table)
        table_rows = product_table[0]

        table_rows = product_table[0].find('tbody').findAll('tr')

        for row in table_rows:
            print()
            # print(row)
            th = row.find('th').contents[0]
            th = str(th.lower())
            th = th.replace(":", "")
            th = th.replace(" ", "_")
            th = th.replace("-", "_")
            print("th: ", th)
            if "publisher" in th:  # publisher row has a different format because of the url
                td = row.find('td').text
                td = td.strip('\n')  # remove trailing new line
            elif "sales_rank" in th:
                td = row.find('td').contents[0]
                td = td.replace(",", "")
            else:
                td = row.find('td').contents[0]
                td = td.strip('\n')
            print("td: ", td)
            item[th] = td

        item['publication_date'] = datetime.strptime(item['publication_date'], '%m/%d/%Y')

    except:
        print("No content for this item")

    print("item: ", item)

    #check if item dictionary is empty
    if not bool(item): #if is empty
        print("Item is empty; nothing parsed.")
    else:
        print("item keys: ", item.keys())
        # for k in item.keys():
        #     print("key:", k)
        if len(list(item.keys()))<3:
            print("Item not a book")
        else:
            print(item)
            ix.index_item(item)



