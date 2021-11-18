import DatabaseProvider as db
from SearchResultQuery import SearchResultQuery as srq

searchQ = srq()
result = searchQ.get_master_data()
for res in result:
    print('title:', res['title'])
