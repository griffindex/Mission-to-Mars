# Use Flask to render a template, redirect to another url, and create a URL.
from flask import Flask, render_template, redirect, url_for

# Use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo

# Use the scraping code.
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#### app.config["MONGO_URI"] 
# tells Python that our app will connect to Mongo using a URI.

#### "mongodb://localhost:27017/mars_app" 
# URI that connect our app to Mongo.
# The app can reach Mongo through our localhost server, using port 27017, 
# and using a database named "mars_app".

@app.route("/")      # Home page
def index():
   mars = mongo.db.mars.find_one()      # Find the Mars collection.
   # Return an HTML template using an index.
   return render_template("index.html", mars=mars) # Use mars collection in MongoDB.

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars      # Mongo database
   mars_data = scraping.scrape_all()    # scraping.py exported from Jupyter Notebook.

   # .update(query_parameter, data, options)
   mars.update({}, mars_data, upsert=True)

   # Navigate page back to / where we can see the updated content.
   return redirect('/', code=302)

# Save and run.
if __name__ == "__main__":
   app.run()