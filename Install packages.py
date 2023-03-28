"""
This program is a restore tool for Linux that can install packages from a backup list and export installable and
non-installable packages list.

To use the program, simply run it from the command line using Python:

    $ python "Install packages.py"

This program reads a list of packages provided by the user and compares it with the list of packages currently
installed on the system.

Requirements:
    This program only works with Debian-based Linux distributions.

Author: Vaibhav Agrawal
Date: March 29, 2023

"""

import os  # Importing os module to interact with the operating system
import subprocess  # Importing subprocess module for running shell commands


def main():
    try:
        # Get a list of packages already installed on the system
        result = subprocess.run(["apt", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        # Extract package names from the output
        package_list = [package.split("/")[0] for package in output.splitlines()]
        del package_list[0]
        print(f"{len(package_list)} packages read.")

        # Get user input for the path of the package list file
        file = input("Path of the package list file: ").strip()
        file = open(file, "r")
        user_package_list = file.read()
        file.close()
        user_package_list = user_package_list.split()

        # Check which packages are available to install
        available = []
        unavailable = []
        for package in user_package_list:
            if package in package_list:
                available.append(package)
            else:
                unavailable.append(package)
        print(f"{len(available)} of {len(user_package_list)} packages are installable.")

        # Get user input for the desired operation
        print("What do you want to do?\n"
              "1 - Install all installable packages\n"
              "2 - Export list (non-installable packages only)\n"
              "3 - Export list (installable packages only)\n"
              "4 - Nothing (exit)")
        op = int(input("Input: ").strip())

        # Execute the desired operation
        if op == 1:
            # Install all available packages
            os.system(f"sudo apt install {' '.join(available)} -y")
        elif op in [2, 3]:
            # Export list of non-installable or installable packages depending upon what the user has opted for
            file = input("Output file path: ").strip()
            file = open(file, "w")
            newline = input("Do you want the list to be separated by newline? Y/N: ").strip().lower()
            separator = "\n" if newline == "y" else " "
            file.write(separator.join(unavailable if op == 2 else available))
            file.close()
        elif op == 4:
            # Exit the program
            exit()
        else:
            # Raise an exception if user has inputted an invalid option
            raise Exception("Invalid input! Valid options are 1, 2, 3 or 4.")

    except Exception as e:
        # Handle any exceptions that may occur
        print(e)


# Call the main function when the script is executed
if __name__ == "__main__":
    main()
