import logging
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yagdrive import errors
from yagdrive import constants
from yagdrive import authentication

LOGGER = logging.getLogger(__name__)


class Searcher:
    _authenticator = authentication.Authenticator

    def __init__(self, authenticator):
        self._authenticator = authenticator

    def file_by_name(self, name: str):
        file = dict()
        files = [dict]
        page_token = None
        try:
            while True:
                service = build(
                    "drive", "v3", credentials=self._authenticator.get_credentials()
                )
                response = (
                    service.files()
                    .list(
                        q=f"name='{name}'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    if file["name"] == name:
                        LOGGER.info(f"File {file['name']} founded - id = {file['id']}")
                        return file

                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    LOGGER.error(f"File {name} not found in the given Drive")
                    raise errors.NoFileNameError(
                        f"File {name} not found in the given Drive"
                    )

        except HttpError as error:
            LOGGER.critical(error)
            file = None
            raise errors.SearchFileHttpError(error)

        # Not reachable but to fit to the Standards
        return file
