from flask import Flask
from config import Config
from model import db
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__, template_folder='./Front-End')
    app.config.from_object(Config)

    handler = RotatingFileHandler('file_browser.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # Initialize the database
    db.init_app(app)

    

    return app
