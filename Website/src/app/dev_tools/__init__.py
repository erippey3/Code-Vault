from flask import Blueprint


dev_tools = Blueprint('dev_tools', __name__, template_folder='templates')

from . import routes