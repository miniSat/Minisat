Installation
============

**System Requirements**

+ 64-bit Architecture
+ A minimum 250GB storage and 4GB memory
+ Developed and tested on Fedora 27

**Pre-requisites**

+ All system should have Libvirt API installed for VM provisioning.

::

    dnf install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install -y


+ All compute resources should have Docker installed for running Docker containers. To install Docker on Fedora  `follow <https://docs.docker.com/install/linux/docker-ce/fedora/#install-using-the-repository>`_

+ Server should have Docker machine installed.

::

    curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && sudo install /tmp/docker-machine /usr/local/bin/docker-machine


+ Server should have SSH public key or it can be generated using SSH keygen.

::

    ssh-keygen


**Installation**

*From Docker*

To run Minisat using docker, first clone the Github Minisat repository using and go to directory Minisat
::

    git clone https://github.com/miniSat/minisat.git
    cd Minisat

Now build docker image for Minisat using
::

    docker build -t minisat:latest .

Hang on building docker image may take time depending on your internet speed.

After building the image now run the image using
::

    docker container run -it -p 8000:8000 minisat:latest 0.0.0.0:8000

Head to http://localhost:8000 for Minisat

*From Source code*

Minisat uses Django web framework which can be installed in  Python 3 virtual environment. To create Python 3 virtual environment
::

    python3 -m venv <environment_name>


After that we need to activate the virtual environment by executing
::

    source <environment_name>/bin/activate


Now clone the Github Minisat repository from
::

    git clone https://github.com/miniSat/minisat.git


Minisat requires some Python modules like Django (version 2.0).  We can install them by executing
::

    pip install -r requirements.txt


Django `ORM <https://docs.djangoproject.com/en/2.0/topics/db/>`_ is used to create database.
::
    
    python manage.py makemigrations

Above command will create a Python script which will contain all SQL queries that we need to create the schema of database. The migration files are stored at ``.../satellite/migrations/``.
::

    python manage.py migrate

It will create a database and execute the SQL queries in Python script. Minisat, uses `SQLite <https://www.sqlite.org/index.html>`_ database to store values.

Now our environment is ready to run Minisat server. To start server
::

    python manage.py runserver

By default, Django server is running at http://localhost:8000.

If you encounter below error

::

    Error: That port is already in use.


Try changing the port number while running the server

::

    python manage.py runserver <port_number>

