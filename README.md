# MiniSatUI
Web interface for MiniSat.

MiniSat is a centralize web interface to provision virtual machine and run docker container on remote hosts.

### How to run MiniSatUI
- Create your python3 virtual enviroment
```sh
python -m venv <enviroment_name>
```
- Activate virtual enviroment
```sh
source <enviroment_name>/bin/activate
```
- Install dependency using pip
```sh
pip install -r requirements.txt
```
- Run django web app
```sh
python3 manage.py runserver 
```
