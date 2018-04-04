Usage
=====

Creating Virtual Machines
-------------------------

Follow the steps to provisioning virtual machine. 

++++++
Step 1
++++++

First create compute resource.

To do so click on Infrastructure -> Compute Resource

* Fill all the details
* Make sure there is no repetition of name, compute resource is reachable from Minisat server and root password should be correct.
* All the fields have validation.

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

Now, add Packages for the Virtual machine.

* Click on Content -> Product

	Enter the name of package and give URL from where it should fetch the package repository.

* Click on Content -> View

	Enter the name for View and select the product from the list avialable. Select one or more products to encapsulate into single View.

* Click on Content -> Activation key

	Here enter the name for activation key and select one or more Views as per requirment.

.. note::
	
	Adding packages is optional. If required then only follow **Step 3** else skip it.


++++++
Step 4
++++++

The next thing that comes into picture is Host Group.
To use same compute, profile, operating system and activation key frequently then *host group* plays vital role.

Click Host Group -> Host Group

* Name the host group as per convenience.
* Select Compute Resource, Profile, Operating System and Activation key from their *drop down* respectively.

Once host group is created its entry is inserted in database and will be enlisted under **View Existing** section.

.. note::

	Host Group is optional but important at time of eliminating repetition.

++++++
Step 5
++++++

This is the final step of provisioning the virtual machine on remote machine.

Click Host -> Create Host

- Here provide name to host.

- Select all the fields which are required.

- Selecting *host group* will fill the fields such as compute, profile, operating system and activation key automatically.

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

To do so click on Infrastructure -> Compute Resource

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


