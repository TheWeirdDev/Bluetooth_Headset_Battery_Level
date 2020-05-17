# 🔋🎧 Bluetooth Headset Battery Level

This is a python script to fetch the battery charge level of some Bluetooth headsets.

You need python version 3.6.0 or newer to run the script.

# ▶️ How to run

```bash
chmod +x bl_battery.py
./bl_battery.py [BT_MAC_ADDRESS_1] ...
```

You can input addresses for as many devices as you want separated by space.

### It didn't work?

You can set the port number manually by adding a dot at the end of mac address, like this: `00:00:00:00:00:00.3`

Try port numbers `1 to 9` to find the one that works for your device.

If that didn't work, disconnect your device first, and then try again.

## Still doesn't work?

Please consider that this script doesn't guarantee to support every bluetooth device.

You can open a new issue for discussion or check the existing ones for more information.

## Tested on

- [x] Linux (ArchLinux 5.6.11)

# 💸 Donate

You can donate if you like this project :)

BTC: `1KXJPJSmXUocieC3neRZEDakpzfcyumLqS`

BCH: `qzzmzegfy76r5glpj26jzq2xly2cczsmfyrn66ax8q`

ETH: `0xb6178080c8f0792e6370959909199647e26b8457`

Thank you!

# 📜 License

This project is a free software licensed under GPL-3.0 or newer.
