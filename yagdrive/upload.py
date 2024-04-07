import logging
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from yagdrive import errors
from yagdrive import constants
from yagdrive import authentication

LOGGER = logging.getLogger(__name__)


class Uploader:
    _authenticator = authentication.Authenticator

    def __init__(self, authenticator):
        self._authenticator = authenticator

    def push_file(self, file):
        uploaded_file = None
        try:
            service = build(
                "drive", "v3", credentials=self._authenticator.get_credentials()
            )
            file_metadata = {"name": file["name"]}
            media = MediaFileUpload(file["name"], mimetype="application/octet-stream")
            uploaded_file = (
                service.files()
                .update(
                    body=file_metadata,
                    media_body=media,
                    fileId=file["id"],
                    fields="id, name",
                )
                .execute()
            )
            LOGGER.info(
                f"Uploaded file name {uploaded_file['name']} - id {uploaded_file['id']}"
            )
        except HttpError as error:
            uploaded_file = None
            raise errors.UpdateFileHttpError(error)

        return uploaded_file
