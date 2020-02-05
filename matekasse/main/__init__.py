from flask import Blueprint

main = Blueprint('main', __name__)

from matekasse.main import routes
