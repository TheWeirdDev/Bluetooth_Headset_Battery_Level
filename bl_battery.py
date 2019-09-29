#!/usr/bin/env python3

#
# This script prints the battery charge level of some bluetooth headsets
# Define your BT_ADDRESS before using
# 

# License: GPL-3.0
# Author: @TheWeirdDev
# 29 Sept 2019

import socket

# Change this
BT_ADDRESS = 'XX:XX:XX:XX:XX:XX'

def send(sock, message):
    sock.send(b"\r\n" + message + b"\r\n")

def getATCommand(sock, line):
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
        parts = line.split(b",")

        # This might print the wrong value if dock state is received
        blevel = (int(parts[-1]) + 1) * 10
        print("Battery level: {}%\n".format(blevel))
        return False
    else:
        send(sock, b"OK")
    return True

def main():
    if (BT_ADDRESS.startswith("XX")):
        print("You need to define bluetooth address of your device\n")
        print("BT_ADDRESS =", BT_ADDRESS)
        exit()
		
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((BT_ADDRESS, 4))

    while getATCommand(s, s.recv(128)):
        pass

                
if __name__ == "__main__":
	main()

		
		

