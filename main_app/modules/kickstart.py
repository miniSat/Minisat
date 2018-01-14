

def kick_gen(passwd, location, partition):
    ks = open("ks.cfg", "w+")
    ks.write("install \n"
             "keyboard 'us' \n"
             "rootpw --plaintext "+passwd+"\n"
             "lang en_US \n"
             "firewall --enabled \n"
             "reboot \n"
             "timezone Africa/Abidjan --isUtc \n"
             "graphical \n"
             "url --url= \"" +location+ "\" \n"
             "auth  --useshadow  --passalgo=sha512 \n"
             "firstboot --enable \n"
             "selinux --enforcing \n"
             "bootloader --location=mbr \n"
             "clearpart --all --initlabel\n"
             )
    for i in partition:
        ks.write(i + "\n")
    ks.close()

passwd = "root"
location = "http://172.22.26.203/repos/fedora25/"
partition = ["part /boot --fstype=\"ext4\" --size=1024 ",
             "part swap --fstype=\"swap\" --size=2048 ",
             "part / --fstype=\"ext4\" --grow --size=1 "]
kick_gen(passwd, location, partition)