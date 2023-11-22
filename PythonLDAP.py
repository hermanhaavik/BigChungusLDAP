import ldap 
from ldap import modlist
import random
import string


# Function to generate a random string
def generate_random_string(length=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to generate a fake user entry
def generate_fake_user_entry(username):
    user_dn = f"cn={username},dc=example,dc=com"
    user_attrs = {
        'objectClass': ['top', 'person'],
        'cn': [username],
        'sn': [generate_random_string()],
        'userPassword': [generate_random_string()]
    }
    return user_dn, user_attrs

# Function to add a fake user to the LDAP server
def add_fake_user(ld, username):
    user_dn, user_attrs = generate_fake_user_entry(username)
    ld.add_s(user_dn, modlist.addModlist(user_attrs))

# Function to start the fake LDAP server
def start_fake_ldap_server():
    try:
        # Initialize LDAP server
        server = ldap.initialize("ldap://localhost:389")

        # Bind as admin (modify this based on your setup)
        server.simple_bind_s("cn=admin,dc=nodomain", "admin")



        # Add fake users (modify as needed)
        for i in range(1, 6):
            add_fake_user(server, f"user{i}")

        # Unbind and close the connection
        server.unbind_s()

        print("Fake LDAP server started successfully.")
    except ldap.LDAPError as e:
        print(f"Error starting fake LDAP server: {e}")

if __name__ == "__main__":
    start_fake_ldap_server()