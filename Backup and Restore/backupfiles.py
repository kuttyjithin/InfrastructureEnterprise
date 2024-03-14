import os
import shutil

def move_files():
    # Define source and destination directory pairs
    source_dest_pairs = [
        (r'C:\School\NETW3300\lab 2\firewall', r'C:\School\NETW3300\lab 2\backups\firewall'),
        (r'C:\School\NETW3300\lab 2\Switches', r'C:\School\NETW3300\lab 2\backups\Switches')
    ]
    
    # Iterate over each pair of source and destination directories
    for source_dir, dest_dir in source_dest_pairs:
        try:
            # Get list of files in the source directory
            files_to_move = os.listdir(source_dir)
            
            # Move each file from the source directory to the destination directory
            for file in files_to_move:
                source_file_path = os.path.join(source_dir, file)  # Get the full path of the source file
                dest_file_path = os.path.join(dest_dir, file)      # Get the full path of the destination file
                shutil.move(source_file_path, dest_file_path)      # Move the file to the destination directory
                print(f"File {file} moved successfully from {source_dir} to {dest_dir}")  # Print success message
        except Exception as e:
            print(f"An error occurred: {e}")  # Print error message if an exception occurs

if __name__ == '__main__':
    move_files()
