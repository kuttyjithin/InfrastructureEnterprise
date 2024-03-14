import csv

def get_device_info_from_csv(csv_file):
    """Extract device information from the CSV file."""
    device_info_list = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create dictionary for each device with name, primary IP, and device type
            device_info = {
                'Device Name': row['Device Name'],
                'Primary IP': row['Primary IP'],
                'Device Type': 'fortinet' if 'FortiAP' in row['Device Type'] else 'cisco_ios'
            }
            device_info_list.append(device_info)  # Append device info dictionary to list
    return device_info_list

def list_available_devices():
    """List available devices excluding FW01."""
    csv_file = 'netboxinfo.csv'
    devices_list = get_device_info_from_csv(csv_file)  # Get device info from CSV

    print("Available devices:")
    idx = 1  # Start index from 2
    for device in devices_list:
        if device['Device Name'] != 'FW01':
            print(f"{idx}. {device['Device Name']} ({device['Device Type']})")
            idx += 1
    return devices_list  # Return list of devices

def prompt_user_choice(devices_list):
    """Prompt user to choose devices for configuration."""
    available_devices = [device for device in devices_list if device['Device Name'] != 'FW01']

    while True:
        choice = input("\nEnter the numbers of devices you want to configure separated by commas (e.g., 1,3), or type 'all' for configuring all devices, or 'exit' to quit: ")
        if choice.lower() == 'all':
            selected_devices = available_devices
            break
        elif choice.lower() == 'exit':
            selected_devices = []
            break
        else:
            chosen_indices = [int(idx.strip()) - 1 for idx in choice.split(',') if idx.strip().isdigit()]  # Extract chosen indices
            print("Chosen indices:", chosen_indices)  # Debugging print statement
            # Check if any index is out of range
            if any(idx < 0 or idx >= len(available_devices) for idx in chosen_indices):
                print("Invalid input. Index out of range.")
                continue
            selected_devices = [available_devices[idx] for idx in chosen_indices]  # Get selected devices
            print("Selected devices:", selected_devices)  # Debugging print statement
            if selected_devices:
                break
            else:
                print("Invalid input. Please enter valid numbers or 'all' to configure all devices, or 'exit' to quit.")
    return selected_devices  # Return selected devices

if __name__ == "__main__":
    pass 
