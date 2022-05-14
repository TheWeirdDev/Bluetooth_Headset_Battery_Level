# 🔋🎧 Bluetooth Headset Battery Level

This is a python script to fetch the battery charge level of some Bluetooth headsets.

You need python 3.6 or newer to run the script.

Table of Contents
=================

* [How to run](#️-how-to-run)
    * [Option 1: Install from PyPI](#option-1-install-from-pypi)
    * [Option 2: Download this repository](#option-2-download-this-repository)
    * [Option 3: Docker](#option-3-docker)
    * [Option 4: AUR](#option-4-aur)
* [Library usage](#library-usage)
* [GNOME Extension](#gnome-extension)
* [Budgie Applet](#budgie-applet)
* [Finding MAC address](#finding-mac-address)
* [It didn't work?](#it-didnt-work)
* [Still doesn't work?](#still-doesnt-work)
* [Tested on](#tested-on)
* [Thanks](#-thanks)
* [License](#-license)

# ▶️ How to run

### There are four options:

### Option 1: Install from PyPI
Please ensure you have the BlueZ, pydbus and python libraries and header files if you are using Ubuntu/Debian based distros:
```console
sudo apt install libbluetooth-dev python3-dev
```

If you are using *OpenSUSE*, you will need to install `bluez`, `bluez-devel`, `python3-devel`, `python3-pybluez`

Then, install with pip:
```console
pip3 install bluetooth_battery

bluetooth_battery BT_MAC_ADDRESS_1 ...
```

**You can input addresses for as many devices as you want separated by space.**

_the dependency `pybluez` should be installed automatically, but if not, you may need to install it manually_

--------

### Option 2: Download this repository

```console
cd Bluetooth_Headset_Battery_Level
chmod +x bluetooth_battery.py

./bluetooth_battery.py BT_MAC_ADDRESS_1 ...
```

_make sure you have `python-pybluez` or `python3-pybluez` or `python3-bluez` and `python3-pydbus` installed on your system._

--------

### Option 3: Docker

You must have docker installed on your system.
Clone the repository using `git clone` command. Then run:

```console
cd Bluetooth_Headset_Battery_Level
docker build -t bluetooth_battery_level .
```

Once the build is complete you can use the below command to run the program:

```console
docker run --rm -ti --privileged --net=host bluetooth_battery_level "BT_MAC_ADDRESS"
```

--------

### Option 4: AUR

You must have AUR access enabled on your Arch or Manjaro machine.
You can install this library using

```console
yay -S python-bluetooth-battery
```

--------

## Library usage

To use this as a library, simply install it using pip or AUR (see above) or require it in your Pipfile.  
You can then
```python
from bluetooth_battery import BatteryStateQuerier, BatteryQueryError, BluetoothError
                                                   # only for error handling
```
and query the Battery State as follows:
```python
# Autodetects SPP port
query = BatteryStateQuerier("11:22:33:44:55:66")
# or with given port
query = BatteryStateQuerier("11:22:33:44:55:66", "4")

result = int(query)  # returns integer between 0 and 100
# or
result = str(query)  # returns "0%".."100%"
```

As errors can occur in a wireless system, you probably want to handle them:

```python
try:
    query = BatteryStateQuerier("11:22:33:44:55:66")  # Can raise BluetoothError when autodetecting port
    str(query)                                        # Can raise BluetoothError when device is down or port is wrong
                                                      # Can raise BatteryQueryError when the device is unsupported
except BluetoothError as e:
    # Handle device is offline
    ...
except BatteryQueryError as e:
    # Handle device is unsupported
    ...
```

## GNOME Extension

There is also a GNOME extension for integrating this program with GNOME desktop environment:
https://extensions.gnome.org/extension/3991/bluetooth-battery/

## Budgie Applet

There is also a Budgie extension for integrating this program with Budgie desktop environment:
https://github.com/GaLaXy102/budgie-bluetooth-battery-applet

## Finding MAC address

There are a variety of utilities that can find the MAC address of your bluetooth device.  Here is one, this command is in the `bluez` package, and the given argument gets a list of all devices it knows about, even if not currently available.
```
$ bluetoothctl devices
Device E8:AB:FA:XX:XX:XX iTeknic IK-BH002
Device D0:77:14:XX:XX:XX Barak's Moto X4
Device E8:AB:FA:XX:XX:XX iTeknic IK-BH002
```
The 1st and 3rd would be relevant here, as those are headsets.

This shows devices that are actually connected.
```console
$ bluetoothctl info
Device E8:AB:FA:XX:XX:XX (public)
	Name: iTeknic IK-BH002
	...
```
So you can use
```console
bluetooth_battery.py $(bluetoothctl info | awk '/^Device/ {print $2}')
```
to query the battery of all connected devices.

## It didn't work?

You can set the port number manually by adding a dot at the end of mac address, like this: `00:00:00:00:00:00.3`

Try port numbers `1 to 30` to find the one that works for your device. (wait a few seconds between each try)

If that didn't work, **disconnect your device first**, and then try again.

## Still doesn't work?

Please consider that this script doesn't guarantee to support every bluetooth device.

You can open a new issue for discussion or check the existing ones for more information.

## Tested on

- [x] ArchLinux (5.6.14)
- [x] Manjaro (5.14.10)
- [x] NixOS 20.09 (20.09.2386.ae1b121d9a6)
- [x] Debian GNU/Linux (bullseye 5.9)
- [x] Ubuntu/Linux (Focal Fossa 20.04.1)
- [x] openSUSE (Leap 15.3)

# 🤝 Thanks

Special thanks to:

[@clst](https://github.com/clst): For spreading the word!

[@bhepple](https://github.com/bhepple): For his research on fixing the important bug

[@balsoft](https://github.com/balsoft): For thinking outside the box (finding my big mistake)

[@martin-beran](https://github.com/martin-beran): For making it easy to set the port number

[@Bobo1239](https://github.com/Bobo1239): For adding support for Samsung galaxy buds

[@keystroke3](https://github.com/keystroke3): For adding multiple device support to the script

[@jadia](https://github.com/jadia): For docker container support

[@cheriimoya](https://github.com/cheriimoya): For refactoring the code and providing NixOS packages

[@MichalW](https://github.com/MichalW): For making the GNOME shell extension

[@GaLaXy102](https://github.com/GaLaXy102): For re-writing the code, making it cleaner and usable as a library

❤️ And everyone else that pointed out the issues or helped me with writing the code or testing it.

# 📜 License

This project is a free software licensed under GPL-3.0 or newer. For more information see [LICENSE](LICENSE)
