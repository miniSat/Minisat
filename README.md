# Minisat
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg)
![travis-ci](https://travis-ci.org/miniSat/Minisat.svg?branch=master)

Minisat is a centralizes web interface, built on [Django framework](https://www.djangoproject.com/start/overview/), to provision virtual machines and run Docker containers on remote hosts.

### Dependencies
- Install QEMU and libvirt packages
```sh
$ sudo dnf install qemu-kvm qemu-img libvirt libvirt-python libvirt-client virt-install -y
```

- Create ssh public key
```sh
$ ssh-keygen -q -t rsa -f ~/.ssh/id_rsa -N ""
```

- Install docker-machine
```sh
$ curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine && sudo install /tmp/docker-machine /usr/local/bin/docker-machine
```

### How to run Minisat
- Create your python3 virtual environment
```sh
$ python3 -m venv <environment_name>
```
- Activate virtual environment
```sh
$ source <environment_name>/bin/activate
```
- Install dependency using pip
```sh
$ pip install -r requirements.txt
```
- Run migrations
```sh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
- Run django web app
```sh
$ python3 manage.py runserver
```
### Containerize Minisat
- Build Docker image
```sh
$ cd Minisat/
$ docker build -t minisat:latest .
```
- Run the image
```sh
$ docker container run -it -p 8000:8000 minisat:latest 0.0.0.0:8000
```
- Head to http://localhost:8000 for Minisat UI

### Create test environment
All Minisat pull requests are tested in [Travis-ci](https://travis-ci.org/miniSat/minisat). If tests fail, visit the test job that failed to view its console output.

Run these same tests locally using selenium. Download [selenium](http://www.seleniumhq.org/) webdriver for mozilla firefox. [mozilla geckodriver](https://github.com/mozilla/geckodriver/releases).

Extract the driver.
Export path
```sh
$ export PATH=$PATH/:/path/of/driver
```
It will set a path variable to the webdriver.

And run the test
```sh
$ pytest
```

## Licensing
Minisat is licensed under GNU General Public License v3.0. See [LICENSE](https://github.com/miniSat/minisat/blob/master/LICENSE/)
