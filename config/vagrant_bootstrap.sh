#!/usr/bin/env bash

# This is supposed to fix the dictionaries-common errors we're getting
sudo /usr/share/debconf/fix_db.pl

# Update the packages list to its newest version and upgrade all the packages
sudo apt-get -y {update,upgrade,autoremove}

# Install all needed packages available from the repo
packages=(
	"make"                    # GNU build system
	"python-setuptools"       
	"python-dev"              # Dependency for graph analysis libraries
	"python-pip"              # Python dependency installations
	"python-matplotlib"       # Matplotlib and a bunch of related libraries
	"python-pyside"           # Brandon's visualization
	"vim"                     # Convenient text editing
	"virtualbox-guest-dkms"   # These are needed by VirtualBox
	"virtualbox-guest-utils"  # They're used to do things like
	"virtualbox-guest-x11"    # set the screen resolution.
	"xfce4"                   # Vagrant box GUI
)

for pkg in "${packages[@]}"; do 
	sudo apt-get -y install "$pkg"
done

# Install packages available via Pip
sudo pip install -r /vagrant/config/requirements.txt

# Normally only root can start xfce. This allows anyone to start it.
sudo echo "allowed_users=anybody" > /etc/X11/Xwrapper.config

# This execs xfce when you log into the terminal.
echo "exec startxfce4" > ~/.xinitrc
# This doesn't actually work, so I'm not sure what it's supposed to do.
#sudo VBoxClient-all

# to run the GUI
#   login as vagrant user.  (User: vagrant Password: vagrant)
#   $ sudo startxfce4&

# To run Vagrant from Linux, first make sure your vboxdrv kernel modules are
# currently enabled:
#   # modprobe vboxdrv
