call .venv\Scripts\activate.bat
pyinstaller main.py -n "Steamtools Game Uninstaller" -y --collect-all pyfiglet -F
copy ".\dist\Steamtools Game Uninstaller.exe" .\ /Y