import os


def isOnline(host):
    response = os.system("ping -c 2 " + host + " > /dev/null 2>&1 &")
    if response == 0:
        print("online")
    else:
        print("offline")


isOnline("google.com")
