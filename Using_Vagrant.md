#Using Vagrant

1. Have [vagrant](https://www.vagrantup.com/downloads.html 'Download link') 
   installed on your machine. 

    **Note**: If you're running Ubuntu or another Debian-based distribution of
    Linux, you likely won't have a recent enough version of Vagrant available
    through your system's repositories. If this applies to you, install the
    current version from 
    [Vagrant's download page](https://www.vagrantup.com/downloads). (Version
    1.5.* is enough; the current version is 1.7. The current version of Vagrant
    in the Debian/Ubuntu repositories is 1.4.3.) To install the file you
    downloaded, double-click it or run `# dpkg -i <file>`.

2. Go to the repository directory (where this file and the `Vagrantfile` 
   are located). Your Vagrant box won't be able to boot if you're not in this
   directory.   

3. Make sure you have VirtualBox installed, then run `vagrant up`. Wait for 
   command line to be available again.  A GUI should have popped up.  

    **Note**: If VirtualBox shuts down the VM shortly after creating the
    GUI window, try starting the VM directly from the VirtualBox GUI and
    Googling the error. More often than not it will be that virtualization is
    disabled in your BIOS.

4. Login to the shell presented in the GUI  
        `user: vagrant`  
        `password: vagrant`  

    **Note**: You can also just `$ vagrant ssh` if you don't need the GUI. 
    Vagrant uses ssh keys in your computer's `~/.vagrant.d/` directory
    (which it creates and manages) to automatically log you into the 
    box without requiring a password.

5. In the GUI shell, run `sudo startxfce4 &`  

6. An actual GUI should appear, from here you can access the repository in 
   `/vagrant` because it's a shared folder of the project  

To save state of the VM, use `vagrant suspend`  
To destroy the VM, use `vagrant destroy`  
To start, or restart the VM from suspend, use `vagrant up`  
(I'm not sure of this) To update the VM when new stuff is added, use 
`vagrant reload --provision`   

If you're using Linux, you'll have to make sure your VirtualBox kernel 
module is enabled:
        # modprobe vboxdrv
