import DatabaseProvider as db
from flask import jsonify
import json

class SearchResultQuery:
    connection = None

    def __init__(self):
        if self.connection is None:
            self.connection = db.get_db()
        return

    def get_master_data(self):
        cursor = self.connection.execute('SELECT title, url, rating, reviews, price, search_url FROM consumer_products_master')
        result = cursor.fetchall()
        fields_list = cursor.description   # sql key name
        # print("fields result -->",type(fields_list))
        column_list = []
        for i in fields_list:
            column_list.append(i[0])
        print("print final colume_list",column_list)

        jsonData_list = []
        for row in result:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            jsonData_list.append(data_dict)
        # print("Query Json Data",jsonData_list)
        cursor.close()
        return jsonData_list

    def get_master_data_arr(self, category):
        cursor = self.connection.execute('SELECT title, url, rating, reviews, price, search_url, description FROM consumer_products_master WHERE category=\'%s\' ORDER BY title '
        % (category))
        result = cursor.fetchall()
        cursor.close()
        return result
        # result_arr = []
        # for row in result:
        #     resarr = []
        #     resarr.append(row["title"])
        #     # resarr.append("<a href='https://amazon.com'" + row["url"] + "'>url</a>")
        #     resarr.append(row["rating"])
        #     resarr.append(row["reviews"])
        #     resarr.append(row["price"])
        #     resarr.append("open link")
        #     result_arr.append(resarr)
        # print("result_arr",result_arr)
        # cursor.close()
        # return json.dumps(result_arr)

    def get_data_stats(self):
        cursor = self.connection.execute('SELECT category, count(*) as count from consumer_products_master GROUP BY category')
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_product_desc(self, category):
        cursor = self.connection.execute('SELECT category, description from consumer_products_master WHERE category=\'%s\''
        % (category))
        result = cursor.fetchall()
        cursor.close()
        return result

    def close(self):
        if self.connection is not None:
            self.connection.close()
            