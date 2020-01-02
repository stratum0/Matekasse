from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from matekasse import db
from matekasse.user.forms import RegistrationForm, Credit, Transfer, Edit
from matekasse.models import User, Transaction, Item

user = Blueprint('user', __name__)


@user.route("/register", methods=['Post', 'Get'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


def getCredit(credit):
    addrem = credit[:3]
    credit = credit[3:]
    switch = {
        "zerofive": 0.5,
        "one": 1,
        "onefive": 1.5,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "ten": 10,
        "twenty": 20,
        "fifty": 50
    }
    if addrem == 'add':
        return 0 + switch.get(credit)
    else:
        return 0 - switch.get(credit)


@user.route("/user/<int:user_id>", methods=['Post', 'Get'])
def userpage(user_id):
    # Check User
    user = User.query.get_or_404(user_id)

    # import Forms
    creditform = Credit()
    transferform = Transfer()
    edit = Edit()

    # Credit foo
    if creditform.validate_on_submit() and True in list(creditform.data.values()):
        credit = getCredit(list(creditform.data.keys())[list(creditform.data.values()).index(True)])
        user.credit += credit
        setattr(user, 'lastchange', datetime.utcnow())
        addtransaction = Transaction(credit=credit, userid=user_id, date=datetime.utcnow())
        db.session.add(addtransaction)
        db.session.commit()
        return redirect(url_for('main.home'))

    # transaction foo
    users = User.query.filter(User.id.isnot(user_id)).all()
    choice = []
    for u in users:
        choice.append((u.id, u.username))
    transferform.beneficary.choices = choice
    if True in list(transferform.data.values()):
        transfer = 0
        for data in transferform.data:
            if transferform.data[data] is True:
                switch = {
                    "transferzerofive": 0.5,
                    "transferone": 1,
                    "transferonefive": 1.5,
                    "transfertwo": 2,
                    "transferthree": 3,
                    "transferfour": 4,
                    "transferfive": 5,
                    "transferten": 10
                }
                transfer += switch.get(data)
        user.credit -= transfer
        beneficary = User.query.filter(User.id == transferform.data["beneficary"]).first()
        beneficary.credit += transfer
        setattr(user, 'lastchange', datetime.utcnow())
        addUserRecord = Transaction(credit=transfer * -1, userid=user_id, date=datetime.utcnow())
        setattr(beneficary, 'lastchange', datetime.utcnow())
        addBeneficaryRecord = Transaction(credit=transfer, userid=transferform.data["beneficary"], date=datetime.utcnow())
        db.session.add(addUserRecord)
        db.session.add(addBeneficaryRecord)
        db.session.commit()
        return redirect(url_for('main.home'))

    # query for transaction table
    transaction = Transaction.query.filter(Transaction.userid == user_id).all()

    # Item foo
    item = Item.query.all()
    if edit.validate_on_submit() and True in list(edit.data.values()):
        if edit.delete.data:
            db.session.query(Transaction).filter(Transaction.userid == user_id).delete()
            db.session.delete(user)
        if edit.edit.data:
            user.username = edit.rename.data
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('user.html', title=user.username, user=user, transaction=transaction, creditform=creditform, transferform=transferform, item=item, edit=edit)


@user.route("/user/<int:user_id>/<int:item_id>", methods=['Post', 'Get'])
def buyitem(user_id, item_id):
    usr = User.query.get_or_404(user_id)
    item = Item.query.get_or_404(item_id)
    usr.credit -= item.price
    db.session.commit()
    return redirect(url_for('user.userpage', user_id=user_id))
