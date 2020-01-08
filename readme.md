# Matekasse
## How to install
1. `wget https://raw.githubusercontent.com/stratum0/Matekasse/installer/install.sh`
2. `chmod +x install.sh`
3. `sudo ./install.sh`

## Migrate from Fnord_Credit
1. `sudo -i`
2. `su - matekasse`
3. `cd Matekasse`
4. `source venv/bin/activate`
5. `python migrate_from_fnordcredit.py -p <Path_to_Fnordcredit_db>`
6. `deactivate`