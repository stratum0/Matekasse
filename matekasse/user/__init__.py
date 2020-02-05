from flask import Blueprint

user = Blueprint('user', __name__)

from matekasse.user import routes, events
