# Send system informations to custom QMK based keyboard.
[Link to custom keymap containing the OLED configurations](https://github.com/lnxx-56/qmk_firmware)

## Use as systemd service
Need to change the execution path for your own path

## For Ubuntu install
```
sudo apt install libasound2-dev
```

## Install necessary python packages
pip install hid

Install the service as User service (NOT ROOT):
- Create user service folder if not present
```
mkdir ~/.config/systemd/user
```
```
cp ./qmk_oled.service ~/.config/systemd/user/qmk_oled.service
```

```
systemctl --user enable qmk_oled.service
```

## Setup of keyboard
# 🧠 USB Access Setup on Fedora (for Lily58 & other HID devices)

This project uses a USB HID device (e.g., Lily58 keyboard) that requires non-root access during development and testing.  
Fedora’s SELinux and udev system will, by default, block direct access to such devices from user-level Python scripts. Here's how to fix that cleanly.

## 🧰 Requirements

- Fedora-based Linux distro
- USB device with known `idVendor` and `idProduct`
- `pyusb` installed (`pip install pyusb`)
- `libusb` installed (`sudo dnf install libusb1-devel`)

---

## 🔌 Identifying Your Device

Plug in your device and run:

```bash
lsusb

