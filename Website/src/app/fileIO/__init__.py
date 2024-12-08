from flask import Blueprint


fileIO = Blueprint('fileIO', __name__, template_folder='templates')

from . import routes