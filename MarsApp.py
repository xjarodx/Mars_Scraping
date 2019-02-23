from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo 
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.marsdb
coll = db.mars_info

@app.route("/")
def index():
    mars_data = coll.find_one()
    return render_template("index.html", mars_data=mars_data)

from scrape_mars import scrapey_mars

@app.route("/scrape")
def scrape():
    mars_data = scrapey_mars()
    coll.update({"i":1}, {"$set": mars_data}, upsert = True)
    
if __name__ == "__main__":
    app.run(debug=True)
    