from flask import Flask
from config import Config
from .extensions import limiter, db, migrate, talisman
from flask import current_app
from flask_dance.contrib.github import make_github_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
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
    app.debug = True
    app.config.from_object(Config)


    handler = RotatingFileHandler('logs/file_browser.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)



    limiter.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    talisman.init_app(app)


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
        redirect_url='http://192.168.44.4:54003/github_login/authorized',
        authorized_url='/authorized',
    )
    app.register_blueprint(github_blueprint, url_prefix='/github_login')



    register_error_handlers(app)



    @app.route('/db_test')
    def db_test():
        from sqlalchemy import text
        try:
            db.session.execute(text('SELECT 1'))
            return 'Database connection successful'
        except Exception as e:
            app.logger.error(f'Database connection failed: {e}')
            return 'Database connection failed'

    return app