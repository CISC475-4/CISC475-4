#!/bin/bash

# Changes output color temporarily
function status_msg () 
{
    color="\e[0;35m" # purple
    end="\e[0m"      # regular
    echo -e "$color$1$cend"
}

# If this is the first time this machine is being brought up, do the
# installation stuff.
if [[ ! -f /var/log/vagrant_installed ]]; then
    status_msg ":::"
    status_msg "::: This is the first time you've booted this machine!"
    status_msg "::: Installing necessary software..."
    status_msg ":::"

    # Fix the problem with dictionaries-common and install xfce/etc.
    status_msg ":: Attempting to fix dictionaries-common problem..."
    sudo /usr/share/debconf/fix_db.pl
    sudo apt-get -y install dictionaries-common
    sudo dpkg-reconfigure -f noninteractive dictionaries-common

    # If that command failed, don't bother continuing.
    if [[ $? -ne 0 ]]; then
        status_msg "::: Failed to update dictionaries-common. Aborting" 
	exit 1
    fi

    # Update the list of packages known by apt and upgrade all the packages
    status_msg ":: Updating APT..."
    sudo apt-get -u update
    sudo apt-get -y upgrade
    sudo apt-get -y autoremove

    # Don't add the virtualbox-guest-* packages; they'll come later.
    packages=(
        "make"                    # GNU build system
        "python-setuptools"       # These should be moved to pip eventually...
        "python-dev"              # Dependency for graph analysis libraries
        "python-pip"              # Python dependency installations
        "python-matplotlib"       # Matplotlib and a bunch of related libraries
        "python-pyside"           # Brandon's visualization
        "vim"                     # Convenient text editing
    )        

    for pkg in "${packages[@]}"; do
        status_msg ":: Installing $pkg..."
	sudo apt-get -y install "$pkg"
    done

    # Install Python dependencies available via Pip
    status_msg ":: Installing Pyton Pip dependencies"
    sudo pip install -r /vagrant/config/requirements.txt


    status_msg ":: Installing virtualbox-guest-*..."
    sudo apt-get -y install virtualbox-guest-{utils,x11,dkms}
    status_msg ":: Installing xfce4..."
    sudo apt-get -y install xubuntu-desktop #xfce4 xfce4-session xinit

    # Normally only root can start xfce. This allows anyone to start it.
    sudo sed -i 's/^allowed_users=.*/allowed_users=anybody/' /etc/X11/XWrapper.config
    # If XWrapper.config didn't exist, the previous command would do nothing.
    if [[ ! "$(grep 'allowed_users=anybody' /etc/X11/XWrapper.config)" ]]; then
	# If that's the case, we have to create it.
        sudo echo "allowed_users=anybody" > /etc/X11/XWrapper.config
    fi

    status_msg ":: Completing installation..."
    sudo touch /var/log/vagrant_installed

    status_msg "::: Need to reboot for software installation to complete!"
    sudo reboot
else
    status_msg "Installation has already been performed. Setting up GUI..."
fi

status_msg "::: Starting xfce4 GUI"
cd ~
/usr/bin/startxfce4 &
sleep 6

