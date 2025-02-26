@echo off
echo Starting...
echo If this is your first time starting up, please have patience!
echo This may take some time.
ping -n 3 127.0.0.1 >nul
echo Installing modules...
python -m pip install -r requirements.txt
echo Starting!
start "" pythonw main.py
