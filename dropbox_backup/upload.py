import sys
import argparse
import requests
import os

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TIMEOUT = 900
CHUNK_SIZE = 4 * 1024 * 1024
BASE_URL = "http://hassio/"


# Get the hassio token for authentication.
def get_headers():
    return {"X-HASSIO-KEY": os.environ.get("HASSIO_TOKEN")}


# Uploads a file to Dropbox
def upload_file(dbx, file, target):

    # Open the file
    with open(file, 'rb') as f:

        try:
            print("[INFO] Uploading '" + file + "' to Dropbox as '" + target + "'.")

            # Get file size
            file_size = os.path.getsize(file)

            # Use normal upload method if file is small.
            if file_size <= CHUNK_SIZE:

                print("[DEBUG] Using simple uploader.")

                # Use normal upload method if file is small.
                dbx.files_upload(f.read(), target, mode=WriteMode('add'))

            else:

                print("[DEBUG] Using upload session.")

                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=f.tell())
                commit = dropbox.files.CommitInfo(path=target)

                while f.tell() < file_size:

                    if (file_size - f.tell()) <= CHUNK_SIZE:
                        dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)

                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                        cursor.offset = f.tell()

        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and err.error.get_path().reason.is_insufficient_space()):
                sys.exit("[ERROR] Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


# Take backups from hass and define set paths.
def make_backup_path(hass_backup_list, output_dir, preserve_filename):

    upload_list = []

    for hass_backup in hass_backup_list:

        # Add extension and folder to path.
        source = hass_backup['slug'] + ".tar"
        source = os.path.join('backup', source)

        # Choose new file name
        if preserve_filename is True:
            target = hass_backup['slug'] + ".tar"
        else:
            target = hass_backup['name'] + ".tar"

        # Add target folder to path
        target = os.path.join(output_dir, target)

        # Add to list
        output = {'source': source, 'target': target}
        upload_list.append(output)

    return upload_list


def main(token, output_dir, preserve_filename):

    # Check for an access token
    if (len(token) == 0):
        sys.exit("[ERROR] Looks like you didn't add your access token.")

    # Get hass headers.
    my_headers = get_headers()

    # Get backup name and information as a list of dicts.
    backup_info = requests.get(BASE_URL + "backups", headers=my_headers)
    backup_info.raise_for_status()
    hass_backup_list = backup_info.json()["data"]["backups"]

    # Format the file paths
    upload_list = make_backup_path(hass_backup_list, output_dir, preserve_filename)

    # Check if there are any files to upload
    if (len(upload_list) == 0):
        sys.exit("[INFO] No files found to upload.")
    else:
        print("[INFO] Found", len(upload_list), "file(s) to upload.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("[DEBUG] Creating a Dropbox object.")
    with dropbox.Dropbox(token, timeout=TIMEOUT) as dbx:

        # Check that the access token is valid.
        try:
            dbx.users_get_current_account()
        except AuthError:
            sys.exit("[ERROR] Invalid access token; try re-generating an access token from the app console on the web.")

        # Upload all files.
        for backup in upload_list:
            upload_file(dbx, backup['source'], backup['target'])

        print("[INFO] Completed upload(s).")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Upload hassio backups.")

    parser.add_argument("token", type=str, help="Dropbox OAuth2 access token.")
    parser.add_argument("output_dir", type=str, help="Output directory.")
    parser.add_argument("preserve_filename", type=str, help="Preserve original backup filename.")

    args = parser.parse_args()
    main(args.token, args.output_dir, args.preserve_filename)
