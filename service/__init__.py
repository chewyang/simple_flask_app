"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import os
from flask import Flask
from datetime import timedelta
from service import config
# from config import ProductionConfig, TestingConfig

# Create Flask application
app = Flask(__name__, template_folder='../templates')

if os.environ.get('FLASK_DEBUG') == 'production':
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.TestingConfig)
app.logger.info("Service initialized!")

from service import models, routes

models.init_db(app)