from flask import Blueprint, render_template, redirect, url_for
from matekasse.models import User

main = Blueprint('main', __name__)


@main.route("/")
def redHome():
    return redirect(url_for('main.home'))


@main.route("/home")
def home():
    user = User.query.all()
    return render_template('home.html', users=user)
