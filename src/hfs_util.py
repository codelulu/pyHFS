import os
import socket
import fcntl
import struct

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
            )[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break;
            except IOError:
                pass

    return ip

def smart_size(size):
    size *= 1.0
    if size < 0:
        return 'N/A'
    elif size < 1 << 10:
        return '%d B' % size
    elif size < 1 << 20:
        return '%.2f KB' % (size / (1 << 10))
    elif size < 1 << 30:
        return '%.2f MB' % (size / (1 << 20))
    else:
        return '%.2f GB' % (size / (1 << 30))

