# Keepass automatic launcher with Google Drive

This tool automatically downloads your keepass database from your Google Drive and opens it to be ready to be consulted.
When exiting, it will check if there is any differences between the remote and the local ones. If any, it will upload the local to the remote to be up-to-date.

**Be warned that this tool uses some environment variables such as your db password and Google OAuth client secret in argument.**
**In the next releases, these information would be filled from a configuration json file, which could be more secured (to be verified)**

## Prerequisites

1. Having keepass [Get it here](https://keepass.info/index.html)
2. Yes, having a Google account could help here
3. Install requirements.txt packages in the environment of your choice (virtual preferred)

## Installation

1. Clone this repository
2. Create a secret configuration file that store credentials with the following scheme:

```json
{
  "file": {
    "name": "databasename.kdbx",
    "password": "unencryptedpassword"
  },
  "client": {
    "secrets_location": "secrets.json"
  }
}
```

1. You can now give it a try to the following command line:
    ```python3 keepass.py <your_database_name> <your_client_secrets_json_file>```

## Improvements

1. Potentially access the KEEPASS_DB_PWD from another source (configuration file ?) ==> Check the securer way.
