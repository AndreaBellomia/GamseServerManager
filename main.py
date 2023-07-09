

import time
import threading
import logging
import multiprocessing
import subprocess
import sys
import os

from dotenv import load_dotenv
from GameServerLig import VistualZip, GoogleService


logging_format = logging.Formatter('[%(name)s] [%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] : %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
# logging.basicConfig(level=logging.NOTSET, format=logging_format)

file_handler = logging.FileHandler('logfile.log')
file_handler.setLevel(logging.NOTSET)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.NOTSET)

file_handler.setFormatter(logging_format)
console_handler.setFormatter(logging_format)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

load_dotenv()


SAVE_DIR = os.environ['SAVE_DIR']
SERVER_BAT = os.environ['SERVER_BAT']
stop_event = threading.Event()
google_service = GoogleService("settings.json", SAVE_DIR)


def auto_backup():
    logger.info("Backup Started!")
    is_enabled  = True if os.environ['BACKUP'].lower() == 'true' or os.environ['BACKUP'].lower() == '1' else False
    while is_enabled:
        time.sleep(os.environ['BACKUP_TIME'])
        logger.info("Backup start...")
        zip_data = VistualZip(SAVE_DIR).get_zip()
        logger.debug("Uploading %s byte to drive" % (zip_data.getbuffer().nbytes))
        google_service.update_file(zip_data)
        logger.info("Backup completed!")
    
    
if __name__ == "__main__":
    
    print("""
############################################################################################################################################
  .--.   .----..-.  .-..-. .-. .---.        .----..----..----. .-. .-..----..----.    .-.   .-.  .--.  .-. .-.  .--.   .---. .----..----.  
 / {} \ { {__   \ \/ / |  `| |/  ___}      { {__  | {_  | {}  }| | | || {_  | {}  }   |  `.'  | / {} \ |  `| | / {} \ /   __}| {_  | {}  } 
/  /\  \.-._} }  }  {  | |\  |\     }      .-._} }| {__ | .-. \\\ \_/ /| {__ | .-. \   | |\ /| |/  /\  \| |\  |/  /\  \\\  {_ }| {__ | .-. \ 
`-'  `-'`----'   `--'  `-' `-' `---'       `----' `----'`-' `-' `---' `----'`-' `-'   `-' ` `-'`-'  `-'`-' `-'`-'  `-' `---' `----'`-' `-' 

                                    Project Zomboid Server manager for not standalone server saving                                    
                                                             
                                                              Version 0.1
            
############################################################################################################################################
    
    ## Manager for Sync Bakup with Google Cloud API
    - Sync server save to google drive for share with friends
    
    ## Before start
    Remeber update settings.json and .env with the information required 
    for more info consult the github repository https://www.google.com
    
    ## Commands
    python main.py -notpul (for not pull for drive at the start)
    python main.py -upload dir_of_file (for uload file to drive and update settings)
    """)
    
    print("Loading...")
    
    time.sleep(3)
    
    print("""
          
          
          
          """)
    
    
    if "-notpul" not in sys.argv:
        logger.debug("Download backup form drive")
        row_file = google_service.download_file()
        logger.debug("File decompressing...")
        VistualZip(SAVE_DIR).save_zip(row_file)
    
    if "-dry" in sys.argv:
        
        logger.info("Game server startin...")
        logger.info("Bat exec %s" % (SERVER_BAT))
        subprocess.call(['cmd', '/c', SERVER_BAT])
        
        logger.warning("Gamse server stoped")
        
    else: 
        if "-upload" in sys.argv:
            upload_dir = sys.argv[sys.argv.index("-upload") + 1]
            
            logger.warning("Upload file from %s, tuo the drive" % (upload_dir))
            user_upload = input("are you sure (y/n): ")
            if user_upload.upper() == "Y":
                logger.debug("File compressing...")
                zip_data = VistualZip(upload_dir).get_zip()
                logger.debug("Uploading %s byte to drive" % (zip_data.getbuffer().nbytes))
                file = google_service.create_file(zip_data)
                logger.info("File generated with id: %s" % (file["id"]))
                google_service.update_json(file)
            else:
                logger.warning("Upload file to drive skipped")  
        
        is_enabled  = True if os.environ['BACKUP'].lower() == 'true' or os.environ['BACKUP'].lower() == '1' else False
        if is_enabled:
            logger.debug("Starting Thread for Auto Backup")
            proc = multiprocessing.Process(target=auto_backup, args=())
            proc.start()
        
        logger.info("Game server startin...")
        logger.info("Bat exec %s" % (SERVER_BAT))
        subprocess.call(['cmd', '/c', SERVER_BAT])
        
        logger.warning("Gamse server stoped")
        if is_enabled:
            proc.kill()
        
        logger.debug("File compressing...")
        zip_data = VistualZip(SAVE_DIR).get_zip()
        logger.debug("Uploading %s byte to drive" % (zip_data.getbuffer().nbytes))
        google_service.update_file(zip_data)
        logger.debug("Save complete")
        
        
        time.sleep(3)
    
