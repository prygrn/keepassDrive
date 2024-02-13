import logging
import io
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# When the scope is changed, the self._token file shall be deleted
# TODO : Be able to change the scope in runtime if the file does not exist
SCOPES = ["https://www.googleapis.com/auth/drive"]

TOKEN_PATH = "./token.json"
LOGGER = logging.getLogger(__name__)


class SecretFileNotFound(Exception):
    """
    Raised when a client secret file is not found
    """

    pass


class TokenFileInvalid(Exception):
    """
    Raised when a token file is invalid
    """

    pass


class DriveIsEmpty(Exception):
    """
    Raised when the given Google Drive is empty
    """


class FileDownloadFailed(Exception):
    """
    Raised when a file has failed to be downloaded
    """


class GDrive:
    _secrets = Path()
    _token = Path(TOKEN_PATH)
    _credentials = None
    _files = list(dict())

    def __init__(self, secrets_file=None) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            level=logging.INFO,
        )

        if secrets_file is not None:
            self._secrets = Path(secrets_file)
        # The file self._token stores the user's access and refresh tokens and
        # is created automatically when the authorization flow completes for
        # the first time.
        if Path(self._token).is_file():
            LOGGER.info(
                f"{str(self._token)} file exists. Get credentials from it.")
            try:
                self._credentials = Credentials.from_authorized_user_file(
                    str(self._token), SCOPES
                )
            except ValueError as error:
                self._credentials = None  # Let the user log in again

        # If there are no (valid) self._credentials, let the user log in
        if not self._credentials or not self._credentials.valid:
            # Token expired and invalid
            if (
                self._credentials
                and self._credentials.expired
                and self._credentials.refresh_token
            ):
                LOGGER.info("Refreshing credentials as tokens expired")
                self._credentials.refresh(Request())
            # No token at all
            else:
                LOGGER.info(
                    "Creating a new workflow as there are no token file")
                # Check if there is any secret file to start the authentication
                # workflow
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self._secrets), SCOPES
                    )
                except (FileNotFoundError, IsADirectoryError) as error:
                    raise SecretFileNotFound("No secret file found")

                self._credentials = flow.run_local_server(port=0)
            # Save the token locally for the next run
            with open(str(self._token), "w") as token:
                token.write(self._credentials.to_json())
            LOGGER.info("Succeeded to write a new token file")

    def download_file(self, file):
        file['is_downloaded'] = False

        try:
            service = build("drive", "v3", credentials=self._credentials)
            request = service.files().get_media(fileId=file["id"])
            binary = io.BytesIO()
            downloader = MediaIoBaseDownload(binary, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            LOGGER.info(f"{file['name']} successfully downloaded")

        except HttpError as error:
            LOGGER.exception(f"An Http Error occurred: {error}")

        LOGGER.info(f"Save {file['name']} in progress")
        with open(file["name"], "wb") as fd:
            fd.write(binary.getvalue())

        file['is_downloaded'] = True

        return file

    def list_files(self):
        # TODO : Using pageToken and also using pageSize token in argument
        try:
            # Print out the 10 first files
            service = build("drive", "v3", credentials=self._credentials)
            response = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)"
            ).execute()
            self._files = response.get("files", [])
            LOGGER.info(f"Get the {10} first files as below")
            LOGGER.info("file id")
            for item in self._files:
                LOGGER.info(f"{item['id']} - {item['name']}")

        except HttpError as error:
            LOGGER.exception(f"An Http Error occurred: {error}")

        return self._files

    def get_file_by_id(self, id):
        for file in self._files:
            if id in file.values():
                return file
        return

    def get_file_by_name(self, name):
        for file in self._files:
            if name in file.values():
                return file
        return

    def search_file_by_name(self, name):
        file = dict()
        files = [dict]
        page_token = None
        try:
            while True:
                service = build("drive", "v3", credentials=self._credentials)
                response = service.files().list(
                    q=f"name='{name}'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token
                ).execute()
                for file in response.get("files", []):
                    if file['name'] == name:
                        return file

                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        # None if not found
        return file
