"""
This file is to make connection with newly added compute resources
"""

import os


def copy_ssh_id(ip_address, password):
    """Copy SSH key with remote system

    :param ip_address: IP address of remote system (Compute resource)
    :param password: Root password of remote system

    :return: True
    """
    make_ssh = "sshpass -p " + password + " ssh-copy-id -o StrictHostKeyChecking=no root@" + ip_address
    os.system(make_ssh)
    return "True"


def make_connection(ip_address, password):
    """Check the compute is reachable and password is correct or not

    :param ip_address: IP address of remote system (Compute resource)
    :param password: Root password of remote system

    :return: calls the copy_ssh_id(ip_address, password) to copy SSH key else error
    """
    copy_id = "sshpass -p " + password + " ssh -o StrictHostKeyChecking=no root@" + ip_address + " hostname"
    copy_id_status = os.system(copy_id)
    if copy_id_status == 0:
        return copy_ssh_id(ip_address, password)
    elif copy_id_status == 1280:
        return "Root password incorrect"
    elif copy_id_status == 65280:
        return "Ip Address Unreachable"
