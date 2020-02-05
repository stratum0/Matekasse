from datetime import datetime

from flask import render_template, flash, redirect, url_for
from matekasse import db
from matekasse.user.forms import RegistrationForm, Transfer, Edit
from matekasse.models import User, Transaction, Item, Credits
from matekasse.user import user


@user.route("/register", methods=['Post', 'Get'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        usr = User(username=form.username.data, lastchange=datetime.utcnow())
        db.session.add(usr)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@user.route("/user/<int:user_id>", methods=['Post', 'Get'])
def userpage(user_id):
    # Check User
    usr = User.query.get_or_404(user_id)

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

    # Item foo
    item = Item.query.all()
    if edit.validate_on_submit() and True in list(edit.data.values()):
        if edit.delete.data:
            db.session.query(Transaction).filter(Transaction.userid == user_id).delete()
            db.session.delete(usr)
        if edit.edit.data:
            usr.username = edit.rename.data
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('user.html', title=usr.username, user=usr, transaction=transaction, transferform=transferform, item=item, edit=edit, negcredit=negcredit, poscredit=poscredit)






