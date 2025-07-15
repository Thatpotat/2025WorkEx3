@echo off

:: Start the server in a new window
start "Server" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingServer.py""

:: Wait 2 seconds for server to initialize
timeout /t 2 > nul

:: Start the first client
start "Client" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingClient.py""

:: Wait 1 second
timeout /t 1 > nul

:: Start the second client
start "Client Copy" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingClient copy.py""

echo All scripts launched.
