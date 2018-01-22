import os


def vm_create(compute_ip, name, ram, cpus, disk_size, location_url, kickstart_location):
    final_cmd = 'virt-install --connect qemu+ssh://root@' + compute_ip + '/system --name ' + name + ' --ram '
    + str(ram) + ' --vcpus ' + str(cpus) + ' --disk path=/var/lib/libvirt/images/' + name + '.qcow2,bus=virtio,size=' \
    + str(disk_size) + ' --location ' + location_url + ' --extra-args=\'ks=' + kickstart_location \
    + ' ksdevice=ens3\' --network bridge:virbr0 > /dev/null 2>&1 &'
    print(final_cmd)
    response = os.system(final_cmd)
    if response == 0:
        return True
    else:
        return False


def isOnline(host):
    response = os.system("ping -c 2 " + host + " > /dev/null 2>&1 &")
    if response == 0:
        print("online")
    else:
        print("offline")
