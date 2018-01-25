import os


def get_vms(ip_list=[]):
    vm_dict = {}
    for tuple in ip_list:
        ip = tuple[2]
        vm_list = os.popen("virsh -c qemu+ssh://"+ip+"/system list --all").readlines()
        for vm in range(2, len(vm_list)-1):
            vm_names = vm_list[vm].split()
            vm_details = os.popen("virsh -c qemu+ssh://"+ip+"/system dominfo "+vm_names[1]).readlines()
            key = vm_details[2].split()
            print(vm_details)
            vm_det = []
            vm_name = vm_details[1].split()
            vm_det.append(vm_name[1])
            vm_status = vm_details[4].split()
            vm_det.append(vm_status[1])
            vm_det.append(tuple[1])
            vm_dict[key[1][:8]] = vm_det

    return vm_dict



