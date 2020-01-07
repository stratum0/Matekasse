import sys
import os

sys.path.append(os.getcwd())

from matekasse import create_app, db
from matekasse.models import Credits

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
exit()
