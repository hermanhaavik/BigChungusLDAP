# Use the official Python image as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required dependencies
RUN apt-get update \
    && apt-get install -y libldap2-dev libsasl2-dev slapd ldap-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Expose the LDAP port
EXPOSE 389

# Start the LDAP server
CMD ["slapd", "-d", "0", "-u", "openldap", "-g", "openldap"]
