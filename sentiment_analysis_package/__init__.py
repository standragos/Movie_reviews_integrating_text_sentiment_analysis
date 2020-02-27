from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
db = SQLAlchemy(app)

from sentiment_analysis_package import routes