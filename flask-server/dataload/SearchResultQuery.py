import DatabaseProvider as db
from flask import jsonify

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

    def close(self):
        if self.connection is not None:
            self.connection.close()
            