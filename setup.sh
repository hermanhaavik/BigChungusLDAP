#!/bin/bash

# Stop existing Docker Compose containers
echo "Stopping existing Docker Compose containers..."
docker-compose -f openldap/docker-compose.yaml down

# Check if Docker Compose down was successful
if [ $? -eq 0 ]; then
    echo "Docker Compose containers stopped successfully."
else
    echo "Error: Failed to stop Docker Compose containers."
    exit 1
fi

# Run your Python script
echo "Running Python script..."
python3 FileDecider.py

# Check if the Python script was successful
if [ $? -eq 0 ]; then
    echo "Python script executed successfully."
    sleep 10

    # Prompt user for LDAP admin password
    read -sp "Enter the LDAP admin password (default is admin_pass): " ldap_admin_password
    ldap_admin_password=${ldap_admin_password:-admin_pass}

    # Export the LDAP admin password as an environment variable
    export LDAP_ADMIN_PASSWORD=$ldap_admin_password

    # Prompt user for input
    read -p "Enter the host port for LDAP server (default is 389): " ldap_host_port
    ldap_host_port=${ldap_host_port:-389}

    # Export the host and container ports as environment variables
    export LDAP_HOST_PORT=$ldap_host_port

    # Run Docker Compose with environment variables
    echo "Starting Docker Compose..."
    LDAP_ADMIN_PASSWORD=$LDAP_ADMIN_PASSWORD LDAP_HOST_PORT=$LDAP_HOST_PORT docker-compose -f openldap/docker-compose.yaml up -d

    # Check if Docker Compose was successful
    if [ $? -eq 0 ]; then
        echo "Docker Compose started successfully."
    else
        echo "Error: Failed to start Docker Compose."
        exit 1
    fi
else
    echo "Error: Failed to execute Python script."
    exit 1
fi

exit 0
