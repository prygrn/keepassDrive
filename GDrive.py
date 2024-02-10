import logging
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# When the scope is changed, the self._token file shall be deleted
# TODO : Be able to change the scope in runtime if the file does not exist
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

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


class GDrive:
    _secrets = Path()
    _token = Path(TOKEN_PATH)
    _credentials = None

    def __init__(self, secrets_file=None) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
            level=logging.INFO,
        )

        self._secrets = secrets_file
        # The file self._token stores the user's access and refresh tokens and is created
        # automatically when the authorization flow completes for the first time.
        if Path(self._token).is_file():
            LOGGER.info(f"{str(self._token)} file exists. Get credentials from it.")
            try:
                self._credentials = Credentials.from_authorized_user_file(
                    str(self._token), SCOPES
                )
            except ValueError as error:
                self._credentials = None # Let the user log in again

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
                LOGGER.info("Creating a new workflow as there are no token file")
                # Check if there is any secret file to start the authentication workflow
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self._secrets), SCOPES
                    )
                except FileNotFoundError as error:
                    raise SecretFileNotFound("No secret file found")

                self._credentials = flow.run_local_server(port=0)
            # Save the token locally for the next run
            with open(str(self._token), "w") as token:
                token.write(self._credentials.to_json())
            LOGGER.info("Succeeded to write a new token file")

    def get_file(id):
        pass

    def get_files():
        pass
