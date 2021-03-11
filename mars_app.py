# import depend
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import the scraping script
import scrape_mars

# creaet an instance of Flask
app = Flask(__name__)

# use PyMongo to establish Mongo Connection- week 12 day 3 act 9
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
        # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
