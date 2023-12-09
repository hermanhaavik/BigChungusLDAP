@echo off

:: Run your Python script
echo Running Python script...
python FileDecider.py

:: Check if the Python script was successful
if %errorlevel% equ 0 (
    echo Python script executed successfully.
    timeout /nobreak /t 10 >nul

    :: Prompt user for LDAP admin password
    set /p "ldap_admin_password=Enter the LDAP admin password (default is admin_pass): "
    set "ldap_admin_password=%ldap_admin_password:-admin_pass%"

    :: Export the LDAP admin password as an environment variable
    set "LDAP_ADMIN_PASSWORD=%ldap_admin_password%"

    :: Prompt user for input
    set /p "ldap_host_port=Enter the host port for LDAP server (default is 389): "
    set "ldap_host_port=%ldap_host_port:-389%"

    :: Export the host and container ports as environment variables
    set "LDAP_HOST_PORT=%ldap_host_port%"

    :: Run Docker Compose with environment variables
    echo Starting Docker Compose...
    set "LDAP_ADMIN_PASSWORD=%LDAP_ADMIN_PASSWORD%" set "LDAP_HOST_PORT=%LDAP_HOST_PORT%" docker-compose -f openldap/docker-compose.yaml up -d

    :: Check if Docker Compose was successful
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
