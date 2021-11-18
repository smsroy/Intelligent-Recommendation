from flask import Flask
from SearchResultQuery import SearchResultQuery as srq

app = Flask(__name__)

# Api Route
@app.route("/reco")
def reco():
    return {"reco": ["Samsung", "Sony", "Westin"]}

# Api Route
@app.route("/search-result-query")
def searchResultQuery():
    searchQ = srq()
    result = searchQ.get_master_data()
    returnString = ''
    for res in result:
        returnString = returnString + res['title']+'\n'+ '<br>' + '<br>'
    return returnString


if __name__ == "__main__":
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)