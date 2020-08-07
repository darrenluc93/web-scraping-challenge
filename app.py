from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)


myclient = MongoClient("mongodb://127.0.0.1:5500/")
mars_database = myclient["mars_database"]

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_db = mongo.db.mars.find_one() # mars_data = mongo.data base name. collection
    return render_template("index.html", mars_data = mars_db) #Variable to pass = mars_data

@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars #Current collection
    mars_data = scrape_mars.scrapper() #calls the scrape function
    mars_info.update({}, mars_data, upsert=True) 
    return redirect("/", code=302) 

if __name__ == "__main__":
    app.run(debug=False)