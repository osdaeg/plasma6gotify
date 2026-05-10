#!/bin/bash

mkdir -p ~/scripts/

cd ~/scripts/

git clone https://github.com/osdaeg/plasma6gotify.git

mv plasma6gotify gotify_notify

cd gotify_notify

mv gotify_notify.env.example gotify_notify.env
mv gotify.service.example gotify.service

sed -i "s/usuario/$USER/g" gotify.service

mkdir -p ~/.config/systemd/user
cp gotify.service ~/.config/systemd/user/gotify.service

pip install websocket-client python-dotenv --break-system-packages

systemctl --user daemon-reload
systemctl --user enable gotify.service
#systemctl --user start gotify.service

echo "==============================================================================="
echo "|  Tenés que editar el archivo gotify_notify.env para modificar las variables |"
echo "|  GOTIFY_URL y GOTIFY_TOKEN con los valores correctos                        |"
echo "|  y luego ejecutar systemctl --user start gotify.service                     |" 
echo "==============================================================================="