from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import PRA.mongocreds


app = Flask(__name__)
app.config['MONGO_URI'] = mongocreds.mongo_uri 
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)


from PRA import routes
