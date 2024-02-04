# Keepass automatic launcher with Google Drive

This tool automatically downloads your keepass database from your Google Drive and opens it to be ready to be consulted.
When exiting, it will check if there is any differences between the remote and the local ones. If any, it will upload the local to the remote to be up-to-date.

**Be warned that this tool shall be used with care as it uses some environment variables such as your db password and Google OAuth client secret in argument.**

## Prerequisites
1. Having keepass [Get it here](https://keepass.info/index.html)
2. `curl` installed
3. Credentials created ("OAuth client ID" - "TVs and Limited Input devices") from [Google Cloud Platform](https://console.cloud.google.com/apis/credentials)
   This step allows you to get your CLIENT_ID and CLIENT_SECRET

## Installation
1. Clone this repository
2. Setup your database path and password into the following environment variables
    * `KEEPASS_DB_URL` i.e. `echo "export KEEPASS_DB_URL=<your_db_url> >> .bashrc"`
    * `KEEPASS_DB_PWD` i.e. `echo "export KEEPASS_DB_PWD=<your_db_pwd> >> .bashrc"`
    * `CLIENT_ID` i.e. `echo "export CLIENT_IDL=<your_id> >> .bashrc"`
    * `CLIENT_SECRET` i.e. `echo "export CLIENT_SECRET=<your_secret> >> .bashrc"`
    * Source the file `source ~/.bashrc`
3. You can now give it a try ;)

## Known Issues
### Application Type
For security reasons, we used OAuth 2.0 with Limited Input Devices. Indeed, the [allowed scopes](https://developers.google.com/identity/protocols/oauth2/limited-input-device?hl=en#allowedscopes) of this type of client ID for the Google Drive API are:
* https://www.googleapis.com/auth/drive.appdata
* https://www.googleapis.com/auth/drive.file
from [Google Drive API documentation](https://developers.google.com/drive/api/guides/api-specific-auth?hl=en=)
Thus, we can only update files that have already been created throughout this application... But the application, as-in, is not able to do that. We need to modify the script by hand to first create a new file with a new fresh ID and then uses this file as the one we previously wanted to update. Ayyy, sure... Kind a bit commplicated but shall be improved afterward to include this situation.
