from flask import Flask, jsonify
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
    searchQ.close()
    print('result', result)
    return jsonify({'space': result})
  

if __name__ == "__main__":
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)