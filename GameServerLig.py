from io import BytesIO
import os
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from zipfile import ZipFile, ZIP_DEFLATED

import logging


class GoogleService:
    def __init__(self, json_file, file_dir):
        self.json_file = json_file
        self._data = self._get_settings(self.json_file)
        self.CLIENT_SECRET_FILE = self._data["CLIENT_SECRET_FILE"]
        self.API_SERVICE_NAME = self._data["API_NAME"]
        self.API_VERSION = self._data["API_VERSION"]
        self.SCOPES = self._data["SCOPES"][0]
        self.pickle_file = f'token_{self.API_SERVICE_NAME}_{self.API_VERSION}.pickle'
        self.cred = self._get_credentials()
        self.service = self._build_service()
        self.file_dir = file_dir

    def _get_settings(self, json_file):
        with open(json_file, "r") as settings:
            return json.load(settings)

    def _get_credentials(self):
        
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not creds or not creds.valid:
            if creds  and creds.expired and creds .refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CLIENT_SECRET_FILE, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds .to_json())
                
        return creds 

    def _build_service(self):
        try:
            if self.cred:
                return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=self.cred)
            else:
                raise Exception("Invalid credentials.")
        except Exception as e:
            logging.error('Unable to connect.')
            logging.error(e)
            return None

    def get_service(self):
        if self.service:
            return self.service
        raise Exception("Service not built")

    def create_file(self, raw_file):
        file_metadata = {
            'name': self._data["file_names"],
            'parents': [self._data["FOLDER_ID"]]
        }
        media = MediaIoBaseUpload(raw_file, mimetype=self._data["mime_types"])
        file = self.get_service().files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()
        return file
    
    def update_json(self, file):
        self._data["file_id"] = file["id"]
        with open(self.json_file, "w") as settings:
            json.dump(self._data, settings)

    def update_file(self, raw_file):
        if not self._data["file_id"]:
            file = self.create_file(raw_file)
            self.update_json(file)
            
        if self._data["file_id"]:
            media = MediaIoBaseUpload(raw_file, mimetype=self._data["mime_types"])
            file_metadata = {
                'name': self._data["file_names"],
            }
            file = self.get_service().files().update(
                body=file_metadata,
                media_body=media,
                fileId=self._data["file_id"]
            ).execute()
        else:
            raise Exception("Error while getting file ID")

    def download_file(self):
        if self._data["file_id"]:
            request = self.get_service().files().get_media(fileId=self._data["file_id"])
            fh = BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                logging.info(f'Download progress: {status.progress() * 100}')
            fh.seek(0)
            if not os.path.exists(self.file_dir):
                os.makedirs(self.file_dir)
            
            return fh
        else:
            raise Exception("Error while getting file ID")



class VistualZip:
    
    ZIP_DATA = BytesIO()
    
    ZIP_CREATED = False
    
    def __init__(self, dir_name):
        self.dir = dir_name
        
        self._create_virtual_zip()
        
    def _create_virtual_zip(self):
        try:
            with ZipFile(self.ZIP_DATA, 'w', ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(self.dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, self.dir))
            self.ZIP_CREATED = True
        except Exception as e:
            raise Exception(e)

    def get_zip(self):
        if self.ZIP_CREATED:
            return self.ZIP_DATA
        raise Exception("ERROR: Zip not Created")
    
    def save_zip(self, raw_zip):
        with ZipFile(raw_zip, 'r') as zip_ref:
            zip_ref.extractall(self.dir)