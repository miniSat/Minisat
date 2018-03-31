import os
import time
import re
from satellite.models import (
    Product_model,
    Activation_model,
    View_model,
    Create_host_model
)


def vm_create(compute_ip, name, ram, cpus, disk_size, location_url, kickstart_loc):
    """Create virtual machine on remote system

    :param compute_ip: Remote system IP address
    :param name: Name of virtual machine
    :param ram: RAM size for virtual machine
    :param cpus: Number of virtual CPUS for virtual machine
    :param disk_size: Disk size for virtual machine
    :param location_url: URL location of OS
    :param kickstart_loc: location of kickstart

    :return: Boolean, True if success or False
    """
    kickstart_name = kickstart_loc.split('/')[-1]
    final_cmd = 'virt-install --connect qemu+ssh://root@' + compute_ip + '/system --name ' + name + ' --ram ' + str(
        ram) + ' --vcpus ' + str(cpus) + ' --disk path=/var/lib/libvirt/images/' + name + '.qcow2,bus=virtio,size=' \
        + str(disk_size) + ' --location ' + location_url + ' --initrd-inject=' + kickstart_loc + \
        ' --extra-args=\'ks=file:/' + kickstart_name + ' ksdevice=ens3\' --network bridge:virbr0 > /dev/null 2>&1 &'
    response = os.system(final_cmd)
    if response == 0:
        return True
    else:
        return False


def isOnline(host):
    """Check whether host is online or offline

    :param host: IP of remote system

    :returns: True if online else False
    """
    response = os.system("ping -c 1 " + host + ">/dev/null 2>&1")
    if response == 0:
        return True
    else:
        return False


def virsh_start_vm(vm_name, com_ip):
    """Starts the virtual machine on remote system
    :param vm_name: Name of virtual machine
    :param com_ip: Compute IP on which virtual machine is running

    :return: start_vm_flag
    """
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system start " + str(vm_name)
    start_vm_flag = os.system(cmd)
    time.sleep(6)
    return start_vm_flag


def virsh_pause_vm(vm_name, com_ip):
    """Shutdown the virtual machine on remote system
    :param vm_name: Name of virtual machine
    :param com_ip: Compute IP on which virtual machine is running

    :return: shut_vm_flag
    """
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system shutdown " + str(vm_name)
    shut_vm_flag = os.system(cmd)
    time.sleep(6)
    return shut_vm_flag


def virsh_delete_vm(vm_name, com_ip):
    """Delete the virtual machine on remote system

    :param vm_name: Name of virtual machine
    :param com_ip: Compute IP on which virtual machine is running

    :return: delete_vm_flag
    """
    cmd = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system shutdown " + str(vm_name)
    cmd2 = "virsh -c qemu+ssh://root@" + str(com_ip) + "/system undefine " + str(vm_name)
    os.system(cmd)
    delete_vm_flag = os.system(cmd2)
    os.system("ssh root@" + com_ip + " rm -f /var/lib/libvirt/images/" + vm_name + ".qcow2")
    time.sleep(6)
    return delete_vm_flag


def vm_ip(vm_name, compute_ip):
    """Find the IP address of virtual machine

    :param vm_name: Name of virtual machine
    :param compute_ip: Compute IP on which virtual machine is running

    :return vm_ipaddress: contain IP address of virtual machine
    """
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


def get_memory(compute_ip, vm_name, vm_ip):
    """Find memory consumption of virtual machine

    :param compute_ip: Compute IP on which virtual machine is running
    :param vm_name: Name of virtual machine
    :param vm_ip: IP address of virtual machine

    :return total_mem: Total memory of virtual machine
    :return free_mem: Free memory of virtual machine
    """
    vm_ip = vm_ip.split("/")[0]
    root_passwd = Create_host_model.objects.filter(vm_name=vm_name).values_list()[0][6]
    cmd = "ssh root@" + str(compute_ip) + " 'sshpass -p " + str(root_passwd) + " ssh -o StrictHostKeyChecking=no root@" + str(vm_ip) + " free'"
    memory = os.popen(cmd).readlines()
    memory = memory[1].split()
    total_mem, free_mem = memory[1], memory[2]
    free_mem = int(total_mem) - int(free_mem)
    total_mem = str(int(int(total_mem) / 1024)) + " MB "
    free_mem = str(int(int(free_mem) / 1024)) + " MB "
    return total_mem, free_mem


def vm_details(compute_name, compute_ip, vm_id):
    """Find details of virtual machine

    In this function virtual machine details like ID, name, state(Running or shut),
    virtual CPUs, Total memory allocated, Free memory, virtual machine IP address, virtual machine MAC address,
    Compute name (on which it is provisioned).

    :param compute_name: Name of compute on which virtual machine is running
    :param compute_ip: IP address of compute on which virtual machine is running
    :param vm_id: UUID of virtual machine

    :return details: Dictionary of ID, name, state(Running or shut),
    virtual CPUS, Total memory allocated, Free memory, virtual machine IP address, virtual machine MAC address,
    Compute name
    """
    details = {}
    details["Id"] = vm_id
    vm_name = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domname " + vm_id).readline()
    details["Name"] = vm_name[:-1]
    vm_state = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domstate " + vm_id).readline()
    details["State"] = vm_state[:-1]
    VM_ip = vm_ip(details["Name"], compute_ip)
    try:
        details["Total Allocated Memory"], details["Free Memory"] = get_memory(compute_ip, details["Name"], VM_ip)
        vm_cpu = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system dominfo " + vm_id).readlines()
        details["Virtual CPUs"] = vm_cpu[5].split()[1]
    except IndexError:
        details["Total Allocated Memory"] = "-"
        details["Free Memory"] = "-"
        details["Virtual CPUs"] = '-'
    details["IP Address"] = VM_ip
    list = os.popen("virsh -c qemu+ssh://root@" + compute_ip + "/system domiflist " + vm_id).readlines()[2].split()
    vm_mac = list[4]
    details["MAC Address"] = vm_mac
    details["Compute Resource"] = compute_name + ' (' + compute_ip + ')'
    return details


def get_packages(compute_ip, vm_ip, root_passwd):
    """Get packages installed in virtual machine

    :param compute_ip: IP address of compute on which virtual machine  is running
    :param vm_ip: IP address of virtual machine
    :param root_passwd: Root password of virtual machine

    :return package_info: List of all packages in virtual machine
    """
    vm_ip = vm_ip.split("/")[0]
    package_info = os.popen("ssh root@" + compute_ip + " 'sshpass -p " + root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " rpm -qa'").readlines()
    package_info = package_info[2:]
    return package_info


def get_repo(activation_name):
    """Get repo list included in Activation name

    :param activation_name: Name of activation

    :return repo: Dictionary of repo name and repo URL included in that activation
    """
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
    """Get status of virtual machine

    :param compute_name: Name of compute on which virtual machine is running
    :param compute_ip: Compute IP on which virtual machine is running
    :param vm_name: Name of virtual machine

    :return: Running or Initializing
    """
    try:
        root_passwd = Create_host_model.objects.filter(select_compute=compute_name, vm_name=vm_name).values_list()[0][6]
    except IndexError:
        return "running"
    vm_ipaddress = vm_ip(vm_name, compute_ip).split("/")[0]
    cmd = "ssh root@" + compute_ip + " sshpass -p " + root_passwd + " ssh root@" + vm_ipaddress + " hostname"
    ping = "ssh root@" + compute_ip + " ping -c 2 " + vm_ipaddress
    ping_response = os.system(ping)
    response = os.system(cmd)
    if response == 0 or ping_response == 0:
        return "running"
    elif response == 65280:
        return "initializing"


def filter_repo(repo_info):
    """Filter the repos

    Remove all unnecessary data from repos

    :param repo_info: Raw repo data

    :return repo_info: Cleaned repo data
    """
    repo_info = [x for x in repo_info if not x.startswith('Last')]
    repo_info = [x for x in repo_info if not x.startswith('repo')]
    repo_info = [x.split(None, 1) for x in repo_info]
    repo_info = [x for x in repo_info if x]
    return repo_info


def get_vm_repo(compute_ip, vm_ip, vm_name):
    """Get virtual machine repo

    Find repo added in virtual machine and its status whether its enable or disable

    :param compute_ip: IP address of compute on which virual machine is running
    :param vm_ip: IP address of virtual machine
    :param vm_name: Name of virtual machine

    :return repo_info: Contain of list of enabled and disabled repo
    """
    vm_root_passwd = Create_host_model.objects.filter(vm_name=vm_name).values_list()[0][6]
    cmd = "ssh root@" + compute_ip + " 'sshpass -p " + vm_root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " dnf repolist enabled -y'"
    repo_info = os.popen(cmd).readlines()
    enabled_repos = filter_repo(repo_info)
    enabled_repo_id = [each.pop(0) for each in enabled_repos]
    for i in range(len(enabled_repo_id)):
        if enabled_repo_id[i].startswith('*'):
            enabled_repo_id[i] = enabled_repo_id[i][1:]
        else:
            pass
    enabled_repo_name = [each.pop() for each in enabled_repos]

    cmd = "ssh root@" + compute_ip + " 'sshpass -p " + vm_root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " dnf repolist disabled -y'"
    repo_info = os.popen(cmd).readlines()
    disabled_repos = filter_repo(repo_info)
    disabled_repo_name = [each.pop() for each in disabled_repos]
    disabled_repo_id = [each.pop(0) for each in disabled_repos]
    for i in range(len(disabled_repo_id)):
        if disabled_repo_id[i].startswith('*'):
            disabled_repo_id[i] = disabled_repo_id[i][1:]
        else:
            pass
    enabled_repos = []
    disbaled_repos = []
    enabled_repo_dict = {}
    disabled_repo_dict = {}
    for each in enabled_repo_name:
        li = re.split(r'\s{3}', each)
        li = [x for x in li if x]
        li = [x.strip() for x in li]
        enabled_repos.append(li)
    enabled_repo_dict = dict(zip(enabled_repo_id, enabled_repos))
    for each in disabled_repo_name:
        li = []
        li.append(each.split('\n')[0].strip())
        disbaled_repos.append(li)
    disabled_repo_dict = dict(zip(disabled_repo_id, disbaled_repos))
    repo_info = {}
    repo_info["enabled"] = enabled_repo_dict
    repo_info["disabled"] = disabled_repo_dict
    return repo_info


def vm_status(compute_ip, vm_name, vm_ip):
    """Get status of virtual machine

    :param compute_ip: Compute IP on which virtual machine is running
    :param vm_name: Name of virtual machine
    :param vm_ip: IP address of virtual machine

    :return: Running or Initializing or Shutdown
    """
    status = {}
    compute_ip = compute_ip.replace('-', '.')
    vm_ip = vm_ip.replace('-', '.')
    vm_root_passwd = Create_host_model.objects.filter(vm_name=vm_name).values_list()[0][6]
    if os.system("ssh root@" + compute_ip + " ping -c 2 " + vm_ip) == 0:
        if os.system("ssh root@" + compute_ip + " 'sshpass -p " + vm_root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " hostname'") == 0:
            status["status"] = "running"
        else:
            status["status"] = "initializing"
    else:
        status["status"] = "shutdown"
    return status


def change_repo(compute_ip, vm_ip, repo_id, repo_flag, vm_name):
    """Change the repo status

    :param compute_ip: IP address of compute on which virtual machine is running
    :param vm_ip: IP address of virtual machine
    :param repo_id: repo ID
    :param repo_flag: flag of repo (enable or disable)
    :param vm_name: Name of virtual machine

    :return : success or failed
    """
    compute_ip = compute_ip.replace('-', '.')
    vm_ip = vm_ip.replace('-', '.')
    vm_root_passwd = Create_host_model.objects.filter(vm_name=vm_name).values_list()[0][6]
    if repo_flag == "enable":
        cmd = "ssh root@" + compute_ip + " 'sshpass -p " + vm_root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " dnf config-manager --set-enabled " + repo_id + " -y'"
        res = os.system(cmd)
        if not res:
            return "success"
        else:
            return "failed"
    elif repo_flag == "disable":
        cmd = "ssh root@" + compute_ip + " 'sshpass -p " + vm_root_passwd + " ssh -o StrictHostKeyChecking=no root@" + vm_ip + " dnf config-manager --set-disabled " + repo_id + " -y'"
        res = os.system(cmd)
        if not res:
            return "success"
        else:
            return "failed"
