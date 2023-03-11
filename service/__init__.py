"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
from flask import Flask
from datetime import timedelta

# Create Flask application
app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3' #name of table for referencing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 5) 
app.logger.info("Service initialized!")

from service import models, routes

models.init_db(app)