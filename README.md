# Keepass automatic launcher with Google Drive

This tool automatically downloads your keepass database from your Google Drive and opens it to be ready to be consulted.
When exiting, it will check if there is any differences between the remote and the local ones. If any, it will upload the local to the remote to be up-to-date.

**Be warned that this tool shall be used with care as it opens your keepass database to anybody with the link + pass its password in argument.**

## Prerequisites
1. Having keepass [Get it here](https://keepass.info/index.html)
2. Allow your database to be reached by anybody with its link (**!**)
3. `curl` and `wget` installed
4. Create credentials ("OAuth client ID" - "TVs and Limited Input devices") from [Google Cloud Platform](https://console.cloud.google.com/apis/credentials)

## Installation
1. Clone this repository
2. Copy the `keepass` file into your bin folder
`cp ./keepass /usr/bin/keepass`
3. Setup your database path and password into the following environment variables
    * `KEEPASS_DB_URL` i.e. `echo "export KEEPASS_DB_URL=<your_db_url> >> .bashrc"`
    * `KEEPASS_DB_PWD` i.e. `echo "export KEEPASS_DB_PWD=<your_db_pwd> >> .bashrc"`
    * `CLIENT_ID` i.e. `echo "export CLIENT_IDL=<your_id> >> .bashrc"`
    * `CLIENT_SECRET` i.e. `echo "export CLIENT_SECRET=<your_secret> >> .bashrc"`
    * Source the file `source ~/.bashrc`
4. You can now give it a try ;)
