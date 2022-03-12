#import flask
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#create the app
app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app) 

#app routes
@app.route("/")
def index():
    #find mars in our database, convert to html
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#scraping route
@app.route("/scrape")
def scrape():
    #access db
    mars = mongo.db.mars
    #scrape using scraping script
    mars_data = scraping.scrape_all()
    #update the database
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    #redirect us back after updating
    return redirect('/', code=302)

#run the app
if __name__ == "__main__":
    app.run()