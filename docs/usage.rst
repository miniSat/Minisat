Usage
=====

Creating Virtual Machines
-------------------------

Follow the steps to provision a virtual machine. 

++++++
Step 1
++++++

First create compute resource by clicking on Infrastructure -> Compute Resource.

* Fill all the details
* Make sure there is no repetition of compute name, compute resource is reachable by Minisat server and root password should be correct.

++++++
Step 2
++++++

Once done with compute resource move to profiles.

Click on Infrastructure -> Profile

* Name the Profile, fill the fields of RAM, virtual CPUs and Disk Space.
* Name should not get repeated.

Click *Submit* Profile gets added to database and is enlisted in **View Existing** Section.

++++++
Step 3
++++++

Now, add Packages for the virtual machine.

* Click on Content -> Product

	Enter the name of *Product* and URL from where it should fetch the package repository.

* Click on Content -> View

	Enter the name for *View* and select the product from the list avialable. Select one or more products to encapsulate them into single *View*.

* Click on Content -> Activation key

	Here enter the name for activation key and select one or more *View* as per requirement.

.. note::
	
	Adding packages is optional. If required then only follow **Step 3** else skip it.


++++++
Step 4
++++++

The next thing that comes into picture is Host Group.
To make use of the same compute resources, profiles, operating systems and activation keys frequently, they can be bundled together under a single unit called *Host Group*.

Click Host Group -> Host Group

* Name the *Host Group*.
* Select Compute Resource, Profile, Operating System and Activation key from their respective drop down options.

Once a *Host Group* is created, a virtual machine is provisioned with less efforts as selecting a host group populates the other
parameters necessary to provision a virtual machine.

.. note::

	*Host Group* are advantageous when multiple virtual machines are to provisioned with little or no changes in their specifications. 

++++++
Step 5
++++++

This is the final step of provisioning a virtual machine on remote machine.

Click Host -> Create Host

- Name the virtual machine so as to identify it on the dashboard.

- Selecting *Host Group* will populate the fields such as compute, profile, operating system and activation key according to the values the *Host Group* consists of.

.. note::
	
	Choosing `host group` and `activation key` is optional.


- At the end provide **root** password for the virtual machine.

Finally, just hit the ``Create Instance`` button and virtual machine deployment starts at background.



Running Docker containers
-------------------------

Docker containers are created either from existing local images or by pulling images from Docker registry and then running them.

++++++
Step 1
++++++

First create compute resource.

Click on Infrastructure -> Compute Resource

* Fill all the details
* Make sure there is no current existance of name and IP address in database.
* Also see to it that compute resource is reachable to Minisat server and root password is correct.
* As there is validation for the above.

.. note::

	If a compute for virtual machine is added no need to add it again, same compute can be used for containers also.


++++++
Step 2
++++++

The previous step will now allow the server to perform SSH on remote Docker server and gather container related facts.

To deploy a Docker container on a compute resource

* Enter name for container
* Enter the Docker image and tag name
* Provide the host port and container port
* Select compute resource
* To run containers in background select the *checkbox* provided there.

++++++
Step 3
++++++

Finally hit ``Run`` to run image.

Check running containers on dashboard under Docker containers tab.


