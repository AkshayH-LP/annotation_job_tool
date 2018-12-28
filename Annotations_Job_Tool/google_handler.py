import requests
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from io import BytesIO
from apiclient.http import MediaIoBaseDownload
import csv


folder_id = '1zUUnk1Q-3CG6EzO4LHhNHg66Neceg2VJ'
taxonomy_id = '1SV9Z0eMf0Wo9TaYChYNDtRkdJxZ56OqN'
ontology_id = '1qVH-azHVoo-NX-if8f9WuZIcZnIWDyL2'
team_drive_id = '0AKIigLx7rCqGUk9PVA'
telco = '1ap6878VdJeT1LbU3uO4V1vpxPeGAlG9l'
tmobile = '1KcC8DF6Lcnh3yKJt0-wQQWfBNnvsV6tX'


### 
# Batch4_debug:
## batch4_instructions = '1DepfaW9yaLXttkVBLGh3fX0N9iPct1pn'
## batch
## telco_tmobile_batch4_CITv3
class Google_handler:
    def __init__(self):
        
        # If modifying these scopes, delete the file token.json.
        SCOPES = 'https://www.googleapis.com/auth/drive'
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.drive_service = build('drive', 'v3', http=creds.authorize(Http()))


    #### Download csv from file_id
    def download_file(self, file_id, name, data_type = 'csv'):
        if data_type == 'csv':
            request = self.drive_service.files().get_media(fileId = file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            ### Decode file to format
            text = fh.getvalue().decode("utf-8").split('\n')
            with open('data/' + str(name), 'w') as fp:
                ### Write CSV
                writer = csv.writer(fp, delimiter = ',')
                writer.writerow(text[0].split(','))  # write header
                for row in text[1:]: writer.writerow(row.split(','))
        
        if data_type == 'instructions':
            request = self.drive_service.files().export_media(fileId=file_id,
                                             mimeType='text/html')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            with open('data/' + str(name), "w") as file:
                file.write(fh.getvalue().decode("utf-8"))
        
        return 200

    def upload_file(self, name): 
        request = self.drive_service.files().list().execute()
        return 


    ### Create branch in Tree on Drive for the job
    def create_batch_folder(self, mode, vertical, brand, batch, cit):
        ### Set Ontology or Taxonomy as parent
        if mode == 'taxonomy': parent_id = taxonomy_id
        if mode == 'ontology': parent_id = ontology_id
        
        ### Find the vertical else create it
        vertical_id = self.get_id(vertical, parent_id)
        if vertical_id == 0: vertical_id = self.create_folder(vertical, parent_id)

        ### Find the brand else create it
        brand_id = self.get_id(brand, vertical_id)
        if brand_id == 0: brand_id = self.create_folder(brand, vertical_id)
        
        ### Create components for the Batch
        folders = ['evaluations', 'input_data', 'instructions', 'outputresults']
        for folder in folders:
            body = {'name': str(batch) + "_" +str(cit) + "_" + str(folder), 
                    'mimeType': 'application/vnd.google-apps.folder', 
                    'parents': [brand_id]}
            self.drive_service.files().create(body=body, 
                supportsTeamDrives=True, fields='id').execute()

    ### Get Id of folder with name as name in folder with id == Parent_id
    def get_id(self, name, parent_id = taxonomy_id, data_type = 'folder'):
        if data_type == 'folder':
            mimeType = 'application/vnd.google-apps.folder'
        if data_type == 'csv':
            mimeType = 'application/vnd.google-apps.file'
        if data_type == 'instructions':
            mimeType = 'application/vnd.google-apps.document' 

        query = "name contains '" + str(name) + "' and mimeType = '" +str(mimeType) + "' and '" + str(parent_id) + "' in parents"
        query2 = str(parent_id) + "' in parents"
        response = self.drive_service.files().list(q = query, corpora = 'teamDrive', includeTeamDriveItems = True, teamDriveId = '0AKIigLx7rCqGUk9PVA', supportsTeamDrives = True).execute().get('files', [])
        if len(response) == 0: return 0
        print (response)
        return (response[0].get('id'))

    ### Create folder under folder with id == parent_id
    def create_folder(self, name, parent_id):
        body = {'name': name, 'mimeType': 'application/vnd.google-apps.folder', 
        'parents': [parent_id]}
        return self.drive_service.files().create(body=body,
                supportsTeamDrives=True, fields='id').execute().get('id')
            








