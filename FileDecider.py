import os
import shutil

def regular_mode():
    print("Running in regular mode...")
    # Add your regular mode logic here

def custom_mode():
    print("Running in custom mode...")
    ldif_file_path = input("Enter the path of the LDIF file: ")

    # Validate if the file exists
    if not os.path.exists(ldif_file_path):
        print(f"Error: The specified file '{ldif_file_path}' does not exist.")
        return

    # Read data from the LDIF file
    with open(ldif_file_path, 'r') as ldif_file:
        ldif_data = ldif_file.read()

    # Update an existing file with the LDIF data (replace this with your logic)
    existing_file_path = "openldap/data/bootstrap.ldif"
    with open(existing_file_path, 'a') as existing_file:
        existing_file.write(ldif_data)

    print(f"Data from '{ldif_file_path}' has been added to '{existing_file_path}'.")

def main():
    print("Choose mode:")
    print("1. Regular Mode")
    print("2. Custom Mode")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        regular_mode()
    elif choice == "2":
        custom_mode()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
