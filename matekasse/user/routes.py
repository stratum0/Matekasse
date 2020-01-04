from datetime import datetime

from flask import Blueprint, render_template, flash, redirect, url_for
from matekasse import db
from matekasse.user.forms import RegistrationForm, Transfer, Edit
from matekasse.models import User, Transaction, Item, Credits

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


@user.route("/user/<int:user_id>", methods=['Post', 'Get'])
def userpage(user_id):
    # Check User
    user = User.query.get_or_404(user_id)

    # import Forms
    transferform = Transfer()
    edit = Edit()

    # query for transaction table
    transaction = Transaction.query.filter(Transaction.userid == user_id).all()
    negcredit = Credits.query.filter(Credits.pos.isnot(True)).order_by(Credits.credit.asc()).all()
    poscredit = Credits.query.filter(Credits.pos.isnot(False)).order_by(Credits.credit.asc()).all()

    # transaction foo
    users = User.query.filter(User.id.isnot(user_id)).all()
    choice = []
    for u in users:
        choice.append((u.id, u.username))
    transferform.beneficary.choices = choice
    credit = []
    for c in poscredit:
        credit.append((c.credit, "{0:.2f}€".format((c.credit / 100))))
    transferform.sum.choices = credit
    if True in list(transferform.data.values()):
        print('yaay')
        user.credit -= int(transferform.sum.data)
        beneficary = User.query.filter(User.id == transferform.data["beneficary"]).first()
        beneficary.credit += int(transferform.sum.data)
        setattr(user, 'lastchange', datetime.utcnow())
        addUserRecord = Transaction(credit=int(transferform.sum.data) * -1, userid=user_id, date=datetime.utcnow())
        setattr(beneficary, 'lastchange', datetime.utcnow())
        addBeneficaryRecord = Transaction(credit=transferform.sum.data, userid=transferform.data["beneficary"], date=datetime.utcnow())
        db.session.add(addUserRecord)
        db.session.add(addBeneficaryRecord)
        db.session.commit()
        return redirect(url_for('user.userpage', user_id=user_id))


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
    return render_template('user.html', title=user.username, user=user, transaction=transaction, transferform=transferform, item=item, edit=edit, negcredit=negcredit, poscredit=poscredit)


@user.route("/user/<int:user_id>/<string:sign>/<int:new_credit>", methods=['Post', 'Get'])
def addcredits(user_id, sign, new_credit):
    usr = User.query.get_or_404(user_id)
    if '-' in sign:
        new_credit = new_credit * -1
    usr.credit += new_credit
    trans = Transaction(credit=new_credit, userid=user_id, date=datetime.utcnow())
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('user.userpage', user_id=user_id))


@user.route("/user/<int:user_id>/<int:item_id>", methods=['Post', 'Get'])
def buyitem(user_id, item_id):
    usr = User.query.get_or_404(user_id)
    item = Item.query.get_or_404(item_id)
    usr.credit -= item.price
    trans = Transaction(credit=item.price * -1, userid=user_id, date=datetime.utcnow())
    db.session.add(trans)
    db.session.commit()
    return redirect(url_for('user.userpage', user_id=user_id))



