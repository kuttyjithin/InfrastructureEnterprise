import os
from ftplib import FTP
import datetime
from backupfiles import move_files  

def copy_files():
    # FTP server credentials
    hostname = '10.11.8.20'
    username = 'same'
    password = 'FuzzyDuck30'

    # Local directories from which files will be copied
    local_dir_paths = [
        r'C:\School\NETW3300\lab 2\Switches',
        r'C:\School\NETW3300\lab 2\firewall'
    ]

    # Remote directory path on the FTP server
    remote_dir_path = '/Team7'

    # Create a new folder with current timestamp as folder name
    new_folder_name = datetime.datetime.now().strftime("(%d_%m_%Y)-(%H_%M_%S)")

    try:
        # Connect to the FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        # Move to the desired directory on the server
        ftp.cwd(remote_dir_path)

        # Create a new directory on the server with the current timestamp as folder name
        ftp.mkd(new_folder_name)
        print(f"New folder '{new_folder_name}' created on the server.")

        # Iterate through local directories
        for local_dir_path in local_dir_paths:
            # Get list of files in the local directory
            files = os.listdir(local_dir_path)

            # Iterate through files in the local directory
            for file_name in files:
                local_file_path = os.path.join(local_dir_path, file_name)
                if os.path.isfile(local_file_path):
                    # Open the local file for reading in binary mode
                    with open(local_file_path, 'rb') as file:
                        # Change the current working directory to the newly created folder
                        ftp.cwd(f"{remote_dir_path}/{new_folder_name}")
                        # Create a new file on the server and write the contents of the local file to it
                        ftp.storbinary('STOR ' + file_name, file)

                    print(f"File '{file_name}' copied successfully from '{local_dir_path}' to '{new_folder_name}'.")

        print("All files copied successfully.\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'ftp' in locals():
            # Close the FTP connection
            ftp.quit()
            # Call the move_files function after copying files
            move_files()

if __name__ == '__main__':
    copy_files()
