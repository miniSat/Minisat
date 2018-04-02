Usage
=====

Creating Virtual Machines
-------------------------

Follow the steps carefully so that you dont get any error while creating virtual machine. The steps are very easy only need is to follow them in order.

++++++
Step 1
++++++

First you need to create compute resource.

To do so click on Infrastructure -> Compute Resource

* Fill all the details
* Make sure there is no repeatation of name, remote system is reachable from your system and root password is correct.
* All the fields have validation.

++++++
Step 2
++++++

Once done with compute resource move to profiles.

Click on Infrastructure -> Profile

* Name your Profile, fill the fields of RAM, VCPUS and Disk Space
* Name should not get repeated.

Once you click *Submit* Profile gets added to database and is visible in **View Existing** Section.

++++++
Step 3
++++++

Now, you have to add Packages for you Virtual machine.

* Click on Content -> Product

	Enter the name of package and give URL from where it should fetch the package repository.

* Click on Content -> View

	Enter the name for View and select the product from the list avialable. You can select one or more products to encapsulate into single View.

* Click on Content -> Activation key

	Here enter the name for your activation key and select one or more Views of your desire.

.. note::

	Activation is very essential at time of creating host.

++++++
Step 4
++++++

The next thing that comes into picture is Host Group.
If you want to use same compute, profile, operating system and activation key again and again then *host group* plays vital role.

Click Host Group -> Host Group

* Name the host group as per convenience.
* Select Compute Resource, Profile, Operating System and Activation key from their *drop down* respectively.

Once you create host group its entry is inserted in database and can be visible under **View Existing** section.

.. note::

	Host Group is optional but important at time of eliminating repeatation.

++++++
Step 5
++++++

This is the final step of provisioning the virtual machine on remote machine.

Click Host -> Create Host

- Here you have to provide the name to host.

- Select all the fields of your requirement.

- You will notice that when you select *host group* here fields such as compute, profile, operating system and activation key are filled automatically.

- At the end you have to provide **root** password for your Virtual Machine.

Finally, just hit the ``Create Instance`` button and your Virtual Machine deployment starts at background.



Running Docker containers
-------------------------

run Docker cont
