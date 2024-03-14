from netboxinfo import get_informationnetbox
from netmikoset import getinfos
from move2ftp import copy_files
from filefromserver import copy_files_from_latest_folder
from netconfig import list_available_devices, prompt_user_choice
from selectedrestore import matchselect_restore

def main():
    while True:
        try:
            banner = """\n\t\tStudent Assignment  Lab02 . Created by Jithin Jose, Saiban Muhammad, Walid M Rana and Bryan M Collins. Written on 2/28/2024
            
            **********************************************************************************************************************************
            
                NETW3300 Winter 2024, Sam El-Awour, Network Automation Program, Backup and Restore.

                Option A: This option backups network device using netbox inventory csv to connect with netmiko to get live configs.
                Then it will backup the configs to FTP Server and a local folder.

                Option B: Will get the latest configs from the FTP Server and then the user can select any or all devices to restore.
                The user will be able to see each command being pushed, it will save any failed commands to a file, to aid the user.

            **********************************************************************************************************************************
            """
            print (banner)
            # Displaying options to the user
            print("\nOption (A): Gather info from Netbox to get live configurations then backup to FTP server")
            print("Option (B): Set network based on configurations from FTP Server backups, based on selection")
            print("Option exit (X): Exit")

            # Prompting the user to choose an option
            userchoice = input("\nPick your option (A/B/X): ").lower()

            # Checking the user's choice and calling the appropriate function
            if userchoice == 'a':  
                get_informationnetbox()  # gets info from netbox
                print("\nCSV file created: netboxinfo.csv\n")
                getinfos() # get configs from devices
                print("Devices Info Saved\n")
                copy_files() # move files to ftp and backup locally as well
                print("\nFile moved to FTP Server\n")

            elif userchoice == 'b':  
                copy_files_from_latest_folder() # Obtain files from FTP Server 
                print("\nSelect devices(s)")
                devices_list = list_available_devices() # obtain device list for selections
                
                # Prompt user to choose device(s)
                selected_devices = prompt_user_choice(devices_list)
                print("Following Devices will be Configured\n")
                x = 0
                for device in selected_devices:
                    x += 1
                    print(x, ':', device['Device Name'])

                matchselect_restore(selected_devices)
            elif userchoice == 'x' or 'exit':
                print("Exiting the program.")
                break  # Exit the loop and end the program
            
            else:
                # If the user enters an invalid option, prompt again
                print("\nInvalid Option, try again\n")
                main()
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
