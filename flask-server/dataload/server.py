from flask import Flask, jsonify
from SearchResultQuery import SearchResultQuery as srq
import CosineSimCalculator as cal
import queue as Q
from collections import deque
import json

app = Flask(__name__)

class Result(object):
    def __init__(self, priority, url, rating, title, price, reviews):
        self.priority = priority
        self.url = url
        self.rating = rating
        self.title = title
        self.price = price
        self.reviews = reviews
        return

    def __lt__(self, other):
        return -1 * cmp(self.priority, other.priority)

    def __repr__(self):
        return str(self.priority) + " : " + self.url

def cmp(a, b):
    return bool(a) ^ bool(b) 

# Api Route
@app.route("/reco")
def reco():
    return {"reco": ["Samsung", "Sony", "Westin"]}

# Api Route
@app.route("/search-result-query")
def searchResultQuery():
    searchQ = srq()
    result = searchQ.get_master_data()
    searchQ.close()
    print('result', result)
    return jsonify({'space': result})

# Api Route
@app.route("/search-result-queryarr/<keywords>/<category>", methods=['GET'])
def searchResultQueryArr(keywords, category):
    result = __get_ranked_products(keywords, category)
    # searchQ = srq()
    # result = searchQ.get_master_data_arr()
    # searchQ.close()
    print('result', result)
    return result
  

def __get_ranked_products(keywords, category):
    searchQ = srq()
    product_listings = searchQ.get_master_data_arr(category)
    searchQ.close()
    q = Q.PriorityQueue()
    for product in product_listings:
        if product['description']:
            product_description = product['description'] + "Product Title: " + product['title']
            q.put(Result(cal.get_sim(keywords, product_description), product['url'], product['rating'], product['title'], product['price'], product['reviews']))
    result = []
    for i in range(0, len(q.queue)):
        result.append(q.get())
    
   
    result_arr = []
    for row in result:
        resarr = []
        resarr.append(row.title)
        if(row.rating):
            resarr.append(row.rating[:3])
        else:
            resarr.append(row.rating)
        resarr.append(row.reviews)
        resarr.append(row.price)
        resarr.append(row.url)
        result_arr.append(resarr)
    print("result_arr",result_arr)
    return json.dumps(result_arr)

if __name__ == "__main__":
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)