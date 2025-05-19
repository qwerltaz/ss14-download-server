py -m venv .venv
".venv\Scripts\python.exe" -m pip install -r requirements.txt

".venv\Scripts\python.exe" main.py

start "Robust server" "%userprofile%\Downloads\SS14.Server_win-x64\Robust.Server.exe"
start "" "steam://rungameid/1482520"
timeout 10