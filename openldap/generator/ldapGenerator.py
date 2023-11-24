import random
import string
import os

def generate_random_user(uid):
    user = {
        'dn': f"cn={uid},ou=Users,dc=example,dc=org",
        'changetype': 'add',
        'objectclass': ['inetOrgPerson'],
        'cn': [uid],
        'givenname': [f'GivenName_{uid}'],
        'sn': [f'Surname_{uid}'],
        'displayname': [f'DisplayName_{uid}'],
        'mail': [f'{uid}@example.com'],
        'uid': [uid],
        'userpassword': [f'{uid}_pass']
    }
    return user

def generate_random_group(cn, unique_members):
    group = {
        'dn': f"cn={cn},ou=Groups,dc=example,dc=org",
        'changetype': 'add',
        'objectclass': ['organizationalUnit', 'groupOfUniqueNames'],
        'cn': [cn],
        'ou': [f'{cn}_OU'],
        'uniqueMember': unique_members
    }
    return group

def generate_random_data(num_users, num_groups):
    users = [generate_random_user(f'user{i}') for i in range(1, num_users + 1)]
    groups = [
        generate_random_group('Admins', [f'cn=admin_gh,ou=Users,dc=example,dc=org']),
        generate_random_group('Maintainers', [f'cn=maintainer,ou=Users,dc=example,dc=org', f'cn=developer,ou=Users,dc=example,dc=org']),
    ]
    return users, groups

def write_ldif_file(entries, output_file):
    with open(output_file, 'w') as ldif_file:
        for entry in entries:
            ldif_file.write(f"dn: {entry['dn'][0]}\n")
            ldif_file.write(f"changetype: {entry['changetype']}\n")
            for key, values in entry.items():
                if key not in ['dn', 'changetype']:
                    for value in values:
                        ldif_file.write(f"{key}: {value}\n")
            ldif_file.write("\n")

# Get the absolute path of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the data directory path outside of the generator directory
data_directory = os.path.join(script_directory, "..", "data")

# Ensure the data directory exists
os.makedirs(data_directory, exist_ok=True)

# Example usage:
num_users = 3
num_groups = 2
output_ldif_file = os.path.join(data_directory, "generated_data.ldif")

users_data, groups_data = generate_random_data(num_users, num_groups)
all_entries = users_data + groups_data
write_ldif_file(all_entries, output_ldif_file)

print(f"LDIF file '{output_ldif_file}' generated successfully.")
