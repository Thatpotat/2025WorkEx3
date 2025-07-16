@echo off

:: Start the server
start "ServerWindow" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingServer.py""

start "Client1" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingClient.py""

start "Client2" cmd /c ""C:\Users\claus\scoop\apps\python\3.13.5\python.exe" "C:\Users\claus\OneDrive\Documents\WEX\2025WorkEx3\Network\TestingClient.py""

echo All scripts launched.
