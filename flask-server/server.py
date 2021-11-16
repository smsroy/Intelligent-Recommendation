from flask import Flask

app = Flask(__name__)

# Api Route
@app.route("/reco")
def reco():
    return {"reco": ["Samsung", "Sony", "Westin"]}


if __name__ == "__main__":
    print ("Starting application")
    app.run(host="localhost", port=5000, debug=True)