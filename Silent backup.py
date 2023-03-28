"""
This program is a backup tool for Linux that saves a list of installed packages to a text file.
The text file is named with the hostname and the current date and time, and is saved to the user's home directory.

To use the program, simply run it from the command line using Python:

    $ python "Silent backup.py"

The program requires no additional arguments or input. Upon completion, it will print a message indicating that
the backup is complete, and the user can find the backup file in their home directory.

Requirements:
    This program only works with Debian-based Linux distributions.

Author: Vaibhav Agrawal
Date: March 29, 2023

"""

# Import the necessary modules
import os  # Importing os module to interact with the operating system
import subprocess  # Importing subprocess module for running shell commands
import socket  # Importing socket module for getting the hostname of the computer
from time import time  # Importing time module for getting the current time
from datetime import datetime  # Importing datetime module for formatting the timestamp


def main():
    try:
        # Get the current date and time in YYYY-MM-DD HH:MM:SS format
        date_time = datetime.fromtimestamp(time()).strftime("%Y-%m-%d_%H.%M.%S")

        # Run the shell command "apt list --installed" to get installed packages and capture the output
        result = subprocess.run(["apt", "list", "--installed"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode().splitlines()

        # Remove the first line of output, which contains column headers
        del output[0]

        # Extract the package names from the remaining lines of output
        package_list = [package.split("/")[0] for package in output]

        # Create a new file in a folder "Backup" in the home directory with the hostname and timestamp in the filename
        file = os.path.join(os.path.expanduser("~"), "Backup", f"{socket.gethostname()}_{date_time}.txt")
        file = open(file, "w")

        # join the package names into a single string separated by spaces
        package_list = " ".join(package_list)

        # write the package names to the file and close it
        file.write(package_list)
        file.close()

        # print a message indicating that the backup is complete
        print("Done.")

    except Exception as e:
        # Handle any exceptions that may occur
        print(e)


# Call the main function when the script is executed
if __name__ == "__main__":
    main()
