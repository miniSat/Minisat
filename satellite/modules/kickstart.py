"""
This module generate the kickstart file for virtual machine
"""


def kick_gen(vm_name, passwd, location, repo):
    """Generate kickstart file

    :param vm_name: Name of virtual machine
    :param passwd: Password of virtual machine
    :param location: Location of operating system
    :param repo: List of repo needed to add in virtual machine

    :returns: location of kickstart file
    """
    with open("/tmp/ks.cfg", "w+") as ks:
        ks.write("install \n"
                 "keyboard 'us' \n"
                 "rootpw --plaintext " + passwd +
                 "\nlang en_US \n"
                 "firewall --enabled \n"
                 "reboot \n"
                 "timezone Asia/Kolkata --isUtc \n"
                 "graphical \n"
                 "url --url=\"" + location +
                 "\" \nauth  --useshadow  --passalgo=sha512 \n"
                 "user --name=" + vm_name + " --groups=wheel --plaintext --password=" + vm_name + " \n"
                 "firstboot --disable \n"
                 "selinux --enforcing \n"
                 "bootloader --location=mbr \n"
                 "clearpart --all --initlabel\n"
                 "part /boot --fstype=\"ext4\" --size=1024 \n"
                 "part swap --fstype=\"swap\" --size=2048 \n"
                 "part / --fstype=\"ext4\" --grow --size=1 \n"
                 "%post \n"
                 "hostnamectl set-hostname " + vm_name + " \n"
                 "systemctl restart sshd \n"
                 "systemctl enable sshd \n"
                 )

        for name, baseurl in repo.items():
            ks.write("echo -e '[" + name + "] \\nname=" + name + " \\nbaseurl=" + baseurl + " \\ngpgcheck=0 \\nenabled=1' >/etc/yum.repos.d/" + name + ".repo \n")
        ks.write("%end \n")

    return "/tmp/ks.cfg"
