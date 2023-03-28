"""
This program is a backup tool for Linux that lists all installed packages using either the 'apt' or 'dpkg' command,
and saves the list file to a user specified file path.

To use the program, simply run it from the command line using Python:

    $ python "Backup packages.py"

The user is prompted to select the package listing method, the output file path, and the package list separator. The
package list separator can be a space or a newline character.

Requirements:
    This program only works with Debian-based Linux distributions.

Author: Vaibhav Agrawal
Date: March 29, 2023

"""

import subprocess  # Importing subprocess module for running shell commands


def main():
    try:
        # Print initial message to the user
        print("This program only works with Debian-based Linux distributions.")

        # Prompt the user to select the package listing method
        print("Select package listing method:\n"
              "\t1 - 'apt' (recommended, high chances of full restoration)\n"
              "\t2 - 'dpkg' (bigger list, includes external packages)")
        method = int(input("Input: "))

        if method == 1:
            # Use 'apt' command to list all installed packages and extract the package names
            result = subprocess.run(["apt", "list", "--installed"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode().splitlines()
            del output[0]  # Remove the first line from the output containing column headers
            package_list = [package.split("/")[0] for package in output]
        elif method == 2:
            # Use 'dpkg' command to list all installed packages and extract the package names
            result = subprocess.run(["dpkg", "--list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode().splitlines()
            for i in range(5):
                del output[0]  # Remove the first 5 lines from the output containing column headers
            package_list = [package.split()[1].split(":")[0] for package in output]
        else:
            # If an invalid option is selected, raise an exception with an error message
            raise Exception("Invalid input! Please select 1 or 2.")

        # Print the number of installed packages found
        print(f"{len(package_list)} installed packages found.")

        # Prompt the user to select the output file path and the package list separator
        file = open(input("Output file path: ").strip(), "w")
        newline = input("Do you want the list to be separated by newline? Y/N: ").strip().lower()
        separator = "\n" if newline == "y" else " "

        # Write the package names to the output file using the selected separator
        package_list = separator.join(package_list)
        file.write(package_list)
        file.close()
        print(f"The package list has been written to {file}.")

    except Exception as e:
        # Handle any exceptions that may occur
        print(e)


# Call the main function when the script is executed
if __name__ == "__main__":
    main()
