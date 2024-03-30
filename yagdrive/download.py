import logging
import io
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yagdrive import errors
from yagdrive import constants

LOGGER = logging.getLogger(__name__)


class Downloader:
    def get_file(self, file):
        if not Path(constants.TOKEN_PATH).is_file():
            raise errors.TokenFileInvalidError(
                "Token file is not found in the project root directory"
            )
        try:
            credentials = Credentials.from_authorized_user_file(
                str(constants.TOKEN_PATH), constants.SCOPES
            )
        except ValueError:
            raise errors.TokenFileInvalidError("Invalid token found")

        try:
            service = build("drive", "v3", credentials=credentials)
            request = service.files().get_media(fileId=file["id"])
            binary = io.BytesIO()
            downloader = MediaIoBaseDownload(binary, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            LOGGER.info(f"{file['name']} successfully downloaded")

        except HttpError as error:
            LOGGER.exception(f"An Http Error occurred: {error}")
            raise errors.FileDownloadFailedError(f"File {file} failed to be downloaded")

        # Write binary in the file
        with open(file["name"], "wb") as fd:
            fd.write(binary.getvalue())

        return file
