# Send system informations to custom QMK based keyboard.
[Link to custom keymap containing the OLED configurations](https://github.com/lnxx-56/qmk_firmware)

## Use as systemd service
Need to change the execution path for your own path

## For Ubuntu install
```
sudo apt install libasound2-dev
```

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
