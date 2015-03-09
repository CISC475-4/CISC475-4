#!/usr/bin/env bash

# Install dependencies
sudo apt-get -y install build-essential git cmake libqt4-dev libphonon-dev python2.7-dev libxml2-dev libxslt1-dev qtmobility-dev

wget https://bootstrap.pypa.io/get-pip.py
sudo python2.7 get-pip.py

sudo pip2.7 install wheel

# Building PySide distribution
wget https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz

tar -xvzf PySide-1.2.2.tar.gz

cd PySide-1.2.2

python2.7 setup.py bdist_wheel --qmake=/usr/bin/qmake-qt4

# Installing PySide Distribution
DIST=$(ls dist)
sudo pip2.7 install dist/"$(DIST)"

#Clean up
cd ..
