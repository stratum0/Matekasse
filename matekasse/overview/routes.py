from flask import Blueprint, render_template, flash, redirect, url_for
from matekasse.models import User, Transaction

overview = Blueprint('overview', __name__)


@overview.route("/overview")
def overviews():
    user = User.query.all()
    transaction = Transaction.query.all()
    return render_template('overview.html', user=user, transaction=transaction)