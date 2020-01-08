#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx
adduser matekasse --system --gecos "Matekasse,,," --shell /bin/bash

/bin/su -c "git clone -b installer https://github.com/stratum0/Matekasse.git" - matekasse

python3 /home/matekasse/Matekasse/installfoo/genconfig.py
chown matekasse:nogroup /var/lib/matekasse
/bin/su -c "~/Matekasse/installfoo/matekasse_user.sh" - matekasse

cp /home/matekasse/Matekasse/installfoo/matekasse.service /etc/systemd/system/
systemctl start matekasse
systemctl enable matekasse

cp /home/matekasse/Matekasse/installfoo/matekasse /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/matekasse /etc/nginx/sites-enabled
FILE=/etc/nginx/sites-enabled/default
if [ -f "$FILE" ]; then
    rm $FILE
fi
systemctl restart nginx
/bin/su -c "rm -rf ~/Matekasse/installfoo/" - matekasse