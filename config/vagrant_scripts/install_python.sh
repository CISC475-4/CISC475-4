#!/usr/bin/env bash

# Install Python
# Download the compressed installation files
wget http://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
# Expand the downloaded file
tar xzf Python-2.7.9.tgz
# Change directories to the decompressed directory
cd Python-2.7.9
# Run a script to configure the installation for this machine
./configure
# Local compilation and assembly
make
# Compilation and assembly specifically for system-wide use.
sudo make install

# This works, but only for one user
#alias python="/usr/local/bin/python"
# This changes the symbolic link to the default version of Python for all users
sudo ln -sf /usr/bin/python /usr/local/bin/python2.7

cd ..
rm -rf Python-2.7.9
rm Python-2.7.9.tgz
