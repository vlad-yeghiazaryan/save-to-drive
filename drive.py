# Setup
import os
from urllib.error import HTTPError
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pathlib
path = pathlib.Path(__file__).parent.resolve()


# References
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(
    path, 'client_secrets.json')
credentials = os.path.join(path, 'credentials.json')


def save_credentials(gauth):
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(credentials)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(credentials)


def save_to_dir(drive, directory_id, filePath):
    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format(directory_id)}).GetList()
    file_id = None

    for x in range(len(file_list)):
        if file_list[x]['title'] == filePath:
            file_id = file_list[x]['id']

    file1 = drive.CreateFile(
        {'id': file_id, 'parents': [{'id': directory_id}]})
    file1.SetContentFile(filePath)
    file1.Upload()

# this method should create a directory tree, from a string like '2017/06/14'


def create_drive_folder(drive, path):
    # this method should create a folder with the given parents
    # at first it is called with root as parent, for the 2017 folder
    # and when the 06 folder should be created it gets [root and the successfully created 2017 folder id]
    def create_drive_folder_level(filename, parents):
        dirs = drive.ListFile(
            {'q': "'{}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'".format(parents[-1]['id'])})
        try:
            # this will give me the parent folder, if it exists
            current = [x for x in list(dirs)[0] if x['title'] == filename][0]
        except (HTTPError, IndexError):
            current = None
        if not current:
            meta = {'title': filename, 'parents': [
                parents[-1]], 'mimeType': 'application/vnd.google-apps.folder'}
            current = drive.CreateFile(meta)
            current.Upload({'convert': True})
            return current
        return current

    path = path.split('/')
    p = [dict(id='root')]
    for folder in path:
        p.append(create_drive_folder_level(folder, p))
    return p

# drivePath: API/SavedData
# filePath: 'data.csv'


def saveToDrive(drivePath, filePath):
    # Setup
    gauth = GoogleAuth()

    # Save Credentials
    save_credentials(gauth)

    # Login to google drive
    drive = GoogleDrive(gauth)

    # Create a directory
    folders = create_drive_folder(drive, drivePath)
    dir = folders[-1]

    # save file in that directory
    save_to_dir(drive, dir['id'], filePath)
