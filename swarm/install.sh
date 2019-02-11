#! /bin/bash

sudo addgroup --system docker
sudo adduser $(whoami) docker
#maybe need to enable/disable
sudo snap install docker
sudo ln -s /snap/bin/docker /usr/bin/docker
sudo snap disable docker
