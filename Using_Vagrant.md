Using Vagrant:

1. Have [vagrant](https://www.vagrantup.com/downloads.html 'Download link') 
   installed on your machine. 
2. Go to the repository directory (where this file and the `Vagrantfile` 
   are located)   
3. Make sure you have VirtualBox installed, then run `vagrant up`. Wait for 
   command line to be available again.  A GUI should have popped up.  
4. Login to the shell presented in the GUI  
   `user: vagrant    
   password: vagrant`    
5. In the GUI shell, run `sudo startxfce4 &`  
6. An actual GUI should appear, from here you can access the repository in 
   `/vagrant` because it's a shared folder of the project  

To save state of the VM, use `vagrant suspend`  
To destroy the VM, use `vagrant destroy`  
To start, or restart the VM from suspend, use `vagrant up`  
(I'm not sure of this) To update the VM when new stuff is added, use 
`vagrant reload --provision`   
