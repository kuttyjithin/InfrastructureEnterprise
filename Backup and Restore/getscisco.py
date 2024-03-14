from netmiko import ConnectHandler  # Importing ConnectHandler from netmiko
import datetime  # Importing datetime module for timestamping
import os  # Importing os module for directory operations

def switchinfo(devicetype, device_ip, username, password, devicename):
    # Defining device parameters for Netmiko
    device = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password,
    }
    try: 
        # Establishing connection to the switch
        with ConnectHandler(**device) as connection:
            print("Switch Connected")
            connection.enable()  # Enabling privileged mode on the switch
            output = connection.send_command('show running-config')  # Sending command to get running configuration

            # Generating timestamp for filename
            timestamp = datetime.datetime.now().strftime("(%d_%m_%Y)-(%H_%M_%S)")
            filename = f"{devicename}_{timestamp}.txt"  # Creating filename with device name and timestamp

            directory = r"C:\School\NETW3300\lab 2\Switches"  # Specifying directory to save configuration files

            # Check if the directory exists, if not, create it
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save output to file in the specified directory
            with open(os.path.join(directory, filename), 'w') as f:
                f.write(output)  # Writing switch configuration to the file

            print(f"Output saved to {os.path.join(directory, filename)}\n")  # Printing the path where the file is saved
    except Exception as e:
        print(e)  # Handling and printing any exceptions that occur during the process

if __name__ == '__main__':
    pass  
