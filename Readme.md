# Bluetooth Headset Battery Level

This is a simple python script to get the battery charge level of some bluetooth headsets

# How to run

# Usage in Polybar
To use in polybar, make the script executable by running:
```bash
chmod +x bl_battery.py
```
and create a module  with this structure in polybar config file:
```ini
[module/bluetooth-bat-level]
type = custom/script
exec = /path/to/bl_battery.py [BLUETOOTH MAC ADDRESS]
interval = VALUE
```
A large `interval` value is encouraged to reduce oscillating results. A value of 10-30 will do. Note that the greater the value, the longer it takes for connection changes (like a newly connected device) to show.

## Tested on

- [x] Linux (ArchLinux 5.4.15-arch1-1)
- [ ] macos
- [ ] Windows

Works on windows/macos too? if so, make a pull request and check that checkbox.

# License
GPL-3.0

