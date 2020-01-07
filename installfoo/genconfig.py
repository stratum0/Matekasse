#!/usr/bin/env python3
import hashlib
import os
import json

# Create secret key
pw = os.urandom(32)
hsh = hashlib.sha256(pw)

# Create config stuff
matekasse_path = '/etc/matekasse'
if not os.path.exists(matekasse_path):
    os.makedirs(matekasse_path)
filepath = os.path.join(matekasse_path, 'config.json')

db_path = '/var/lib/matekasse'
if not os.path.exists(db_path):
    os.makedirs(db_path)

data = {"SECRET_KEY": "" + hsh.hexdigest() + "", "SQLALCHEMY_DATABASE_URI": "sqlite:////" + db_path + "/site.db"}

with open(filepath, 'w') as file:
    json.dump(data, file)
