@echo off

REM Run your Python script
echo Running Python script...
python FileDecider.py

REM Check if the Python script was successful
if %errorlevel% equ 0 (
    echo Python script executed successfully.
    timeout /t 10 > nul

    REM Run Docker Compose
    echo Starting Docker Compose...
    docker-compose -f openldap/docker-compose.yaml up -d

    REM Check if Docker Compose was successful
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
