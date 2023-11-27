import os
import random

def get_openldap_data_directory():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Set the data directory path outside of the generator directory
    data_directory = os.path.join(script_directory, "..", "data")
    output_ldif_file = os.path.join(data_directory, "generated_data.ldif")
    return output_ldif_file

def generate_group_entry():
    ldif_content = "dn: ou=Groups,dc=example,dc=org\n"
    ldif_content += "changetype: add\n"
    ldif_content += "objectclass: organizationalUnit\n"
    ldif_content += "ou: Groups\n\n"
    return ldif_content

def generate_group_ldif(group_name, user_dn_list):
    ldif_content = f"dn: cn={group_name},ou=Groups,dc=example,dc=org\n"
    ldif_content += "changetype: add\n"
    ldif_content += f"cn: {group_name}\n"
    ldif_content += "objectclass: groupOfUniqueNames\n"

    # Determine a random subset size for the group
    subset_size = random.randint(1, len(user_dn_list))
    
    # Shuffle the user_dn_list and select a random subset
    random.shuffle(user_dn_list)
    selected_members = user_dn_list[:subset_size]

    # Generate uniqueMember entries for the group based on the subset
    for user_dn in selected_members:
        ldif_content += f"uniqueMember: {user_dn}\n"

    ldif_content += "\n"  # Add one line of space after the group entry
    return ldif_content

def generate_user_ldif(user_name):
    user_dn = f"cn={user_name},dc=example,dc=org"
    ldif_content = f"dn: {user_dn}\n"
    ldif_content += "changetype: add\n"
    ldif_content += "objectclass: inetOrgPerson\n"
    ldif_content += f"cn: {user_name}\n"
    ldif_content += f"givenname: {user_name}\n"
    ldif_content += f"sn: {user_name.capitalize()}\n"
    ldif_content += f"displayname: {user_name.capitalize()} User\n"
    ldif_content += f"mail: {user_name}@gmail.com\n"
    ldif_content += f"uid: {user_name}\n"
    ldif_content += f"userpassword: {user_name}_pass\n"

    ldif_content += "\n"  # Add one line of space after the user entry
    return ldif_content, user_dn

def generate_ldif_file(num_groups, num_users):
    ldif_content = ""

    user_dn_list = []

    # Generate LDIF entries for users
    for i in range(1, num_users + 1):
        user_name = f"user{i}"
        user_ldif, user_dn = generate_user_ldif(user_name)
        ldif_content += user_ldif
        user_dn_list.append(user_dn)

    ldif_content += generate_group_entry()

    # Generate LDIF entries for groups
    for i in range(1, num_groups + 1):
        if i != 1:  # Skip the first group entry (specified group entry)
            group_name = f"Group{i}"
            ldif_content += generate_group_ldif(group_name, user_dn_list)

    return ldif_content

# Get user input for the number of groups and users
num_groups = int(input("Enter the number of groups: "))
num_users = int(input("Enter the number of users: "))

# Generate LDIF content
ldif_content = generate_ldif_file(num_groups, num_users)

# Save LDIF content to a file
with open(get_openldap_data_directory(), "w") as ldif_file:
    ldif_file.write(ldif_content)

print("LDIF file generated successfully.")
