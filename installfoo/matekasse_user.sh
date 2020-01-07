cd Matekasse
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
python ./installfoo/gendb.py
deactivate