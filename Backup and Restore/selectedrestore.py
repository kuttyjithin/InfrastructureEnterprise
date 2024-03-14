import os
import datetime
from netmiko import ConnectHandler

def save_failed_commands(device_name, failed_commands):
    # Get current date and time
    now = datetime.datetime.now()
    current_time = now.strftime("%d-%m-%Y_%H-%M-%S")
    
    # Create directory if it doesn't exist
    directory = os.path.join(os.getcwd(), "failed_commands")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Write failed commands to a text file
    filename = f"{device_name}_{current_time}.txt"
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as f:
        f.write("\n".join(failed_commands))

def matchselect_restore(devices):
    # Folder containing configuration files
    folder_path = r'C:\School\NETW3300\lab 2\fromserver'
    
    # Find files starting with device names
    for device in devices:
        device_name = device['Device Name']
        matching_files = [filename for filename in os.listdir(folder_path) if filename.startswith(device_name)]
        if matching_files:
            for file in matching_files:
                config_file_path = os.path.join(folder_path, file)
                device_type = device['Device Type']
                ip_address = device['Primary IP']
                
                # Print device information including the matching filename
                print(f"\nConnecting to device: {device_name} ({device_type}) at {ip_address[:-3]} - Matching file: {file}")
                
                # Set username and password based on device type
                if device_type == 'fortinet':
                    username = 'admin'
                    password = 'P@ssw0rd1'
                elif device_type == 'cisco_ios':
                    username = 'cisco'
                    password = 'cisco'
                else:
                    print(f"Unknown device type: {device_type}")
                    continue  # Skip this device if the type is unknown
             
                # Establish SSH connection using Netmiko
                device_params = {
                    'device_type': device_type,
                    'ip': ip_address[:-3],
                    'username': username,
                    'password': password,
                    'global_delay_factor': 2  # Adjust as needed
                }
                with open(config_file_path, 'r') as config_file:
                    commandlist = config_file.read().splitlines()
                
                failed_commands = []  # List to store failed commands for this device
                    
                # Connect to the device
                with ConnectHandler(**device_params) as net_connect:
                    print(f"Connected to {device_name}\n")
                    
                    # Call appropriate function based on device type
                    try:
                        print(f'Doing {device_type} Configs')
                        net_connect.enable()
                        print("Enabled")
                        
                        # Enter configuration mode (conf t)
                        net_connect.config_mode()
                        print("Entered configuration mode")
                        
                        # Send each command individually
                        for command in commandlist:
                            try:
                                print("Pushing command:", command)
                                output = net_connect.send_command(command, expect_string=r'#')
                                print("Output:", output)
                            except Exception as e:
                                print(f"Error message for {command}: {str(e)}")
                                failed_commands.append(command)
                        
                        # Exit configuration mode
                        net_connect.exit_config_mode()
                        print("Exited configuration mode")
                        
                        # Save the configuration
                        net_connect.save_config()
                        print(f"Configuration saved on {device_type} device")
                    except Exception as e:
                        print(f"Error occurred while executing commands")
                        print(f"Error message: {str(e)}")
                
                if failed_commands:
                    save_failed_commands(device_name, failed_commands)

if __name__ == '__main__':
    pass
