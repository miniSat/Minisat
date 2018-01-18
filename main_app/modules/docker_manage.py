import os


def make_connection(ip_address, name):
    add_docker_machine = "docker-machine create --driver generic --generic-ip-address " + ip_address + \
                         " --generic-ssh-user root --generic-ssh-key ~/.ssh/id_rsa " + name + " > /dev/null 2>&1 &"
    # print(add_docker_machine)
    result = os.system(add_docker_machine)

    if result == 0:
        return True
    else:
        return False
