import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from yagdrive import errors
from yagdrive import constants

LOGGER = logging.getLogger(__name__)


class Authenticator:
    _token = Path(constants.TOKEN_PATH)
    _credentials = None

    def __init__(self, secrets_file=None) -> None:
        _token = Path(constants.TOKEN_PATH)

        # The file self._token stores the user's access and refresh tokens and
        # is created automatically when the authorization flow completes for
        # the first time.
        if Path(self._token).is_file():
            LOGGER.info(f"{str(self._token)} file exists. Get credentials from it.")
            try:
                self._credentials = Credentials.from_authorized_user_file(
                    str(self._token), constants.SCOPES
                )
            except ValueError:
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
                LOGGER.info("Creating a new workflow as there are no token file")
                # Check if there is any secret file to start the authentication
                # workflow
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(secrets_file), constants.SCOPES
                    )
                except (FileNotFoundError, IsADirectoryError):
                    raise errors.SecretFileNotFoundError("No secret file found")

                self._credentials = flow.run_local_server(port=0)
            # Save the token locally for the next run
            with open(str(self._token), "w") as token:
                token.write(self._credentials.to_json())
            LOGGER.info("Succeeded to write a new token file")

    def get_credentials(self):
        return self._credentials
