from flask import render_template
from matekasse.models import User, Transaction
from matekasse.overview import overview


@overview.route("/overview")
def overviews():
    user = User.query.all()
    transaction = Transaction.query.all()
    return render_template('overview.html', user=user, transaction=transaction)