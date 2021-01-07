# 🔋🎧 Bluetooth Headset Battery Level

This is a python script to fetch the battery charge level of some Bluetooth headsets.

You need python 3.6 or newer to run the script.

# ▶️ How to run

### There are three options:

#### 1. Install from PyPI
Please ensure you have the BlueZ and python libraries and header files if you are using Ubuntu/Debian based distros:
```bash
sudo apt install libbluetooth-dev python3-dev
```

If you are using OpenSUSE, you will need to install these packages:
```bash
bluez
bluez-devel
python3-devel
python3-pybluez
```

Then, install with pip:
```bash
pip3 install bluetooth_battery

bluetooth_battery BT_MAC_ADDRESS_1 ...
```
_the dependency `pybluez` should be installed automatically, but if not, you may need to install it manually_

#### 2. Download this repository
```bash
chmod +x bluetooth_battery.py

./bluetooth_battery.py BT_MAC_ADDRESS_1 ...
```

_make sure you have `python-pybluez` or `python3-pybluez` or `python3-bluez` installed on your system._

**You can input addresses for as many devices as you want separated by space.**

#### 3. Docker

You must have docker installed on your system.
Use the below command to install or refer to [this guide](https://docs.docker.com/engine/install/).

```bash
curl -fsSL get.docker.com | sudo bash
```

Clone the repository using `git clone` command.

```bash
cd Bluetooth_Headset_Battery_Level && \
docker build -t bluetooth_battery_level .
```

Once the build is complete you can use the below command to run the program:

```bash
docker run --rm -ti --privileged --net=host bluetooth_battery_level "BT_MAC_ADDRESS"
#docker run --rm -ti --privileged --net=host bluetooth_battery_level "E2:41:23:5C:4F:27"
```
### It didn't work?

You can set the port number manually by adding a dot at the end of mac address, like this: `00:00:00:00:00:00.3`

Try port numbers `1 to 30` to find the one that works for your device. (wait a few seconds between each try)

If that didn't work, disconnect your device first, and then try again.

### Still doesn't work?

Please consider that this script doesn't guarantee to support every bluetooth device.

You can open a new issue for discussion or check the existing ones for more information.

## Tested on

- [x] ArchLinux (5.6.14)
- [x] NixOS 20.09 (20.09.2386.ae1b121d9a6)

# 💸 Donate

You can donate if you like this project :)

BTC: `1KXJPJSmXUocieC3neRZEDakpzfcyumLqS`

BCH: `qzzmzegfy76r5glpj26jzq2xly2cczsmfyrn66ax8q`

ETH: `0xb6178080c8f0792e6370959909199647e26b8457`

Thank you!

# 🤝 Thanks

Special thanks to:

[@clst](https://github.com/clst): For spreading the word!

[@bhepple](https://github.com/bhepple): For his research on fixing the ultimate bug

[@balsoft](https://github.com/balsoft): For thinking outside the box (finding my big mistake)

[@martin-beran](https://github.com/martin-beran): For making it easy to set the port number

[@Bobo1239](https://github.com/Bobo1239): For adding support for Samsung galaxy buds

[@keystroke3](https://github.com/keystroke3): For adding multiple device support to the script

❤️ And everyone else that pointed out the issues or helped me with writing the code or testing it.

# 📜 License

This project is a free software licensed under GPL-3.0 or newer.
