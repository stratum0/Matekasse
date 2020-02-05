from flask import Blueprint

overview = Blueprint('overview', __name__)

from matekasse.overview import overview
