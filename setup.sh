#!/bin/bash
echo "Starting script"
# Build the Docker image
docker build -t ldap-server .
echo "Docker image built"

# Run the Docker container, exposing port 389
docker run -d -p 389:389 --name ldap-container ldap-server
echo "Docker container is running, exposing port  389"

# Wait for the LDAP server to start
echo "Waiting for LDAP server to start..."
sleep 10

echo "Trying to run the python script"
# Run the Python script within the Docker container
docker exec ldap-container /usr/bin/env /usr/local/bin/python /app/PythonLDAP.py
echo "Python script is running"

#
# Cleanup: Stop and remove the Docker container
#docker stop ldap-container
#docker rm ldap-container
