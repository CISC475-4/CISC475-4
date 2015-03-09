#!/usr/bin/env bash

apt-get update

sudo apt-get -y install make vim

# Install Python (if we want a newer version than 2.7.3)
# /vagrant/config/vagrant_scripts/install_python.sh/Users/mhoffman/Documents/serenity_software/giving_shared 

# Install pip
sudo apt-get -y install python-setuptools
sudo easy_install pip

# Install Pyside and dependencies
# /vagrant/config/vagrant_scripts/install_pyside.sh
sudo apt-get install -y python-pyside

# Install pip packages
sudo pip install -r /vagrant/config/requirements.txt

# Install vagrant GUI stuff (http://stackoverflow.com/questions/18878117/)
sudo echo "allowed_users=anybody" > /etc/X11/Xwrapper.config
sudo apt-get install -y xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
sudo VBoxClient-all

# to run the GUI
#   login as vagrant user.  (User: vagrant Password: vagrant)
#   $ sudo startxfce4&
