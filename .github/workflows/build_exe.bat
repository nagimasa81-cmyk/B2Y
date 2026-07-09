@echo off
pip install pyinstaller >nul
pyinstaller --onefile --windowed BAT2YML.py
pause
