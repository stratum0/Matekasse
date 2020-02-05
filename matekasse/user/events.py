from flask_socketio import emit
from datetime import datetime
from matekasse import db
from matekasse import socketio
from matekasse.models import User, Transaction, Item, Credits


@socketio.on('credit', namespace='/user')
def credit(data):
    usr = User.query.get_or_404(data.get('userid'))
    usr.credit += data.get('creditvalue')
    usr.lastchange = datetime.utcnow()
    trans = Transaction(credit=data.get('creditvalue'), userid=data.get('userid'), date=datetime.utcnow())
    db.session.add(trans)
    db.session.commit()
    socketio.emit('newcredit', {'userid': usr.id, 'credit': usr.credit}, broadcast=True, namespace='/user')
    socketio.emit('newusercredit', {'userid': usr.id, 'credit': usr.credit}, broadcast=True, namespace='/home')


@socketio.on('buyitem', namespace='/user')
def buyitem(data):
    print(data)
    usr = User.query.get_or_404(data.get('userid'))
    item = Item.query.get_or_404(data.get('itemid'))
    usr.credit -= item.price
    usr.lastchange = datetime.utcnow()
    trans = Transaction(credit=item.price * -1, userid=usr.id, date=datetime.utcnow())
    db.session.add(trans)
    db.session.commit()
    socketio.emit('newcredit', {'userid': usr.id, 'credit': usr.credit}, broadcast=True, namespace='/user')
    socketio.emit('newusercredit', {'userid': usr.id, 'credit': usr.credit}, broadcast=True, namespace='/home')


@socketio.on('transfer', namespace='/user')
def transfer(data):
    user = User.query.get_or_404(data.get('userid'))
    user.credit -= int(data.get('sum'))
    beneficary = User.query.filter(User.id == data.get('beneficary')).first()
    beneficary.credit += int(data.get('sum'))
    setattr(user, 'lastchange', datetime.utcnow())
    addUserRecord = Transaction(credit=int(data.get('sum')) * -1, userid=user.id, date=datetime.utcnow())
    setattr(beneficary, 'lastchange', datetime.utcnow())
    addBeneficaryRecord = Transaction(credit=int(data.get('sum')), userid=beneficary.id, date=datetime.utcnow())
    db.session.add(addUserRecord)
    db.session.add(addBeneficaryRecord)
    db.session.commit()
    socketio.emit('newcredit', {'userid': user.id, 'credit': user.credit}, broadcast=True, namespace='/user')
    socketio.emit('newusercredit', {'userid': user.id, 'credit': user.credit}, broadcast=True, namespace='/home')
    socketio.emit('newcredit', {'userid': beneficary.id, 'credit': beneficary.credit}, broadcast=True, namespace='/user')
    socketio.emit('newusercredit', {'userid': beneficary.id, 'credit': beneficary.credit}, broadcast=True, namespace='/home')
