#!/usr/bin/env python3

"""
A python library to get battery level from Bluetooth headsets
"""

# License: GPL-3.0
# Author: @TheWeirdDev, @GaLaXy102, @drinkcat
# 29 Sept 2019

import argparse
import bluetooth
import logging
from typing import Optional, Union, List, Dict

logger = logging.getLogger(__name__)

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
        data = self._sock.recv(self._chunk_size)
        logger.debug("<<< " + str(data))
        return data


class RFCOMMSocket(bluetooth.BluetoothSocket):

    def __init__(self, proto=bluetooth.RFCOMM, _sock=None):
        super().__init__(proto, _sock)

    def __iter__(self):
        """
        Iterate over incoming chunks of 128 Bytes
        """
        return SocketDataIterator(self)

    @staticmethod
    def find_rfcomm_port(device_mac, uuid = "0000111e-0000-1000-8000-00805f9b34fb") -> int:
        """
        Find the RFCOMM port number for a given bluetooth device
        """
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
        logger.debug(">>> " + str(data))
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
        self._bluetooth_mac = bluetooth_mac
        self._bluetooth_port = int(bluetooth_port or RFCOMMSocket.find_rfcomm_port(bluetooth_mac))

        # Only try to use Nearby/Fast Pair protocol if port is not specified
        self._use_fastpair = (bluetooth_port == None)
        if self._use_fastpair:
            try:
                self._fastpair_port = RFCOMMSocket.find_rfcomm_port(bluetooth_mac, "df21fe2c-2515-4fdb-8886-f12c4d67927c")
            except bluetooth.BluetoothError:
                logger.debug("No Nearby service on this device, disabling.")
                self._use_fastpair = False

    def __int__(self):
        """
        Perform a reading and get the result as int between 0 and 100
        """
        result = self.query()
        # Check whether the result was found, otherwise raise an Error
        if "overall" in result:
            return result["overall"]

        # No overall, take minimum of left and right
        left = result.get("left")
        right = result.get("right")
        if left != None:
            if right == None or left < right:
                return left
            else:
                return right
        elif right != None:
            return right

        raise BatteryQueryError("Could not query the battery state.")

    def __str__(self):
        """
        Perform a reading and get the result as str between 0% and 100%
        """
        return "{:.0%}".format(int(self) / 100)

    def query(self) -> dict[str, int]:
        """
        Will try to get the battery level of supported devices, returns a dictionary with some of the following keys:
          - "overall" battery status (e.g. minimum of left and right earbuds)
          - "left"/"right"/"case": self explanatory
        """
        result = self._perform_query_rfcomm()
        if self._use_fastpair:
            result.update(self._perform_query_fastpair())
        logger.debug("Query results: " + str(result))

        return result

    def _perform_query_rfcomm(self) -> dict[str, int]:
        """
        Will try to get the battery level of supported devices over (more or
        less) standard RFCOMM/SPP service.
        """
        result: dict[str, int] = {}
        sock = RFCOMMSocket()
        logger.debug("Connecting to {}.{} (RFCOMM)".format(self._bluetooth_mac, self._bluetooth_port))
        sock.connect((self._bluetooth_mac, self._bluetooth_port))
        logger.debug("Connected")
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
                        result["overall"] = (int(params[b'1']) + 1) * 10
                        break
            elif b"BIEV=" in line:
                params = line.strip().split(b"=")[1].split(b",")
                if params[0] == b"2":
                    result["overall"] = int(params[1])
                    break
            elif b"XEVENT=BATTERY" in line:
                params = line.strip().split(b"=")[1].split(b",")
                if len(params) >= 3:
                    # AT+XEVENT=BATTERY,6,11,461,0
                    result["overall"] = int(params[1]) / int(params[2]) * 100
                else:
                    # AT+XEVENT=BATTERY,9
                    result["overall"] = (int(params[1]) + 1) * 10
                break
            else:
                sock.send(b"OK")
        sock.close()
        logger.debug("RFCOMM query results: " + str(result))
        return result

    def _perform_query_fastpair(self) -> dict[str, int]:
        """
        Will try to get the battery level of supported devices over the Nearby/Fast Pair protocol.
        """
        result: dict[str, int] = {}
        sock = RFCOMMSocket()
        logger.debug("Connecting to {}.{} (Nearby/Fast Pair)".format(self._bluetooth_mac, self._fastpair_port))
        sock.connect((self._bluetooth_mac, self._fastpair_port))
        logger.debug("Connected")

        try:
            for data in sock:
                while len(data) > 0:
                    # Header format https://developers.google.com/nearby/fast-pair/specifications/extensions/messagestream
                    if len(data) < 4:
                        logger.debug("Invalid data")
                        return result

                    group = data[0]
                    code = data[1]
                    length = int.from_bytes(data[2:4], "big")
                    payload = data[4:4+length+1]
                    logger.debug("Group: {}; Code: {}; Length: {}; Payload: {}".format(group, code, length, payload.hex()))

                    # See https://github.com/google/nearby/blob/main/fastpair/message_stream/message.h
                    # DeviceInformationEvent group, BatteryUpdated code.
                    if group == 3 and code == 3:
                        # Example: https://github.com/google/nearby/blob/main/fastpair/common/battery_notification.cc
                        def parse_level(level: int) -> int:
                            # 0xff means not present/unknown
                            if level == 0xff:
                                return None
                            # Top bit indicates if the device is charging
                            return level & 0x7f

                        if len(payload) == 1:
                            result["overall"] = parse_level(payload[0])
                        elif len(payload) == 3:
                            result["left"] = parse_level(payload[0])
                            result["right"] = parse_level(payload[1])
                            result["case"] = parse_level(payload[2])
                        else:
                            raise BatteryQueryError("Invalid number of data points in Fast Pair packet.")
                        break

                    # Parse next packet
                    data = data[4+length:]
                if len(result) > 0:
                    break

            sock.close()
        except bluetooth.BluetoothError as e:
            # Fast Pair errors are not fatal.
            logger.info("Bluetooth Error while reading Nearby/Fast Pair data: " + str(e))
            pass
        logger.debug("Nearby/Fast Pair query results: " + str(result))
        return result

def main():
    """
    The starting point of the program. For each device address in the argument
    list a bluetooth socket will be opened and the battery level will be read
    and printed to stdout
    """
    parser = argparse.ArgumentParser(description="Get battery level from Bluetooth headsets")
    parser.add_argument("devices", metavar="DEVICE_MAC[.PORT]", type=str, nargs="+",
                        help="(MAC address of target)[.SPP Port]")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logs")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    for device in args.devices:
        query = BatteryStateQuerier(*device.split("."))
        result = query.query()
        print("Battery level for {}:".format(device), end="")
        if "overall" in result:
            print(" {:.0%}.".format(result["overall"]/100), end="")
        for key, value in result.items():
            if key != "overall":
                print(" {}: {:.0%}.".format(key.capitalize(), value/100), end="")
        print("")


if __name__ == "__main__":
    main()
