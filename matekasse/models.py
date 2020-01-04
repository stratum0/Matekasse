from datetime import datetime
from matekasse import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    credit = db.Column(db.Integer, default=0)
    imgfile = db.Column(db.String(20), nullable=False, default='default.svg')
    debtallowed = db.Column(db.Boolean, nullable=False, default=True)
    lastchange = db.Column(db.DateTime)
    password = db.Column(db.String(60))
    locked = db.Column(db.Boolean, default=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.credit}', '{self.imgfile}', '{self.lastchange}')"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, default=0)
    imgfile = db.Column(db.String(20), nullable=False, default='default.svg')


class Credits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit = db.Column(db.Integer)
    pos = db.Column(db.Boolean, nullable=False)
