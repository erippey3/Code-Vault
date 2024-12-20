from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from elasticsearch import Elasticsearch
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379" 
)


es = None 

# elastic search factory
def init_es(app):
    global es

    es = Elasticsearch("http://elasticsearch:9200", http_auth=(app.config['ELASTICSEARCH_USER'], app.config['ELASTICSEARCH_PASSWORD']))




login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .model import User
    return User.query.get(int(user_id))


