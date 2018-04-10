"""
dashboard_details fetch data from remote compute system and virtual machine to display on
dashboard
"""

import os
from . import vm_manage as vm_funcs


def update_vm_file():
    for file in os.listdir("/tmp/Minisat/vm/"):
        file = "/tmp/Minisat/vm/" + file
        with open(file) as fi:
            data = fi.readlines()
            name = data[1][:-1]
            compute_ip = data[3]
            if vm_funcs.vm_ip(name, compute_ip) != '-':
                os.remove(file)


def get_vms(ip_list=[]):
    """Get list of virtual machine and their details from remote compute resources

    :param ip_list: list of IP address of remote compute resources

    :returns final_dict: Contain details of all the virtual machine on all compute
    """
    update_vm()
    final_dict = {}
    error = []
    count = 0
    for tuple in ip_list:
        ip = tuple[2]
        if vm_funcs.isOnline(ip):
            vm_list = os.popen(
                "virsh -c qemu+ssh://root@" +
                ip +
                "/system list --all").readlines()

            for vm in range(2, len(vm_list) - 1):
                vm_names = vm_list[vm].split()
                vm_details = os.popen(
                    "virsh -c qemu+ssh://root@" +
                    ip +
                    "/system dominfo " +
                    vm_names[1]).readlines()
                key = vm_details[2].split()
                vm_det = []
                vm_det.append(key[1])
                vm_name = vm_details[1].split()
                vm_det.append(vm_name[1])
                vm_status = vm_details[4].split()
                vm_det.append(vm_status[1])
                vm_det.append(tuple[1])
                vm_det.append(ip)

                if vm_det[2] == 'running':
                    vm_det[2] = vm_funcs.get_status(vm_det[3], vm_det[4], vm_det[1])

                final_dict[count] = vm_det
                count = count + 1
        else:
            error.append(tuple[1])
    # file create
    for file in os.listdir("/tmp/Minisat/vm/"):
        file = "/tmp/Minisat/vm/" + file
        vm_det = []
        with open(file) as fi:
            data = fi.readlines()
            print(data)
            vm_det.append(data[0][:-1])
            vm_det.append(data[1][:-1])
            vm_det.append(data[2][:-1])
            vm_det.append("")
            vm_det.append("")
            final_dict[count] = vm_det
            count += 1

    if len(error):
        final_dict['error'] = error
    return final_dict


def running_containers(compute=[]):
    """Get list of virtual machine and their details from remote compute resources

    :param compute: list of IP address of remote compute resources

    :returns data: Contain details of all the container on all compute
    """
    data = {}
    error = []
    data['error'] = ""
    i = 0
    for tuple in compute:
        if vm_funcs.isOnline(tuple[2]):
            cont_list = os.popen(
                "docker-machine ssh " +
                tuple[1] +
                " docker container ls").readlines()
            for j in range(1, len(cont_list)):
                li = cont_list[j].split()
                newli = []
                if not li[-2].endswith('/tcp'):
                    li[-2] = "No Port Assigned"
                if '(Paused)' in li:
                    newli.extend([li[-1], li[1], li[-2], tuple[1], "Paused", li[0], tuple[2]])
                else:
                    newli.extend([li[-1], li[1], li[-2], tuple[1], "Running", li[0], tuple[2]])
                data[i] = newli
                i = i + 1
        else:
            error.append(tuple[1])
    if len(error):
        data['error'] = error
    return data
