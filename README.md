# GameServerManager
GameServerManager is a backup manager for non-standalone game servers that allows you to load and synchronize game saves on your local drive. It is designed to facilitate sharing and synchronization of game saves between multiple servers, enabling you to play with your friends without the need for a virtual private server (VPS). With GameServerManager, you can start a server on your own PC and allow different people to start it without any constraints. The manager utilizes cloud sharing to automatically synchronize game saves, eliminating the need for manual transfers between servers on different computers.

Please note that this documentation is for a demo script, and it's important to keep track of any fixes or updates in the future. The script author does not take responsibility for data loss, corruption, or regressions that may occur.

## Important Notice
If you find this script useful, please leave a star. In case you encounter any issues with the script, you can open an issue on the project's repository. However, the script author does not provide support for configuration issues with Google Developers. You should follow the standard procedure to obtain the required credentials.

It is essential not to run the script simultaneously with others connected to the same drive file. Running the script concurrently will overwrite the save, and only the last save on the drive will be backed up. To avoid conflicts, coordinate with other users to ensure that only one person at a time opens the script. Currently, there is no centralized system to limit simultaneous openings.

> **Attention:** Script in beta version, you may run into bugs
> 
## Requirements
To use GameServerManager, you need Python version `3.11.2` or higher installed on your system.

## Google Settings
> **Attention:** The `credentials.json` file is a sensitive file that gives partial access to your google cloud app, share it only with those who must use the app (access is limited by the drive system but be careful :))

Before using the script, you need to configure Google settings to enable access to Google Drive. Follow these steps:
1. Create a Google Developers account at https://developers.google.com/.
2. Refer to [this guide](https://developers.google.com/workspace/guides/create-credentials?hl=it) for instructions on creating credentials.
3. When creating credentials, make sure to select the "Desktop application" option.
4. Download the JSON credential file from the `APIs & Services > Credentials` section and rename it to `credentials.json`.
5. Copy the `credentials.json` file in the script directory. 
6. Allow Tester users from the `APIs & Services > OAuth consent screen` section by adding user emails.
7. Add all the Google Drive accounts that will have access to the backup folder.

## Google Settings
> **Attention:** The generated `token.json` file is a sensitive file that gives you full access to your Google Drive, do not share it with **anyone**, each script auto-generates its own after authentication with google OAuth.
> To generate the `token.json` file, remember to add the account to the test accounts and share the file with the user via Google drive.

To configure Google Drive for use with GameServerManager, follow these steps:
1. In your Google Drive, create a folder where you want to save the game backups.
2. Right-click on the created folder and copy the folder ID.
3. Open the `settings.json` file in the script directory and paste the folder ID into the `FOLDER_ID` field.
4. Complete the settings file with the necessary information, such as file_names.

## Python Setup

Create a virtual environment using the following command:
```bash
python -m venv venv
```

Activate the virtual environment. The activation command may vary depending on your operating system:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Install the required packages using the following command:
```bash
pip install -r requirements.txt
```
## Startup Manager
Inside the .env file, you need to configure the following variables for the entry point and backup
- `SAVE_DIR`: The directory where you want to store the backups.
- `SERVER_BAT`: The entry point of the game server (the file to start the game server).
- `BACKUP_TIME`: The time interval in seconds for automatic backups.
- `BACKUP`: Set this variable to false or true to enable or disable automatic backups (synchronization with the game server backup).

## Starting GameServerManager
To start GameServerManager, follow these steps:

Make sure you are inside the virtual environment (if not, activate it).
For the first run, use the following command:
```bash
python main.py -ntopul -upload <dir_want_upload_to_drive>
```
1. Share the following with your friends:
   - GitHub repository
   - `settings.json` file
   - `credentials.json` file
  
     Do not share the token.json file.


To run the script, use the following command:
```bash
python main.py
```
Alternatively, you can create a `start.bat` file with the command `python main.py` and run the batch file.

### Additional Options

- To perform a dry run without actually backing up to Google Drive, use the following command:
```bash
python main.py -dry
```
- To run only the game server without pulling backups from Google Drive, use the following command:
```bash
python main.py -dry -notpul
```
- To run the script without pulling backups from Google Drive, use the following command:
```bash
python main.py -notpul
```

