import logging
import io
from pathlib import Path

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yagdrive import errors
from yagdrive import constants
from yagdrive import authentication

LOGGER = logging.getLogger(__name__)


class Downloader:
    _authenticator: authentication.Authenticator

    def __init__(self, authenticator):
        self._authenticator = authenticator

    def get_file(self, file):
        try:
            service = build(
                "drive", "v3", credentials=self._authenticator.get_credentials()
            )
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
