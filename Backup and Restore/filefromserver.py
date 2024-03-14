from ftplib import FTP
import os

def copy_files_from_latest_folder():
    # FTP server credentials
    hostname = '10.11.8.20'
    username = 'same'
    password = 'FuzzyDuck30'
    
    # Remote directory path on the FTP server
    remote_dir_path = '/Team7'
    
    # Local directory path to copy files to
    local_dir_path = 'C:/School/NETW3300/lab 2/fromserver'
    
    try:
        # Connect to the FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)
        
        # Change to the remote directory
        ftp.cwd(remote_dir_path)

        # List directories in the remote directory
        directories = ftp.nlst()

        # Get details of each directory
        directory_details = []
        for directory in directories:
            # Skip non-directory items (like files)
            if "." not in directory:
                details = ftp.sendcmd('MDTM ' + directory)
                directory_details.append((details, directory))

        # Sort the directories based on last modified time
        sorted_dirs = sorted(directory_details, key=lambda x: x[0])

        # Get the latest folder
        latest_folder = sorted_dirs[-1][1] if sorted_dirs else None

        if latest_folder:
            # Change to the latest folder on the server
            ftp.cwd(latest_folder)

            # List files in the latest folder
            files = ftp.nlst()

            # Empty local directory
            files_local = os.listdir(local_dir_path)
            for file in files_local:
                file_path = os.path.join(local_dir_path, file)
                os.remove(file_path)

            # Copy each file to local directory
            for file in files:
                local_file_path = os.path.join(local_dir_path, file)
                with open(local_file_path, 'wb') as local_file:
                    ftp.retrbinary('RETR ' + file, local_file.write)

            print("\nFiles from latest folder copied to:", local_dir_path, '\n')
        else:
            print("\nNo folder found.\n")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'ftp' in locals():
            # Close the FTP connection
            ftp.quit()

if __name__ == '__main__':
    copy_files_from_latest_folder()
