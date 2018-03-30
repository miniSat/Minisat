Components
==========

Everything which is required to provision a virtual machine or docker container are wrapped under a term called components.
Read further for complete details.

Infrastructure
--------------
This includes information regarding hardware availability of remote machine.

++++++++++++++++
Compute Resource
++++++++++++++++

Compute Resource is very first step in provisioning virtual machines and runnig Docker containers.

+ Create New

    Firstly you have to create your own compute resource it will ask three fields

    - Compute resource Name.
    - IP Address of remote machine.
    - The **root** password of the remote machine.


    .. note::
	
  	  All the above details are very much essential to set up a compute resource



+ View Existing

    If you have already setup the compute resource earlier you can check it in "View Existing" section. It displays all the available compute resource list.

Compute Resource has various validation such as
- Unique name should be given to each compute resource.
- IP should be valid, reachable and sshd service should be running.
- Root password should be entered correctly.


++++++++
Profiles
++++++++

Profile allows user to set various essential parameters to create a virtual machine. A profile holds values for RAM, disk space and number of virtual CPUs.

+ Create New

    After creating compute resource one has to create profile which has fields as

    - Profile Name
    - RAM(in MB)
    - VCPUs
    - Disk Space(in GB)
+ View Existing

    Previously created profile are visible under this section. You can use same profile multiple times.
    
    .. note :: 
	    
	 Just use correct profile name which will give  correct idea about all the other details include with it.

