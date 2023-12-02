#!/bin/bash

# Run your Python script
echo "Running Python script..."
python3 FileDecider.py


# Check if the Python script was successful
if [ $? -eq 0 ]; then
    echo "Python script executed successfully."
    sleep 10

    # Run Docker Compose
    echo "Starting Docker Compose..."
    docker-compose -f openldap/docker-compose.yaml up -d


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
