#!/usr/bin/env python3
import hashlib
import string
import os
from matekasse import create_app, db

print('Write secret key')
rndchrctrs = string.ascii_letters + string.punctuation + string.digits
pw = os.urandom(32)
hsh = hashlib.sha256(pw)
with open('./matekasse/config.py', 'a') as sk:
    sk.write('    SECRET_KEY = \'' + hsh.hexdigest() + '\'\n')

print('Create DB')
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
exit()

#TODO
# Config to json in /opt/matekasse/
# group matekasse
# berechtigung 640
# if os.getuid() != 0:
#    print('Need root priviliges...')
#    exit()

