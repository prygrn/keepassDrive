from pathlib import Path
import pytest
import json

from yagdrive import errors
from yagdrive import constants
from yagdrive import authentication


@pytest.fixture
def correct_secrets():
    return ".venv/client_secrets.json"


def test___init__(correct_secrets):
    # Pre-test : Deletion of the token file
    token = Path(constants.TOKEN_PATH)
    token.unlink(missing_ok=True)
    # Check there is indeed no token anymore
    assert token.is_file() == False

    # Test no token and no secrets files
    with pytest.raises(errors.SecretFileNotFoundError) as exception:
        authenticator = authentication.Authenticator()
    assert str(exception.value) == "No secret file found"

    # Secrets valid ==> Creating a valid local token file
    authenticator = authentication.Authenticator(secrets_file=correct_secrets)
    assert token.is_file() == True

    # Restart with an invalid token file. To do so, modify the token file
    # ==> Process to a new authentication workflow creating a new valid token file
    with open(str(token), "r") as token_file:
        decoded_token_file = json.load(token_file)
    decoded_token_file["expiry"] = "None"
    with open(str(token), "w") as token_file:
        json.dump(decoded_token_file, token_file)
    authenticator = authentication.Authenticator(secrets_file=correct_secrets)
    assert token.is_file() == True
    with open(str(token), "r") as token_file:
        decoded_token_file = json.load(token_file)
    assert decoded_token_file["expiry"] != "None"
