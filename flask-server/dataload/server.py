from flask import Flask, jsonify
from SearchResultQuery import SearchResultQuery as srq
import CosineSimCalculator as cal
import queue as Q
from collections import deque
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

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
    #print('result', result)
    return jsonify({'space': result})

# Api Route
@app.route("/search-result-queryarr/<keywords>/<category>", methods=['GET'])
def searchResultQueryArr(keywords, category):
    result = __get_ranked_products(keywords, category)
    # searchQ = srq()
    # result = searchQ.get_master_data_arr()
    # searchQ.close()
    # print('result', result)
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
    #print("result_arr",result_arr)
    return json.dumps(result_arr)

# Api Route
@app.route("/search-result-stats", methods=['GET'])
def searchResultStats():
    searchQ = srq()
    result = searchQ.get_data_stats()
    result_arr = []
    for row in result:
        resarr = []
        resarr.append(row['category'])
        resarr.append(row['count'])
        result_arr.append(resarr)   
    searchQ.close()
    # print('result_arr', result_arr)
    return json.dumps(result_arr)

def __get_product_desc(category):
    searchQ = srq()
    product_desc = searchQ.get_product_desc(category)
    searchQ.close()
    descarr = []
    for product in product_desc:
        if product['description']:
            #product_description =   product['title'] + " " + product['description']
            product_description = product['description']
            descarr.append(product_description)
    # descarr = np.array(descarr).reshape(-1,1)
    # print('descarr', descarr.shape)
    return descarr

# Api Route
@app.route("/euclidean-product-distance/<category>", methods=['GET'])
def getEuclideanProductDistance(category):
    corpus = __get_product_desc(category)
    # print('corpus', corpus.shape)
    narr = []
    distnp = np.empty((), float)
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus).todense()
    print( vectorizer.vocabulary_ )
    i=0
    for f in features:
        arr = []
        dist = euclidean_distances(features[0], f)
        distval = dist[0][0]
        print("dist", distval)
        # distnp = np.append(distnp, np.array([distval]), axis=0)
        arr.append(i)
        arr.append(distval)
        narr.append(arr)
        i=i+1
    #narr = np.array(narr)
    print("narr", narr)
    return json.dumps(narr)

# Api Route
@app.route("/euclidean-distance", methods=['GET'])
def getEuclideanDistance():
    corpus = [
        'All my cats in a row',
        'When my cat sits down, she looks like a Furby toy!',
        'The cat from outer space',
        'Sunshine loves to sit like this for some reason.'
        ]
    narr = []
    distnp = np.empty((), float)
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus).todense()
    print( vectorizer.vocabulary_ )
    for f in features:
        dist = euclidean_distances(features[0], f)
        distval = dist[0][0]
        print("dist", distval)
        # distnp = np.append(distnp, np.array([distval]), axis=0)
        narr.append(distval)
    narr = np.array(narr)
    print("narr", narr)
    return "Success"

if __name__ == "__main__":
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)