from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/drive"
]  # Check the API scopes to get the appropriate scope

FILENAME = "Database.kdbx"
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


def main():
    credentials = None
    token_path = Path(TOKEN_FILE)
    credentials_path = Path(CREDENTIALS_FILE)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if Path(token_path).is_file():
        credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    # If there are no (valid) credentials, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the token locally for the next run
        with open(str(token_path), "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("drive", "v3", credentials=credentials)

        # Call the Drive API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
    except HttpError as error:
        # Handle errors from Gmail API
        print(f"An error occurred: {error}")
        
    items = results.get("files", [])

    if not items:
        print("No files found.")
        print("Creating file")
        create_file()
        return

    # Filter items on FILENAME
    # TODO Try to filter through the API to reduce consumption and improve performance
    file_metadata = [dict(name = item['name'], id = item['id']) for item in items if item['name'] == FILENAME]
    if not file_metadata:
        print("Creating file")
        create_file()
    else:
        update_file(file_metadata[0])
        print(f"{FILENAME} present, just need to be updated")

def update_file(file_metadata):
    pass

def create_file():
    pass

if __name__ == "__main__":
    main()