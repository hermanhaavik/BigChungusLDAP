@echo off

rem Check for the presence of pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
  echo pip not found, installing...
  rem Install pip (Python package manager)
  python -m ensurepip --default-pip
)

rem Install project dependencies using pip
rem Replace the following command with the actual command for your project
pip install -r requirements.txt

rem Additional commands for setting up the project, if needed

rem Print a message indicating that the script has completed
echo Project dependencies installed successfully!

rem Stop existing Docker Compose containers
echo Stopping existing Docker Compose containers...
docker-compose -f openldap/docker-compose.yaml down

rem Check if Docker Compose down was successful
if %errorlevel% equ 0 (
    echo Docker Compose containers stopped successfully.
) else (
    echo Error: Failed to stop Docker Compose containers.
    exit /b 1
)

rem Run your Python script
echo Running Python script...
python FileDecider.py

rem Check if the Python script was successful
if %errorlevel% equ 0 (
    echo Python script executed successfully.
    timeout /t 10 /nobreak >nul

    rem Prompt user for LDAP admin password
    set /p "ldap_admin_password=Enter the LDAP admin password (default is admin_pass): "
    set "ldap_admin_password=%ldap_admin_password:-admin_pass%"

    rem Export the LDAP admin password as an environment variable
    set "LDAP_ADMIN_PASSWORD=%ldap_admin_password%"

    rem Prompt user for input
    set /p "ldap_host_port=Enter the host port for LDAP server (default is 389): "
    set "ldap_host_port=%ldap_host_port:-389%"

    rem Export the host and container ports as environment variables
    set "LDAP_HOST_PORT=%ldap_host_port%"

    rem Run Docker Compose with environment variables
    echo Starting Docker Compose...
    set "LDAP_ADMIN_PASSWORD=%LDAP_ADMIN_PASSWORD%" & set "LDAP_HOST_PORT=%LDAP_HOST_PORT%" & call docker-compose -f openldap/docker-compose.yaml up -d

    rem Check if Docker Compose was successful
    if %errorlevel% equ 0 (
        echo Docker Compose started successfully.
    ) else (
        echo Error: Failed to start Docker Compose.
        exit /b 1
    )
) else (
    echo Error: Failed to execute Python script.
    exit /b 1
)

exit /b 0
