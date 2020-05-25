# 🔋🎧 Bluetooth Headset Battery Level

This is a python script to fetch the battery charge level of some Bluetooth headsets.

You need python version 3.6.0 or newer to run the script.

# ▶️ How to run

### There are two options:

#### 1. Install from PyPI

```bash
pip install bluetooth_battery

bluetooth_battery [BT_MAC_ADDRESS_1] ...
```

#### 2. Download this repository

```bash
chmod +x bluetooth_battery.py

./bluetooth_battery.py [BT_MAC_ADDRESS_1] ...
```

**You can input addresses for as many devices as you want separated by space.**

_make sure you have `python-pybluez` or `python3-pybluez` or `python3-bluz` installed on your system._

_if you are using pip, install `PyBluez` instead._

### It didn't work?

You can set the port number manually by adding a dot at the end of mac address, like this: `00:00:00:00:00:00.3`

Try port numbers `1 to 9` to find the one that works for your device. (wait a few seconds between each try)

If that didn't work, disconnect your device first, and then try again.

### Still doesn't work?

Please consider that this script doesn't guarantee to support every bluetooth device.

You can open a new issue for discussion or check the existing ones for more information.

## Tested on

- [x] Linux (ArchLinux 5.6.14)

# 💸 Donate

You can donate if you like this project :)

BTC: `1KXJPJSmXUocieC3neRZEDakpzfcyumLqS`

BCH: `qzzmzegfy76r5glpj26jzq2xly2cczsmfyrn66ax8q`

ETH: `0xb6178080c8f0792e6370959909199647e26b8457`

Thank you!

# 📜 License

This project is a free software licensed under GPL-3.0 or newer.
