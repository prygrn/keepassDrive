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
