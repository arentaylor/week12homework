import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

sys.setrecursionlimit(2000)
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.marsfacts



@app.route('/scrape')
def scrape():
   # db.collection.remove()
    mars = scrape_mars.scrape()
    print("\n\n\n")
    db.marsfacts.update({}, mars, upsert=True)
    return render_template("index.html", mars = mars)

@app.route("/")
def home():
    mars = list(db.marsfacts.find())
    print(mars)
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
    app.run(debug=True)