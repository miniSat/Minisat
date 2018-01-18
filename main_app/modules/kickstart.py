import os


def kick_gen(passwd, location):
    with open("/var/www/html/ks.cfg", "w+") as ks:
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
                 "part / --fstype=\"ext4\" --grow --size=1"
                 )
    # os.system("scp /var/www/html/ks.cfg root@172.22.26.202:/var/www/html/")
    return "http://172.22.26.202/ks.cfg"

