from flask import Flask
from config import Config
from .extensions import limiter, db, migrate
from flask import current_app

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

    handler = RotatingFileHandler('logs/file_browser.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)



    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    
    register_error_handlers(app)

    return app