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
    elif b"IPHONEACCEV" in line:
        if b',' not in line:
            return True

        parts = line[line.index(b',') + 1: -1].split(b',')
        if len(parts) < 1 or (len(parts) % 2) != 0:
            return True
        i = 0
        while i < len(parts):
            key = int(parts[i])
            val = int(parts[i + 1])
            if key == 1:
                blevel = (val + 1) * 10
                print(f"Battery level for {device} is {blevel}%")
                return False
            i += 2
    else:
        send(sock, b"OK")
    return True


def main():
    if (len(sys.argv) < 2):
        print("Usage: bl_battery.py <BT_MAC_ADDRESS>")
        exit()
    else:
        for device in sys.argv[1:]:
            try:
                s = socket.socket(socket.AF_BLUETOOTH,
                                  socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.connect((device, 4))

                while getATCommand(s, s.recv(128), device):
                    pass
            except OSError:
                print(f"{device} is offline")


if __name__ == "__main__":
    main()
