import sys
import hid
import time
import psutil
import alsaaudio

############ CONSTANTS ###############

vendor_id     = 1240
product_id    = 60205

# Original values that don't work with Lily58
usage_page    = 65376
usage         = 97

# Values for Lily58 keyboard
report_length = 32

report_time = 1 # Second

######################################

def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    print("Found devices with matching vendor_id and product_id:")
    for i, device in enumerate(device_interfaces):
        print(f"Device {i+1}:")
        for key, value in device.items():
            print(f"    {key}: {value}")
    
    # Try to find interfaces matching our criteria
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]
    print(f"\nFiltering for usage_page={usage_page}, usage={usage}")
    print(f"Found {len(raw_hid_interfaces)} matching interfaces")

    if len(raw_hid_interfaces) == 0:
        return None
    
    try:
        print(f"Attempting to connect to interface with path: {raw_hid_interfaces[0]['path']}")
        connected_keyboard = hid.Device(path=raw_hid_interfaces[0]['path'])
        print("Successfully connected to device!")
        return connected_keyboard
    except Exception as e:
        print(f"Error connecting to device: {e}")
        # Try the next interface if the first one fails
        if len(raw_hid_interfaces) > 1:
            try:
                print(f"Trying next interface with path: {raw_hid_interfaces[1]['path']}")
                connected_keyboard = hid.Device(path=raw_hid_interfaces[1]['path'])
                print("Successfully connected to device!")
                return connected_keyboard
            except Exception as e:
                print(f"Error connecting to second interface: {e}")
        return None

def send_raw_report(data):
    interface = get_raw_hid_interface()
    
    if interface is None:
        print("No device found")
        return False

    request_data = [0x00] * (report_length + 1) # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_report = bytes(request_data)

    try:
        print(f"Sending data: {request_data}")
        result = interface.write(request_report)
        print(f"Write result: {result}")

        print("Waiting for response...")
        response_report = interface.read(report_length, timeout=1000)
        print(f"Response received: {response_report}")
        return True
    except Exception as e:
        print(f"Error communicating with device: {e}")
        return False
    finally:
        try:
            interface.close()
            print("Interface closed")
        except Exception as e:
            print(f"Error closing interface: {e}")

################ MAIN ##################

if __name__ == '__main__':
    print("Starting QMK OLED Raw HID Script")
    print(f"Looking for device with vendor_id={vendor_id}, product_id={product_id}, usage_page={usage_page}, usage={usage}")
    
    while True:
        try:
            # Get the CPU usage percentage (as an integer)
            cpu_usage = int(psutil.cpu_percent(interval=1))

            # Getting the volume level
            mixer = alsaaudio.Mixer()
            volume = mixer.getvolume()

            # Getting the ram usage
            free_ram = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

            # Convert usages to bytes
            report = bytes([cpu_usage]) + bytes([ord('&')]) + bytes([int(free_ram)]) + bytes([ord('&')]) + bytes([volume[0]])
            print(f"\nSystem stats: CPU={cpu_usage}%, RAM free={int(free_ram)}%, Volume={volume[0]}%")
            
            # Send the report
            success = send_raw_report(report)
            if not success:
                print('Failed to communicate with device')
        except Exception as e:
            print(f'Error in main loop: {e}')

        print(f"Sleeping for {report_time} seconds...")
        time.sleep(report_time)
