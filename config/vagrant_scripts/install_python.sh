#!/usr/bin/env bash

# Install Python
wget http://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
tar xfz Python-2.7.9.tgz
cd Python-2.7.9
./Configure
make
sudo make install
alias python="/usr/local/bin/python"
cd ..
rm -rf Python-2.7.9
rm Python-2.7.9.tgz
