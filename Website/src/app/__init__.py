from flask import Flask, current_app
from config import Config
from .extensions import limiter, db, migrate, init_es, login_manager
from flask_session import Session



import logging
from logging.handlers import RotatingFileHandler





def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        current_app.logger.warning(f"403 Access Denied: {e}")
        return "Access denied", 403
    
def register_session_endpoints(app):
    from flask import session, g
    from app.model import User
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is not None:
            g.user = User.query.get(user_id)
        else:
            g.user = None



def create_app():
    app = Flask(__name__, static_folder='static')
    app.debug = True
    app.config.from_object(Config)

    session = Session(app)



    handler = RotatingFileHandler('logs/file_browser.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)



    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    init_es(app)
    login_manager.init_app(app)



    #talisman.init_app(app)
    # talisman is causing issues 8 ways till Sunday

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.fileIO import fileIO as fileIO_blueprint
    app.register_blueprint(fileIO_blueprint)
    from app.dev_tools import dev_tools as dev_blueprint
    app.register_blueprint(dev_blueprint)


    register_error_handlers(app)
    register_session_endpoints(app)

    return app