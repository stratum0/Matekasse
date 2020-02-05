from flask import Blueprint

item = Blueprint('item', __name__)

from matekasse.item import routes
