import os
import time


def make_connection(ip_address, name):
    add_docker_machine = "docker-machine create --driver generic --generic-ip-address " + ip_address + \
                         " --generic-ssh-user root --generic-ssh-key ~/.ssh/id_rsa " + name + " > /dev/null 2>&1 &"
    result = os.system(add_docker_machine)

    if result == 0:
        return "True"
    else:
        return "False"


def get_docker_images(compute=[]):
    name = compute[0][1]
    images_list = []
    get_images = os.popen("docker-machine ssh " + name + " docker images").readlines()
    count = 0
    docker_dict = {}
    for i in range(1, len(get_images)):
        images = get_images[i].split()
        images_list.extend([images[2], images[0], images[1], images[3] + " " + images[4] + " " + images[5], images[6]])
        docker_dict[count] = images_list
        images_list = []
        count = count + 1
    return docker_dict


def run_cont(new_cont, stat):
    if stat == "on":
        stat_cmd = " -t "
    else:
        stat_cmd = ""

    if new_cont.host_port != "" or new_cont.cont_port != "":
        port_cmd = "-p " + new_cont.host_port + ":" + new_cont.cont_port + " "
    else:
        port_cmd = ""

    if new_cont.tag_name != "":
        tag_cmd = new_cont.image_name + ":" + new_cont.tag_name + " "
    else:
        tag_cmd = " " + new_cont.image_name + ":latest "

    if new_cont.container_name != "":
        cont_cmd = " --name " + new_cont.container_name + " "
    else:
        cont_cmd = ""

    create_cont = "docker-machine ssh " + new_cont.select_compute + " docker container run -d " + stat_cmd + port_cmd + cont_cmd + tag_cmd + " > /dev/null 2>&1 &"
    os.system(create_cont)


def start_cont(cont_name, compute_name):
    start_cmd = "docker-machine ssh " + compute_name + " docker unpause " + cont_name
    cont_response = os.system(start_cmd)
    time.sleep(4)
    if cont_response == 0:
        return "Paused"
    elif cont_response == 256:
        return 0


def stop_cont(cont_name, compute_name):
    start_cmd = "docker-machine ssh " + compute_name + " docker pause " + cont_name
    cont_response = os.popen(start_cmd)
    time.sleep(4)
    if cont_response == 0:
        return "Running"
    elif cont_response == 256:
        return 0


def destroy_cont(cont_name, compute_name):
    stop_cmd = "docker-machine ssh " + compute_name + " docker container rm -f " + cont_name
    cont_response = os.popen(stop_cmd)
    time.sleep(4)
    if cont_response == 0:
        return "Destroyed"
    else:
        return 0
