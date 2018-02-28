import os
import time
from satellite.models import (
    Product_model,
    Activation_model,
    View_model,
    Create_host_model
)


def vm_create(compute_ip, name, ram, cpus, disk_size, location_url, kickstart_loc):
    final_cmd = 'virt-install --connect qemu+ssh://root@' + compute_ip + '/system --name ' + name + ' --ram ' + str(
        ram) + ' --vcpus ' + str(
        cpus) + ' --disk path=/var/lib/libvirt/images/' + name + '.qcow2,bus=virtio,size=' + str(
        disk_size) + ' --location ' + location_url + ' --extra-args=\'ks=' + kickstart_loc + \
        ' ksdevice=ens3\' --network bridge:virbr0 > /dev/null 2>&1 &'
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


def virsh_delete_vm(vm_name, com_ip):
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system shutdown " + str(vm_name)
    cmd2 = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system undefine " + str(vm_name)
    os.system(cmd)
    delete_vm_flag = os.system(cmd2)
    time.sleep(6)
    return delete_vm_flag


def vm_ip(vm_name, compute_ip):
    response = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domiflist " + vm_name).readlines()
    vm_mac = response[2].split(" ")[-1]
    try:
        response = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system net-dhcp-leases default | grep " + vm_mac).readlines()
        if len(response) > 1:
            for each in range(len(response)):
                vm_ipaddress = response[each].split()[4]
                if isOnline(vm_ipaddress):
                    break
        else:
            vm_ipaddress = response[0].split()[4]
    except:
        vm_ipaddress = '-'
    return vm_ipaddress


def vm_details(compute_ip, vm_id):
    details = {}
    details["Id"] = vm_id
    vm_name = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domname " + vm_id).readline()
    details["Name"] = vm_name[:-1]
    vm_state = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domstate " + vm_id).readline()
    details["State"] = vm_state[:-1]
    try:
        vm_allocated_mem = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system dommemstat " + vm_id).readlines()
        details["Total Allocated Memory"] = str(int(int(vm_allocated_mem[0].split()[1]) / 1024)) + " MB"
        details["Free Memory"] = str(int(int(vm_allocated_mem[-2].split()[1]) / 1024)) + " MB"
        vm_cpu = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system dominfo " + vm_id).readlines()
        details["Virtual CPUs"] = vm_cpu[5].split()[1]
    except IndexError:
        details["Total Allocated Memory"] = "-"
        details["Free Memory"] = "-"
        details["Virtual CPUs"] = '-'
    details["IP Address"] = vm_ip(details["Name"], compute_ip)
    list = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domiflist " + vm_id).readlines()[2].split()
    vm_mac = list[4]
    details["MAC Address"] = vm_mac
    return details


def get_packages(compute_ip, vm_ip, root_passwd):
    vm_ip = vm_ip.split("/")[0]
    package_info = os.popen("ssh root@" + compute_ip + " 'sshpass -p " + root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " rpm -qa'").readlines()
    package_info = package_info[2:]
    return package_info


def get_repo(activation_name):
    repo = {}
    product = []
    view_list = list(Activation_model.objects.filter(activation_name=activation_name).values_list())
    for each in view_list:
        product_list = list(View_model.objects.filter(view_name=each[2]).values_list())
        for every in product_list:
            product.append(list(Product_model.objects.filter(product_name=every[2]).values_list()))
    for each in product:
        if each[0][1] in repo:
            pass
        else:
            repo[each[0][1]] = each[0][2]
    return repo


def get_status(compute_name, compute_ip, vm_name):
    try:
        root_passwd = Create_host_model.objects.filter(select_compute=compute_name, vm_name=vm_name).values_list()[0][6]
    except IndexError:
        return "Unable to fetch data"
    vm_ipaddress = vm_ip(vm_name, compute_ip).split("/")[0]
    cmd = "ssh root@" + compute_ip + " sshpass -p " + root_passwd + " ssh root@" + vm_ipaddress + " hostname"
    response = os.system(cmd)
    if response == 0:
        return "running"
    elif response == 65280:
        return "initializing"


# TO get chart details
def get_chart_details(allocated_mem, free_mem):
    chartdetail = {}
    chartdetail["allocated"] = int(allocated_mem.split('M')[0])
    chartdetail["free_mem"] = int(free_mem.split('M')[0])
    chartdetail["used_memory"] = chartdetail["allocated"] - chartdetail["free_mem"]
    return chartdetail
