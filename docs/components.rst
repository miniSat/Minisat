Components
==========

Everything which is required to provision a virtual machine and Docker container are wrapped under components.
Read further for complete details.

Infrastructure
--------------
Infrastructure is a remote system which uses libvirt API and QEMU hypervisor installed.

++++++++++++++++
Compute Resource
++++++++++++++++

Compute Resource is the very first step in provisioning virtual machines and running Docker containers.

+ Create New

    Initially, add compute resource which includes following parameters

    - Compute resource Name.
    - IP Address of remote machine.
    - The **root** password of the remote machine.


.. note::
	
  	  All the above details are very much essential to set up a compute resource.



+ View Existing

    Once a compute resource is added, it is enlisted under **View Existing** section.

Compute Resource has various validations such as

	- A unique name should be given to each compute resource.
	- IP address should be valid, reachable and sshd service on compute resource should be running.
	- Root password should be entered correctly.


++++++++
Profiles
++++++++

Profile allows user to set various essential parameters to create a virtual machine. A profile holds values for RAM, disk space and number of virtual CPUs.

+ Create New

    The following parameters are asked to add a profile

    - Profile Name
    - RAM (in MB)
    - Virtual CPUs
    - Disk Space (in GB)
+ View Existing

    Previously created profiles are visible under this section. Same profile can be used multiple times.
    
    .. note :: 
	    
	Use appropiate profile name which will give the correct idea about all the other details included with it.	 


Host
----

Minisat is host-based virtualization in which one can have access and control over virtual machine from single server.

++++++++++++++++
Operating System
++++++++++++++++

Operating System is the most important program which runs on computer. Any distribution of Linux can be used as guest operating system for the virtual machine.
Operating system url from mirrors of `Fedora <https://admin.fedoraproject.org/mirrormanager/>`_, `CentOS <https://www.centos.org/download/mirrors/>`_ can be added. 
Else, use a tool called rsync to fetch the operating system tree, host these files on a local HTTP server and provide the local url in location field. The latter method will be more reliable and quicker to provision virtual machines.

* Create new

    Fill the two fields

    * Operating System Name

    Name of the operating system which will give the exact idea of the guest operating system.

    * Location

    Provide the location from where the server can fetch the operating system tree.

* Already Existing

    All existing operating systems are enlisted under this section.

+++++++++++
Create Host
+++++++++++

To provision a virtual machine the following parameters need to filled, some are optional though

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

All the remaining fields are filled according to the selected host group.


Content
-------

+++++++
Product
+++++++

While provisioning a virtual machine, packages can be added to a virtual machine. A single repository is identified under the term **Product**.

* Create New

    Consists of two fields

    * Product Name
        * The repository will be recognized with the product name instead of the repository URL.
        * Mapping a repository URL to a name, makes identifying a repository URL with the help of product name easy.
    * Product URL
        * The location from where the repository for a package can be added.
    
    .. note ::
        A single product name will hold only one URL of a repository not more than that.
    
* View Existing

    All existing products are enlisted here along with their repository URL.

++++
View
++++

A single view consists of multiple products along with their corresponding repository URLs. 

* Create New

    Consists of 

        * View Name 
            * Multiple products will be recognized with a single name, **View Name**.
            * If a view is selected, all the underlying products consisted in that view are added. 

        * Select Products
            * To create a view, one or more products can be selected.
            * The view will now consist of the selected products.

* View Existing

    All existing view are enlisted here along with the  included products and their corresponding repository URLs.

++++++++++++++
Activation Key
++++++++++++++

A single activation key consists of multiple views, and each of these views will consist of multiple products.
**Activation Key**, **View**, **Product** exhibit a hierarchy, **Product** being at the top, followed by **View**, and **Activation Key** being at the bottom.
The hierarchical structure allows the server to inherit views from activation key and products from view.

Create New

* Consists of

    * Activation Name
        * Multiple views are bundled inside a single activation key along with the products that they consist of.
        * If an activation key is selected, all the underlying views along with products consisted in that view are added.

    * Select View
        * To create an activation key, one or more views can be selected.
        * The key will now consist of the selected views.

* View Existing

    All existing activation keys are enlisted here along with the multiple views and products that they consist of.

Containers
----------

**Containerization** is a solution to reliable sofware delivery. They offer better consistency between testing environments and production environment.
Deployment of application with containers is perfect for `microservices <http://microservices.io/>`_ approach. 


For now, Minisat can run Docker containers only. Support for other
kind of containers like `LXC <https://linuxcontainers.org/>`_ , `CoreOS's rkt <https://coreos.com/rkt/>`_  will soon be added.

+++++++++++++
New Container
+++++++++++++

- Docker image name and tag name is to be known before running it on any compute resource.
- Container is assigned a name so as to identify it on the dashboard.
- Host port and container port are mapped to each other which makes services running inside container accessible from outside.
- If image is not available  on the selected compute resource, then it is pulled from Docker registry and then run accordingly.

++++++++++++
Local Images
++++++++++++

- Docker images available on remote compute resources are displayed with details such as **Image Name & Tag**, **Image ID**, **Created**, **Size**.
- Any new image found on any compute resource will be enlisted here.




