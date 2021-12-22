import sys
import argparse
import glob
import os

import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

TIMEOUT = 900
CHUNK_SIZE = 4 * 1024 * 1024


# Uploads a file to Dropbox
def upload_file(dbx, file, target):

    # Open the file
    with open(file, 'rb') as f:

        try:
            print("[INFO] Uploading " + file + " to Dropbox as " + target + "...")

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


# Uploads all files to the root folder
def upload_files(dbx, files, output_dir):

    for file in files:
        target = os.path.join(output_dir, os.path.basename(file))
        upload_file(dbx, file, target)


# Ensure the outputh dir path is as expected
def parse_dir(path):

    if path == '/' or path == '//' or len(path) == 0:
        return '/'

    if path[0] != '/':
        path = '/' + path

    if path[-1] != '/':
        path = path + '/'

    return path


def main(token, output_dir):

    # Check for an access token
    if (len(token) == 0):
        sys.exit("[ERROR] Looks like you didn't add your access token.")

    # Get the list of files to upload.
    file_list = glob.glob('backup/*.tar', recursive=True)

    if (len(file_list) == 0):
        sys.exit("[INFO] No files found to upload.")

    print("[INFO] Found", len(file_list), "file(s) to upload.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("[DEBUG] Creating a Dropbox object.")
    with dropbox.Dropbox(token, timeout=TIMEOUT) as dbx:

        # Check that the access token is valid.
        try:
            dbx.users_get_current_account()
        except AuthError:
            sys.exit("[ERROR] Invalid access token; try re-generating an access token from the app console on the web.")
        # Correct the output directory path.
        output_dir = parse_dir(output_dir)

        # Upload files.
        upload_files(dbx, file_list, output_dir)

        print("[INFO] Completed upload(s).")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Upload hassio backups.")

    parser.add_argument("token", type=str, help="Dropbox OAuth2 access token.")
    parser.add_argument("output_dir", type=str, help="Output directory.")

    args = parser.parse_args()
    main(args.token, args.output_dir)
