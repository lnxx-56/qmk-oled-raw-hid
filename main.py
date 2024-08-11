import sys
import hid
import time
import psutil
import alsaaudio

############ CONSTANTS ###############

vendor_id     = 1240
product_id    = 60205

usage_page    = 65376
usage         = 97
report_length = 32

report_time = 1 # Second

######################################

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    connected_keyboard = hid.Device(path=raw_hid_interfaces[0]['path'])

    return connected_keyboard

def send_raw_report(data):
    interface = get_raw_hid_interface()
    
    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)

    try:
        interface.write(request_report)

        response_report = interface.read(report_length, timeout=1000)
    finally:
        interface.close()

################ MAIN ##################

if __name__ == '__main__':
    while True:
        # Get the CPU usage percentage (as an integer)
        cpu_usage = int(psutil.cpu_percent(interval=1))

        # Getting the volume level
        mixer = alsaaudio.Mixer()
        volume = mixer.getvolume()

        # Getting the ram usage
        free_ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

        # Convert usages to bytes
        report = bytes([cpu_usage])  + bytes([ord('&')]) + bytes([int(free_ram)]) + bytes([ord('&')]) + bytes([volume[0]])

        try:
            # Send the CPU usage report
            send_raw_report(report) 
        except:
            print('No device connected')

        time.sleep(report_time)
