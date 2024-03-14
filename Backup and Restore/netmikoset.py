import csv
from fortinetgets import fortinetinfo  
from getscisco import switchinfo  

def get_device_info_from_csv(csv_file):
    # Function to extract device information from CSV file
    device_info_list = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Constructing device information dictionary
            device_info = {
                'Device Name': row['Device Name'],
                'Primary IP': row['Primary IP'],
                'Device Type': 'fortinet' if 'FortiAP' in row['Device Type'] else 'cisco_ios'
            }
            device_info_list.append(device_info)  # Appending device information to the list
    return device_info_list

def connect_to_device(device_info):
    # Function to connect to devices based on device information
    devicetype = device_info['Device Type']
    device_ip = device_info['Primary IP']
    devicename = device_info['Device Name']

    try:
        # Setting username and password based on device type
        if devicetype == 'fortinet':
            username = 'admin'
            password = 'P@ssw0rd1'
            if device_ip[:-3] == '192.168.7.50': # Skipping connecting to this IP as per Network Design, HA Firewalls
                return  
            print("Connecting to Firewall")
            print(f"Device: {devicename} ({devicetype}) at {device_ip}")
            fortinetinfo(devicetype, device_ip[:-3], username, password, devicename)  # Connecting to Fortinet device
        else:
            username = 'cisco'
            password = 'cisco'
            print("Connecting to Switch")
            print(f"Device: {devicename} ({devicetype}) at {device_ip}")
            switchinfo(devicetype, device_ip[:-3], username, password, devicename)  # Connecting to Cisco device
    
    except Exception as e:
        print(f"Failed to connect to {devicename}: {str(e)}")  # Handling connection errors

def getinfos():
    # Function to get device information from CSV and connect to devices
    csv_file = 'netboxinfo.csv'
    device_info_list = get_device_info_from_csv(csv_file)  # Getting device information from CSV
    for device_info in device_info_list:
        connect_to_device(device_info)  # Connecting to devices based on device information

if __name__ == '__main__':
    getinfos()  # Executing main function to get information and connect to devices
