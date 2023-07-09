@echo off

rem Attiva l'ambiente virtuale (venv)
call venv\Scripts\activate

rem Esegui il file Python specificato
python main.py

rem Disattiva l'ambiente virtuale (venv)
deactivate
PAUSE