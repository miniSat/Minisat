import os


def get_vms(ip_list=[]):
    final_dict = {}
    count = 0
    # final_vms = []
    for tuple in ip_list:
        ip = tuple[2]
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
            # final_vms.append(vm_det)
            final_dict[count] = vm_det
            count = count + 1
    return final_dict


def running_containers(compute=[]):
    data = {}
    i = 0
    # print(compute)
    for tuple in compute:
        cont_list = os.popen(
            "docker-machine ssh " +
            tuple[1] +
            " docker container ls").readlines()
        for j in range(1, len(cont_list)):
            li = cont_list[j].split()
            newli = []
            newli.extend([li[13], li[1], li[12], tuple[1],
                          "Up " + li[10] + " hours ago"])
            data[li[0]] = newli
            i = i + 1
    print(data)
    return data
