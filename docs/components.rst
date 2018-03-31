Components
==========

Everything which is required to provision a virtual machine or Docker container are wrapped under components.
Read further for complete details.

Infrastructure
--------------
Infrastructure is a remote system which uses libvirt API and QEMU hypervisor installed.

++++++++++++++++
Compute Resource
++++++++++++++++

Compute Resource is the very first step in provisioning virtual machines and running Docker containers.

+ Create New

    Initially we need to add compute which includes following parameters

    - Compute resource Name.
    - IP Address of remote machine.
    - The **root** password of the remote machine.


    .. note::
	
  	  All the above details are very much essential to set up a compute resource



+ View Existing

    If you have already set-up the compute resource earlier you can check it in "View Existing" section. It displays all the available compute resource list.

Compute Resource has various validation such as

	- A unique name should be given to each compute resource.
	- IP should be valid, reachable and sshd service should be running.
	- Root password should be entered correctly.


++++++++
Profiles
++++++++

Profile allows user to set various essential parameters to create a virtual machine. A profile holds values for RAM, disk space and number of virtual CPUs.

+ Create New

    After creating compute resource one has to create profile which has fields as

    - Profile Name
    - RAM (in MB)
    - Virtual CPUs
    - Disk Space (in GB)
+ View Existing

    Previously created profiles are visible under this section. You can use same profile multiple times.
    
    .. note :: 
	    
	Use meaningful profile name which will give the correct idea about all the other details included with it.	 

