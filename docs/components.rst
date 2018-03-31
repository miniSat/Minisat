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


Host
----

Minisat is host-based virtualization in which one can have access and control over virtual machine from single server.

++++++++++++++++
Operating System
++++++++++++++++

Operating System is the most important program which runs on computer. You can use any linux based operating system for your virtual machine.
For our simplicity we have set-up the server where we have rsync the mirros of Fedora 25, Fedora 26 and so on.
You can use any mirror of linux based operating system.

* Add new

    Here you have to fill up two fields

    * Operating System Name

    The name can be anything you want to give but good practice is giving actual name of operating system which will give the exact idea of Virtual machine OS.

    * Location

    Here you have to provide the location from where it will fetch the operating system.

* Already Existing

    All the operating systems you have added while be visible in this section.

+++++++++++
Create Host
+++++++++++

In this user have to fill various details such as

* Name
* Compute Resource
* Profile
* Operating System
* Activation Name
* Host Group
* Root Password

Except Name and Root Password user have to select other details from drop down as they are created earlier.

If you Have already created **Host Group** then you have to only enter

* Name
* Host Group
* Root Password

All the remaining fields are filled automatically.


Content
-------

+++++++
Product
+++++++

The user has to give a name to the package and URL from where that package is going to be fetched.
It has two fields **Add New** and **View Existing**.

++++
View
++++

View is a layer of abstraction where we can encapsulate two or more products into a single view.
Products added by user will be visible here and user has to give name to the view and select the product of it's choice from the list.

++++++++++++++
Activation Key
++++++++++++++

Activation key is a top layer abstraction. Two or more views are encapsualted under single **Activation Key**.
This is important as it is required at the stage of creating host.

.. note ::

	All the above three have **validation**. No name should be repeated.


