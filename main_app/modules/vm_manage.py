import os
import time


def vm_create(compute_ip, name, ram, cpus, disk_size, location_url, kickstart_loc):
    final_cmd = 'virt-install --connect qemu+ssh://root@' + compute_ip + '/system --name ' + name + ' --ram ' + str(
        ram) + ' --vcpus ' + str(
        cpus) + ' --disk path=/var/lib/libvirt/images/' + name + '.qcow2,bus=virtio,size=' + str(
        disk_size) + ' --location ' + location_url + ' --extra-args=\'ks=' + kickstart_loc + \
        ' ksdevice=ens3\' --network bridge:virbr0 > /dev/null 2>&1 &'
    print(final_cmd)
    response = os.system(final_cmd)
    if response == 0:
        return True
    else:
        return False


def isOnline(host):
    response = os.system("ping -c 1 " + host + ">/dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False


def virsh_start_vm(vm_name, com_ip):
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system start " + str(vm_name)
    start_vm_flag = os.system(cmd)
    time.sleep(6)
    return start_vm_flag


def virsh_pause_vm(vm_name, com_ip):
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system shutdown " + str(vm_name)
    shut_vm_flag = os.system(cmd)
    time.sleep(6)
    return shut_vm_flag
