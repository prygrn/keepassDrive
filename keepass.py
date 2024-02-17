import sys
import logging
import subprocess
import filecmp
from os import environ
from pathlib import Path

from yagdrive import manager
from yagdrive import errors as yagerrors
import errors

ARGUMENTS_NB = 3

LOGGER = logging.getLogger(__name__)


def start_keepass(filename: Path, password: str):
    try:
        process = subprocess.run(
            ["keepass2", f"{filename}", f"-pw:{password}"],
            check=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as error:
        raise errors.KeepassClosedWithError(
            f"keepass closed with error(s).\nError :{error}"
        )
    # Different than 0 meaning there was an error
    if process.returncode:
        return False

    return True


def upload_file(filename: Path):

    return False


def main():
    dbfile = dict()
    process = None
    current_directory = Path.cwd()

    logging.basicConfig(
        filename=f"{current_directory.stem}.log",
        filemode="w",
        encoding="UTF-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.INFO,
    )

    if len(sys.argv) != ARGUMENTS_NB:
        LOGGER.critical(
            """This tool requires the following arguments:
                     - The name of the keepass database to be opened
                     - The path/to/the/secrets/file"""
        )
        raise errors.WrongNumberOfArgumentsError("Invalid number of arguments")

    database = Path(sys.argv[1])
    secrets = Path(sys.argv[2])

    # Create a Google Drive manager
    drive = manager.GDrive(secrets_file=secrets)

    # Search for the given database inside the Drive
    try:
        dbfile = drive.search_file_by_name(database.name)
    except yagerrors.NoFileNameError as file_error:
        LOGGER.critical(f"File error: {file_error}")
        return False
    except yagerrors.SearchFileHttpError as http_error:
        LOGGER.critical(f"Http error: {http_error}")
        return False

    # Start the download
    try:
        dbfile = drive.download_file(dbfile)
    except yagerrors.FileDownloadFailedError as download_error:
        LOGGER.error(f"Download error : {download_error}")
        return False
    LOGGER.info(f"Downloading {dbfile['name']} succeed")

    # Create a copy of the database to be compared afterward
    LOGGER.info(f"Creating a copy of {database}")
    copy_path = Path(f"{database.stem}_copy.kdbx")
    copy_path.write_bytes(database.read_bytes())
    LOGGER.info(f"Copy of {database} created")

    #  Execute the keepass app
    try:
        if not start_keepass(database, environ.copy()["KEEPASS_DB_PWD"]):
            LOGGER.error("An unknown error occurred about keepass")
            return False
    except errors.KeepassClosedWithError as keepass_error:
        LOGGER.critical(keepass_error)

    # Now the user finished to interact with the app, we need to compare both files
    if not filecmp.cmp(database.name, copy_path.name):
        LOGGER.info("Files are different. File will be updated")
        try:
            if drive.upload_file(dbfile) == None:
                LOGGER.error("An unknown error occurred during the update")
                return False
        except yagerrors.UpdateFileHttpError as update_error:
            LOGGER.critical(f"Update error: {update_error}")
            return False

    else:
        LOGGER.info("No changed detected in the database. Nothing to be updated.")

    # Remove all
    database.unlink()
    copy_path.unlink()

    return True


if __name__ == "__main__":
    if main() == True:
        LOGGER.info("Program ended successfully.")
        exit(0)
    else:
        LOGGER.error("Program ended with failure(s).")
        exit(1)
