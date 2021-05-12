#!/usr/bin/env python3

"""
A python script to get battery level from Bluetooth headsets
"""

# License: GPL-3.0
# Author: @TheWeirdDev
# 29 Sept 2019

import sys
import bluetooth


def send(sock, message):
    """
    This function sends a message through a bluetooth socket
    """
    sock.send(b"\r\n" + message + b"\r\n")


def get_at_command(sock, line, device):
    """
    Will try to get and print the battery level of supported devices
    """
    blevel = -1

    if b"BRSF" in line:
        send(sock, b"+BRSF: 1024")
        send(sock, b"OK")
    elif b"CIND=" in line:
        send(sock, b"+CIND: (\"battchg\",(0-5))")
        send(sock, b"OK")
    elif b"CIND?" in line:
        send(sock, b"+CIND: 5")
        send(sock, b"OK")
    elif b"BIND=?" in line:
        # Announce that we support the battery level HF indicator
        # https://www.bluetooth.com/specifications/assigned-numbers/hands-free-profile/
        send(sock, b"+BIND: (2)")
        send(sock, b"OK")
    elif b"BIND?" in line:
        # Enable battery level HF indicator
        send(sock, b"+BIND: 2,1")
        send(sock, b"OK")
    elif b"XAPL=" in line:
        send(sock, b"+XAPL=iPhone,7")
        send(sock, b"OK")
    elif b"IPHONEACCEV" in line:
        parts = line.strip().split(b',')[1:]
        if len(parts) > 1 and (len(parts) % 2) == 0:
            parts = iter(parts)
            params = dict(zip(parts, parts))
            if b'1' in params:
                blevel = (int(params[b'1']) + 1) * 10
    elif b"BIEV=" in line:
        params = line.strip().split(b"=")[1].split(b",")
        if params[0] == b"2":
            blevel = int(params[1])
    elif b"XEVENT=BATTERY" in line:
        params = line.strip().split(b"=")[1].split(b",")
        blevel = int(params[1]) / int(params[2]) * 100
    else:
        send(sock, b"OK")

    if blevel != -1:
        print(f"Battery level for {device} is {blevel}%")
        return False

    return True


def find_rfcomm_port(device):
    """
    Find the RFCOMM port number for a given bluetooth device
    """
    uuid = "0000111e-0000-1000-8000-00805f9b34fb"
    proto = bluetooth.find_service(address=device, uuid=uuid)
    if len(proto) == 0:
        print("Couldn't find the RFCOMM port number")
        return 4

    for pr in proto:
        if 'protocol' in pr and pr['protocol'] == 'RFCOMM':
            port = pr['port']
            return port
    return 4


def main():
    """
    The starting point of the program. For each device address in the argument
    list a bluetooth socket will be opened and the battery level will be read
    and printed to stdout
    """
    if len(sys.argv) < 2:
        print("Usage: bluetooth_battery.py BT_MAC_ADDRESS_1.PORT ...")
        print("         Port number is optional")
        sys.exit()
    else:
        for device in sys.argv[1:]:
            i = device.find('.')
            if i == -1:
                port = find_rfcomm_port(device)
            else:
                port = int(device[i+1:])
                device = device[:i]
            try:
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((device, port))
                while get_at_command(sock, sock.recv(128), device):
                    pass
                sock.close()
            except OSError as err:
                print(f"{device} is offline", err)


if __name__ == "__main__":
    main()
