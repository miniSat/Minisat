Overview
========

`Minisat <https://github.com/miniSat/minisat>`_ is an open source provisioning, managing and monitoring tool for virtual machines and `Docker <https://www.docker.com/>`_ containers, built on `Django Web Framework <https://www.djangoproject.com/>`_. 

It offers a web interface for the user to interact with, which helps in easy manipulation of virtual machines and containers.

Features
--------

* Current state (Running, Initializing, Shutdown) of virtual machines and containers.
* A dashboard to toggle the current state of virtual machines and containers.
* Virtual machine provisioning with a kickstart which makes the installation of the guest operating system uninteractive.
* Mapping the container port to the host port making the service available outside the container.

Virtualization API 
------------------

* Minisat uses `Libvirt API <https://libvirt.org/>`_, which is a toolkit to manage virtualization hosts. The bindings for this API are available in C, Python, Perl, Java.
* Supports provisioning on many hypervisors like  KVM, QEMU, Xen, Virtuozzo, VMWare ESX, LXC, BHyve and more.
* Minisat provisions virtual machines on a remote QEMU hypervisor.
* The facts of virtual machines are gathered using command line tools provided by Libvirt API.