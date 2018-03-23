import os


def get_compute_details(ip_address):
    compute_details = {}
    memory_details = os.popen('ssh root@' + ip_address + ' free -m').readlines()
    ram_details = memory_details[1].split()
    tmp_dict = {}
    tmp_dict['total'], tmp_dict['used'] = int(ram_details[1]), int(ram_details[2])
    tmp_dict['ram-percent-used'] = float(str(round(float(ram_details[2]) / float(ram_details[1]) * 100, 2)))
    compute_details['ram'] = tmp_dict
    used_disk_details = os.popen('ssh root@' + ip_address + ' du -b --si /var/lib/libvirt/images/').readlines()
    tmp_dict = {}
    tmp_dict['used'] = used_disk_details[0].split()[0]

    if tmp_dict['used'].endswith('k'):
        tmp_dict['used'] = float(str(round(float(tmp_dict['used'][:-1]) / 1024, 2)))
    elif tmp_dict['used'].endswith('G'):
        tmp_dict['used'] = float(tmp_dict['used'][:-1])

    avai_disk_details = os.popen('ssh root@' + ip_address + ' df -ah /').readlines()
    tmp_dict['free'] = avai_disk_details[1].split()[3]
    if tmp_dict['free'].endswith('G'):
        tmp_dict['free'] = float(tmp_dict['free'][:-1])
    compute_details['disk'] = tmp_dict
    compute_details['disk-percent-use'] = round(float(tmp_dict['used']) / float(tmp_dict['free']) * 100, 2)
    return compute_details
