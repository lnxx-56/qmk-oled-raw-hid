import usb.core
import usb.util

dev = usb.core.find(find_all=True)

if dev is None:
    print("No USB devices found")
else:
    for d in dev:
        print(d)
