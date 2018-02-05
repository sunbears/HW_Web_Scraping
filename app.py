from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.marsDB

#Create a root route that will query Mongo database and pass the mars data into an HTML template
@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

#Create a route that will import the scrap_mars.py scrip and call the scrape function
#Store the return values in Mongo as a Python dicitonary
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    db.mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
