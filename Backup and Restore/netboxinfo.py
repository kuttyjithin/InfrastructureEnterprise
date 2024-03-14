import pynetbox
import requests
import csv
import warnings

# Define NetBox URL and authentication token
NETBOX_URL = "http://192.168.7.10"
NETBOX_TOKEN = "7e4cd190ed81f1efc89d71abf28df658c996c3b8"

def get_informationnetbox():
    # Suppressing the warning about insecure HTTPS requests
    warnings.filterwarnings("ignore", message="Unverified HTTPS request.*")

    # Creating a requests session
    session = requests.Session()
    session.verify = False  # Passing verify=False to bypass SSL certificate verification

    # Creating a NetBox API instance
    nb = pynetbox.api(url=NETBOX_URL, token=NETBOX_TOKEN)
    nb.http_session = session  # Assigning the requests session to pynetbox's http_session attribute

    # Querying devices from NetBox
    devices = nb.dcim.devices.all()

    # Storing device information in a list
    device_info_list = []

    # Iterating through devices
    for device in devices:
        if should_include_device(device):  # Checking if the device should be included
            # Constructing device information dictionary
            device_info = {
                'Device Name': device.name,
                'Device ID': device.id,
                'Device Type': device.device_type.display,
                'Manufacturer': device.device_type.manufacturer.display,
                'Model': device.device_type.model,
                'Role': device.device_role.display,
                'Site': device.site.display,
                'Status': device.status.label,
                'Primary IP': device.primary_ip.display if device.primary_ip else '',
                'Serial Number': device.serial
            }
            device_info_list.append(device_info)  # Appending device information to the list

    # Writing information about each device to a CSV file
    with open('netboxinfo.csv', 'w', newline='') as csvfile:
        fieldnames = ['Device Name', 'Device ID', 'Device Type', 'Manufacturer', 'Model', 'Role', 'Site', 'Status', 'Primary IP', 'Serial Number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Writing header row to the CSV file

        # Writing device information to the CSV file
        for device_info in device_info_list:
            writer.writerow(device_info)

def should_include_device(device):
    # Define devices to ignore
    devices_to_ignore = ['Client', 'Remote Client', 'Windows Server']

    # Checking if the device name contains any of the strings in devices_to_ignore
    for name_to_ignore in devices_to_ignore:
        if name_to_ignore in device.name:
            return False  # Excluding the device
    return True  # Including the device

def print_device_info(device_info):
    # Printing device information
    for key, value in device_info.items():
        print(f"{key}: {value}")
    print("\n")

if __name__ == '__main__':
    get_informationnetbox()
