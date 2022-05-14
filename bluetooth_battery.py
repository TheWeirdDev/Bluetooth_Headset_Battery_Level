#!/usr/bin/env python3

"""
A python library to get battery level from Bluetooth headsets
"""

# License: GPL-3.0
# Author: @TheWeirdDev, @GaLaXy102
# 29 Sept 2019

import argparse
import bluetooth
import pydbus
from typing import Optional, Union, List, Dict


class BatteryQueryError(bluetooth.BluetoothError):
    pass


class SocketDataIterator:
    def __init__(self, sock: bluetooth.BluetoothSocket, chunk_size: int = 128):
        """
        Create an Iterator over the given Socket

        chunk_size defines the amount of data in Bytes to be read per iteration
        """
        self._sock = sock
        self._chunk_size = chunk_size

    def __next__(self):
        """
        Receive chunks
        """
        return self._sock.recv(self._chunk_size)


class RFCOMMSocket(bluetooth.BluetoothSocket):

    def __init__(self, proto=bluetooth.RFCOMM, _sock=None):
        super().__init__(proto, _sock)

    def __iter__(self):
        """
        Iterate over incoming chunks of 128 Bytes
        """
        return SocketDataIterator(self)

    @staticmethod
    def find_rfcomm_port(device_mac) -> int:
        """
        Find the RFCOMM port number for a given bluetooth device
        """
        uuid = "0000111e-0000-1000-8000-00805f9b34fb"
        services: List[Dict] = bluetooth.find_service(address=device_mac, uuid=uuid)

        for service in services:
            if "protocol" in service.keys() and service["protocol"] == "RFCOMM":
                return service["port"]
        # Raise Interface error when the required service is not offered my the end device
        raise bluetooth.BluetoothError("Couldn't find the RFCOMM port number. Perhaps the device is offline?")

    def send(self, data):
        """
        This function sends a message through a bluetooth socket with added line separators
        """
        return super().send(b"\r\n" + data + b"\r\n")


class BatteryStateQuerier:

    def __init__(self, bluetooth_mac: str, bluetooth_port: Optional[Union[str, int]] = None):
        """
        Prepare a query for the end devices' battery state

        bluetooth_mac is the MAC of the end device, e.g. 11:22:33:44:55:66
        bluetooth_port is the Port of the RFCOMM/SPP service of the end device.
                       It will be determined automatically if not given.

        The actual query can be performed using the int() and str() method.
        """
        self._bt_settings = bluetooth_mac, int(bluetooth_port or RFCOMMSocket.find_rfcomm_port(bluetooth_mac))

    def __int__(self):
        """
        Perform a reading and get the result as int between 0 and 100
        """
        return self._perform_query()

    def __str__(self):
        """
        Perform a reading and get the result as str between 0% and 100%
        """
        return "{:.0%}".format(self._perform_query() / 100)

    def _perform_query(self) -> int:
        """
        Will try to get and print the battery level of supported devices
        """
        result = None
        sock = RFCOMMSocket()
        sock.connect(self._bt_settings)
        # Iterate received packets until there is no more or a result was found
        for line in sock:
            if b"BRSF" in line:
                sock.send(b"+BRSF: 1024")
                sock.send(b"OK")
            elif b"CIND=" in line:
                sock.send(b"+CIND:(\"service\",(0-1)),(\"call\",(0-1)),(\"callsetup\",(0-3)),(\"callheld\",(0-2)),(\"battchg\",(0-5))")
                sock.send(b"OK")
            elif b"CIND?" in line:
                sock.send(b"+CIND: 0,0,0,0,3")
                sock.send(b"OK")
            elif b"BIND=?" in line:
                # Announce that we support the battery level HF indicator
                # https://www.bluetooth.com/specifications/assigned-numbers/hands-free-profile/
                sock.send(b"+BIND: (2)")
                sock.send(b"OK")
            elif b"BIND?" in line:
                # Enable battery level HF indicator
                sock.send(b"+BIND: 2,1")
                sock.send(b"OK")
            elif b"XAPL=" in line:
                sock.send(b"+XAPL=iPhone,7")
                sock.send(b"OK")
            elif b"IPHONEACCEV" in line:
                parts = line.strip().split(b',')[1:]
                if len(parts) > 1 and (len(parts) % 2) == 0:
                    parts = iter(parts)
                    params = dict(zip(parts, parts))
                    if b'1' in params:
                        result = (int(params[b'1']) + 1) * 10
                        break
            elif b"BIEV=" in line:
                params = line.strip().split(b"=")[1].split(b",")
                if params[0] == b"2":
                    result = int(params[1])
                    break
            elif b"XEVENT=BATTERY" in line:
                params = line.strip().split(b"=")[1].split(b",")
                result = int(params[1]) / int(params[2]) * 100
                break
            else:
                sock.send(b"OK")
        sock.close()
        # Check whether the result was found, otherwise raise an Error
        if result is None:
            raise BatteryQueryError("Could not query the battery state.")
        return result


def return_connected_devices(mngr):
    result={}
    mngd_objs = mngr.GetManagedObjects()
    for path in mngd_objs:
        con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', False)
        if con_state:
            addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
            name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
            result[addr] = name
    return result


def main():
    """
    The starting point of the program. For each device address in the argument
    list a bluetooth socket will be opened and the battery level will be read
    and printed to stdout
    """
    bus = pydbus.SystemBus()

    adapter = bus.get('org.bluez', '/org/bluez/hci0')
    mngr = bus.get('org.bluez', '/')
    parser = argparse.ArgumentParser(description="Get battery level from Bluetooth headsets")
    parser.add_argument("-a","--all",action="store_true",help="Show battery of all connected devices")
    parser.add_argument("--devices", metavar="DEVICE_MAC[.PORT]", type=str, nargs="+",
                        help="(MAC address of target)[.SPP Port]")
    args = parser.parse_args()
    if args.devices:
        for device in args.devices:
            query = BatteryStateQuerier(*device.split("."))
            print("Battery level for {} is {}".format(device, str(query)))
    if args.all:
        result = return_connected_devices(mngr)
        for key in result:
            query = BatteryStateQuerier(key)
            print("Battery level for {} is {}".format(result[key], str(query)))

if __name__ == "__main__":
    main()
