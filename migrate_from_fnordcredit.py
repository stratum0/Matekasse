from matekasse import create_app, db
from matekasse.models import User, Transaction
import sqlite3
import argparse

parser = argparse.ArgumentParser(allow_abbrev=False)
parser.add_argument("-p", "--path", action='store', type=str, required=True, help="Path to fnordcredit database")
inp = parser.parse_args()


app = create_app()
ctx = app.app_context()
ctx.push()

try:
    conn = sqlite3.connect(inp.path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user')
    rows = cursor.fetchall()
    for r in rows:
        user = r[5]
        credit = r[1] * 100
        newuser = User(username=user, credit=credit)
        db.session.add(newuser)
    '''cursor.execute('SELECT * FROM transaction')
    rows = cursor.fetchall()
    for r in rows:
        user = r[5]
        trans = r[2] * 100
        newtrans = Transaction(userid=user, credit=trans)
        db.session.add(newtrans)'''
    db.session.commit()
except sqlite3.Error as error:
    print(error)
finally:
    if conn:
        conn.close()
        print('Migration complete')
ctx.pop()
exit()
