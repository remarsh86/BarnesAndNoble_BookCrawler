
#from __future__ import print_function
import pysolr
import datetime
from datetime import datetime

def index_item(item):
    #solr_book = {}

    solr = pysolr.Solr('http://localhost:8983/solr/web', timeout=10)

    # solr_book = {}
    # accepted_fields = ['title', 'authors', 'isbn_13', 'publisher', 'publication_date', 'pages', 'sales_rank:', 'product_dimensions',
    #                    'edition_description', 'series', 'sold_by', 'format', 'file_size', 'age_range']
    # for k in item.keys():
    #     if k in accepted_fields:
    #         solr_book[k] = item[k]

    print("add book: ******************************", item)
    solr.add([item])
    solr.commit()

    pass
