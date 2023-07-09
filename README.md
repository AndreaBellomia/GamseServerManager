# GamseServerManager
Manager for non-stanalone servers (Projectzomboid, unterned, minecraftr, factorio...) for all game with portable save

This is a manager for starting a server with your friends without the need for a standalone server.
It allows you to start a server on your PC, but without the constraint that it is always the same person to start it.
Thanks to cloud sharing, the manager will synchronize your save so you don't have to transfer it manually


## Google Settings


- First you need to create a google [developers account](https://developers.google.com/)
- Follow [this guide](https://developers.google.com/workspace/guides/create-credentials) for creating credentials
- Important: create credential for Desktop application
- Download the json credential form APIs & Services > Credentials and rename it to `credentials.json`
- Replace the file with the one in the directory
- Allow Tester user form APIs & Services > OAuth consent screen, Tester users Add User
- Add all google drive accounts that will have access to the file

### Google Drive
- In your Google Drive share Create the folder where to save the Backup
- Copy the folder id using right click
- Paste the id inside the `settings.json file > FOLDER_ID`
- complete the setting file with information `file_names`


## Python
Create a virtual environment
```
python -m venv venv
```
Activate venv
```
./venv/Scripts/activate # Windown
```

Install packagies
```
pip install -r requirements.txt
```

## Startup Manager
Go in `.env` and compile the variable for entrypoint and backup 

SAVE_DIR => Dir want backup
SERVER_BAT => Entry point of the server (file be start for strt game server)
BACKUP_TIME => Time in second for auto Backup
BACKUP => false or true for allow or not the automatic backup (sync with game server backup)

## Start Manager
Insede venv

Firt run
```
python main.py -ntopul -upload dir_want_upload_to_drive
```

Share wit friends
- Github repo
- settings.json
- credentials.json

don't share 
- token.json

Run
```
python main.py

or 

user start.bat
```

Dry run (manager not backup to drive)
```
python main.py -dry
```

Only game server
```
python main.py -dry -notpul
```

Run without pull from drive
```
python main.py -notpul
```