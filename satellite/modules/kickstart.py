"""
kickgen function create a kickstart and save it in /var/www/html folder
httpd.service should be running
"""
import os


def kick_gen(passwd, location):
    with open("/tmp/ks.cfg", "w+") as ks:
        ks.write("install \n"
                 "keyboard 'us' \n"
                 "rootpw --plaintext " + passwd +
                 "\nlang en_US \n"
                 "firewall --enabled \n"
                 "reboot \n"
                 "timezone Africa/Abidjan --isUtc \n"
                 "graphical \n"
                 "url --url=\"" + location +
                 "\" \nauth  --useshadow  --passalgo=sha512 \n"
                 "firstboot --disable \n"
                 "selinux --enforcing \n"
                 "bootloader --location=mbr \n"
                 "clearpart --all --initlabel\n"
                 "part /boot --fstype=\"ext4\" --size=1024 \n"
                 "part swap --fstype=\"swap\" --size=2048 \n"
                 "part / --fstype=\"ext4\" --grow --size=1 \n"
                 "%post \n"
                 "systemctl restart sshd \n"
                 "systemctl enable sshd \n"
                 "%end "
                 )
    os.system("scp /tmp/ks.cfg root@172.22.26.102:/var/www/html/")
    return "http://172.22.26.102/ks.cfg"
