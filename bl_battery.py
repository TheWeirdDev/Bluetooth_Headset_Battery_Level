#!/usr/bin/env python3

"""
This script prints the battery charge level of some bluetooth headsets
"""

# License: GPL-3.0
# Author: @TheWeirdDev
# 29 Sept 2019

import socket
import sys


def send(sock, message):
    sock.send(b"\r\n" + message + b"\r\n")


def getATCommand(sock, line, device):
    if b"BRSF" in line:
        send(sock, b"+BRSF:20")
        send(sock, b"OK")
    elif b"CIND=" in line:
        send(sock, b"+CIND: (\"battchg\",(0-5))")
        send(sock, b"OK")
    elif b"CIND?" in line:
        send(sock, b"+CIND: 5")
        send(sock, b"OK")
    elif b"XAPL=" in line:
        send(sock, b"+XAPL: iPhone,7")
        send(sock, b"OK")
    elif b"IPHONEACCEV" in line:
        parts = line.strip().split(b',')[1:]
        if len(parts) > 1 and (len(parts) % 2) == 0:
            parts = iter(parts)
            params = dict(zip(parts, parts))
            if b'1' in params:
                blevel = (int(params[b'1']) + 1) * 10
                print(f"Battery level for {device} is {blevel}%")
                return False
    else:
        send(sock, b"OK")
    return True


def main():
    if (len(sys.argv) < 2):
        print("Usage: bl_battery.py <BT_MAC_ADDRESS_1> ...")
        exit()
    else:
        for device in sys.argv[1:]:
            try:
                s = socket.socket(socket.AF_BLUETOOTH,
                                  socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.connect((device, 4))

                while getATCommand(s, s.recv(128), device):
                    pass
            except OSError as e:
                print(f"{device} is offline", e)


if __name__ == "__main__":
    main()
