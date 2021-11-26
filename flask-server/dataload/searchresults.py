from selectorlib import Extractor
from bs4 import BeautifulSoup 
import requests 
import json 
from time import sleep

import DatabaseProvider as db

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('flask-server\\dataload\\search_results.yml')

#######################################################################################

def __drop_master_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS consumer_products_master')

#######################################################################################

def __create_master_table(create):
    if create:
        connection = db.get_db()
        cursor = connection.cursor()
        __drop_master_table(cursor)
        cursor.execute('CREATE TABLE consumer_products_master(category TEXT, title TEXT, url TEXT, rating TEXT, reviews INTEGER, price REAL, search_url TEXT, description TEXT)')
        cursor.close()
        connection.close()

#######################################################################################

def __insert_master_record(cursor, category, title, url, rating, reviews, price, search_url, description):
    cursor.execute(
        'INSERT OR REPLACE INTO consumer_products_master (category, title, url, rating, reviews, price, search_url, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
        (category, title, url, rating, reviews, price, search_url, description))

#######################################################################################

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
    product_details =  e.extract(r.text)
    for product in product_details['products']:
        description_url = product['url']
        description = __get_product_description("https://www.amazon.com/" + description_url, headers)
        sleep(60)
        product.update({"description": description})
    
    return product_details

#######################################################################################

def __get_product_description(description_url, headers):
    try:
        r = requests.get(description_url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        product_description = ""
        lis = []
        description = soup.find("div", {"id" : "featurebullets_feature_div"})
        if description:
            ul = description.find('ul')
            if ul:
                lis = ul.findAll('li')
            for li in lis:
                product_description += li.text.strip() + '. '
            return product_description
        return None
    except:
        pass

#######################################################################################

connection = db.get_db()
cursor = connection.cursor()
__create_master_table(False)
with open("flask-server\\dataload\\search_results_urls.txt",'r') as urllist, open('flask-server\\dataload\\search_results_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        category = url[27:]
        data = scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                json.dump(product,outfile)
                outfile.write("\n")
                #insert data
                __insert_master_record(cursor, category, product['title'], product['url'], product['rating'], product['reviews'], product['price'], product['search_url'], product['description'])
connection.commit()
cursor.close()
connection.close()

#######################################################################################
    