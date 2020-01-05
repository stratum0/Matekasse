#!/usr/bin/env python3
import hashlib
import os
import pwd
import json


if os.getuid() != 0:
    print('Need root priviliges...')
    exit()

print('- - - - Write secret key - - - -')
# Create secret key
pw = os.urandom(32)
hsh = hashlib.sha256(pw)

# Create config stuff
matekasse_path = '/etc/matekasse'
if not os.path.exists(matekasse_path):
    os.makedirs(matekasse_path)
filepath = os.path.join(matekasse_path, 'config.json')

# TODO
# change matekasse DB to a better place...
# db_path = "/var/lib/matekasse"
# if not os.path.exists(db_path):
#    os.makedirs(db_path)

data = {"SECRET_KEY": "" + hsh.hexdigest() + "", "SQLALCHEMY_DATABASE_URI": "sqlite:///site.db"}

with open(filepath, 'w') as file:
    json.dump(data, file)

# Create DB
from matekasse import create_app, db
from matekasse.models import Credits

print('- - - - Create DB - - - -')
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
crts = Credits()
pos = [False, True]
sums = [50, 100, 150, 200, 300, 400, 500, 1000, 2000, 5000]
for p in pos:
    for s in sums:
        newcredit = Credits(credit=s, pos=p)
        db.session.add(newcredit)
db.session.commit()
ctx.pop()

current_user = os.getlogin()
db_path = "./matekasse/site.db"
# Change user and group from db...
os.chown(db_path, pwd.getpwnam(os.getlogin()).pw_uid, pwd.getpwnam(os.getlogin()).pw_gid)
exit()

