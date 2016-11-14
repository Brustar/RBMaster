#!/bin/bash

cd ~
git clone https://github.com/Brustar/RBMaster.git

sudo cp ~/RBMaster/ecloud /etc/init.d/ecloud
sudo chmod +x /etc/init.d/ecloud
sudo service ecloud start
sudo update-rc.d ecloud defaults

sudo reboot
