Installation
============

**System Requirements**

+ 64-bit Architecture
+ A minimum of 250GB storage and 4GB memory
+ Developed and tested on Fedora 27

**Prerequisites**

+ All system should have Libvirt API installed for virtual machine provisioning.

.. code-block:: console

    # dnf install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install -y


+ All compute resources should have Docker installed for running Docker containers. To install Docker on Fedora  `follow <https://docs.docker.com/install/linux/docker-ce/fedora/#install-using-the-repository>`_

+ Server should have Docker machine installed.

.. code-block:: console

    # curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && sudo install /tmp/docker-machine /usr/local/bin/docker-machine


+ Server should have SSH public key or it can be generated using SSH keygen.

.. code-block:: console

    # ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P ""


**Installation**

*From Docker*

To containerize Minisat, first clone the Github Minisat repository using and go to directory Minisat

.. code-block:: console

    # git clone https://github.com/miniSat/minisat.git
    # cd Minisat

Build docker image using

.. code-block:: console

    # docker build -t minisat:latest .

After building the image now run the image using

.. code-block:: console

    # docker container run -it -p 8000:8000 minisat:latest 0.0.0.0:8000

Head to http://localhost:8000 for Minisat

*From Source code*

Minisat uses Django web framework which can be installed in  Python 3 virtual environment. To create Python 3 virtual environment

.. code-block:: console

    # python3 -m venv <environment_name>


After that we need to activate the virtual environment by executing

.. code-block:: console

    # source <environment_name>/bin/activate


Now clone the Github Minisat repository from

.. code-block:: console

    # git clone https://github.com/miniSat/minisat.git


Minisat requires some Python modules like Django (version 2.0).  We can install them by executing

.. code-block:: console

    # pip install -r requirements.txt


Django `ORM <https://docs.djangoproject.com/en/2.0/topics/db/>`_ is used to create database.

.. code-block:: console
    
    # python manage.py makemigrations

Above command will create a Python script which will contain all SQL queries that we need to create the schema of database. The migration files are stored at ``.../satellite/migrations/``.

.. code-block:: console

    # python manage.py migrate

It will create a database and execute the SQL queries in Python script. Minisat, uses `SQLite <https://www.sqlite.org/index.html>`_ database to store values.

Now our environment is ready to run Minisat server. To start server

.. code-block:: console

    # python manage.py runserver

By default, Django server is running at http://localhost:8000.

If you encounter below error

.. code-block:: console

    # Error: That port is already in use.


Try changing the port number while running the server

.. code-block:: console

    # python manage.py runserver <port_number>

