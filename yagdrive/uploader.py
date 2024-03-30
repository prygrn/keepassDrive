import logging
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from yagdrive import errors
from yagdrive import constants

LOGGER = logging.getLogger(__name__)


class Uploader:
    def push_file(self, file):
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

        uploaded_file = None
        try:
            service = build("drive", "v3", credentials=credentials)
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
