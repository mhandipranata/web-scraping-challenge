from flask import Flask, render_template, redirect, url_for
import pymongo
import scrape_mars

app = Flask(__name__)

# Setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Connect to mongo db and collection
db = client.mars_db
collection = db.mars 

# mongo = pymongo(app)

@app.route("/")
def index():
    mars = db.collection.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = db.collection
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
    # app.run_server(
    #     port=27017,
    #     host='0.0.0.0'
    # )


