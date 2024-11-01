from flask import Flask
from config import Config
from .extensions import limiter, db, migrate, talisman
from flask import current_app
from flask_dance.contrib.github import make_github_blueprint
import os


import logging
from logging.handlers import RotatingFileHandler





def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        current_app.logger.warning(f"403 Access Denied: {e}")
        return "Access denied", 403




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    talisman.init_app(app)

    handler = RotatingFileHandler('logs/file_browser.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self"
        return response



    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from dotenv import load_dotenv
    load_dotenv()

    github_blueprint = make_github_blueprint(
        client_id=os.environ.get('GITHUB_CLIENT_ID'),
        client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
        scope='user:email',
    )
    app.register_blueprint(github_blueprint, url_prefix='/github_login')

    
    register_error_handlers(app)

    return app