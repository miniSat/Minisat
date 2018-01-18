import os


def make_connection(ip_address, password):
    copy_id = "sshpass -p " + password + " ssh -o StrictHostKeyChecking=no root@" + ip_address + " hostname"
    copy_id_status = os.system(copy_id)
    if copy_id_status == 0:
        return copy_ssh_id(ip_address, password)
    elif copy_id_status == 1280:
        return "Root password incorrect"
    elif copy_id_status == 65280:
        return "Ip Address Unreachable"


def copy_ssh_id(ip_address, password):
    make_ssh = "sshpass -p " + password + " ssh-copy-id -o StrictHostKeyChecking=no root@" + ip_address
    os.system(make_ssh)
    return True
