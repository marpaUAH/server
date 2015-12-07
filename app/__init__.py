# Import flask and template operators
from flask import Flask, render_template

# Import PyMongo
from pymongo import MongoClient

# Import Beebotte
from beebotte import *

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database client
# by default localhost:27017
client = MongoClient()

# Define the db object and lnumbers collection
db = client.lottery
lnumbers = db.lnumbers

# Define the beebotte object
bclient = BBT('db26c05fa32d1ca054eaf60350914ff9','aa18e56f716b597b2fc0a33bbbdc4dc2d32aff0731edb3bc391fe1282c07f10e')

# Sample HTTP error handling
#@app.errorhandler(404)
#def not_found(error):
#    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_iroom)
from app.mod_iroom.controllers import mod_iroom as iroom_module

# Register blueprint(s)
app.register_blueprint(iroom_module)

