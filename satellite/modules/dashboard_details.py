import os
from . import vm_manage as vm_funcs


def get_vms(ip_list=[]):
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
    if len(error):
        final_dict['error'] = error
    return final_dict


def running_containers(compute=[]):
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
    # print(data)
    return data
