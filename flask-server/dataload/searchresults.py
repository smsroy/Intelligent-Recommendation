from selectorlib import Extractor
import requests 
import json 
from time import sleep
import sqlite3

import DatabaseProvider as db

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

def __drop_master_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS consumer_products_master')

def __create_master_table(create):
    if create:
        connection = db.get_db()
        cursor = connection.cursor()
        __drop_master_table(cursor)
        cursor.execute('CREATE TABLE consumer_products_master(title TEXT, url TEXT, rating TEXT, reviews INTEGER, price REAL, search_url TEXT)')
        cursor.close()
        connection.close()

def __insert_master_record(cursor, title, url, rating, reviews, price, search_url):
    cursor.execute(
        'INSERT OR REPLACE INTO consumer_products_master (title, url, rating, reviews, price, search_url) VALUES(?, ?, ?, ?, ?, ?)',
        (title, url, rating, reviews, price, search_url))


def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

# product_data = []
connection = db.get_db()
cursor = connection.cursor()
__create_master_table(True)
with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url) 
        if data:
            for product in data['products']:
                product['search_url'] = url
                # print("Saving Product: %s"%product['title'])
                json.dump(product,outfile)
                outfile.write("\n")
                #insert data
                __insert_master_record(cursor, product['title'], product['url'], product['rating'], product['reviews'], product['price'], product['search_url'])
                #sleep(10)
connection.commit()
cursor.close()
connection.close()
    