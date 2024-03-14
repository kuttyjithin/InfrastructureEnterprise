from netmiko import ConnectHandler
import datetime
import os

def fortinetinfo(devicetype, host, user, passwords, devicename):
    # Define device information
    device = {
        'device_type': devicetype,
        'host': host,
        'username': user,
        'password': passwords,
    }
    try:
        # Connect to the device
        net_connect = ConnectHandler(**device)

        # Send the first command
        net_connect.send_config_set(['show'])

        # Get the output of the second command
        running_config = net_connect.send_command('show')

        # Generate filename based on hostname and timestamp
        timestamp = datetime.datetime.now().strftime("(%d_%m_%Y)-(%H_%M_%S)")
        filename = f"{devicename}_{timestamp}.txt"

        # Specify the directory path
        directory = r"C:\School\NETW3300\lab 2\firewall" 
        print(directory)
        # Check if the directory exists, if not, create it
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save output to file in the specified directory
        with open(os.path.join(directory, filename), 'w') as f:
            f.write(running_config)

        print(f"Output saved to {os.path.join(directory, filename)}\n")

        # Disconnect from the device
        net_connect.disconnect()
    except Exception as e: # Handle Errors
        print(e)

if __name__ == '__main__':
    pass