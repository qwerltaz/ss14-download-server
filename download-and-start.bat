py -m venv .venv
".venv\Scripts\python.exe" -m pip install -r requirements.txt

".venv\Scripts\python.exe" main.py

timeout 10