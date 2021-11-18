import DatabaseProvider as db

class SearchResultQuery:
    connection = None

    def __init__(self):
        if self.connection is None:
            self.connection = db.get_db()
        return

    def get_master_data(self):
        cur = self.connection.execute('SELECT title, url, rating, reviews, price, search_url FROM consumer_products_master')
        result = cur.fetchall()
        cur.close()
        return result

    def close(self):
        if self.connection is not None:
            self.connection.close()
            