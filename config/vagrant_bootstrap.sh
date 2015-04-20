#!/usr/bin/env bash

# dictionaries-common causes some errors upon first boot. If we remove it now,
# the apt-get upgrade should reinstall a working version. This also uninstalls
# the miscfiles package, which will be reinstalled as needed by anything
# upgraded or installed through the following apt-get commands.
sudo apt-get remove dictionaries-common

# Update the packages list to its newest version and upgrade all the packages
sudo apt-get -y update
sudo apt-get -y upgrade

# Install Python (if we want a newer version than 2.7.3)
# /vagrant/config/vagrant_scripts/install_python.sh/Users/mhoffman/Documents/serenity_software/giving_shared 

# Install all needed packages available from the repo
packages=(
	"make"                    # GNU build system
	"vim"                     # Convenient text editing
	"python-setuptools"       
	"python-pip"              # Python dependency installations
	"python-pyside"           # Brandon's visualization
	"xfce4"                   # Vagrant box GUI
	"virtualbox-guest-dkms"   # These are needed by VirtualBox
	"virtualbox-guest-utils"  # They're used to do things like
	"virtualbox-guest-x11"    # set the screen resolution.
)

for pkg in "${packages[@]}"; do 
	sudo apt-get -y install "$pkg"
done

# Install packages available via Pip
sudo pip install -r /vagrant/config/requirements.txt

# Install vagrant GUI stuff (http://stackoverflow.com/questions/18878117/)
sudo echo "allowed_users=anybody" > /etc/X11/Xwrapper.config

# to run the GUI
#   login as vagrant user.  (User: vagrant Password: vagrant)
#   $ sudo startxfce4&

# To run Vagrant from Linux, first make sure your vboxdrv kernel modules are
# currently enabled:
#   # modprobe vboxdrv
