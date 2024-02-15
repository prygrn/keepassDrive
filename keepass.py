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


def download_file(filename: Path, secrets: Path):
    name = filename.name
    drive = manager.GDrive(secrets_file=secrets)
    file = drive.search_file_by_name(filename.name)
    if file is not None:
        LOGGER.info(
            f"Start downloading the database {name} from the given Google Drive"
        )
        try:
            file = drive.download_file(file)
        except yagerrors.FileDownloadFailedError as error:
            LOGGER.error(f"Downloading {filename.name} results in error")
            return False
    else:
        LOGGER.error(f"No file named '{filename}' in the given Google Drive")
        return False

    LOGGER.info(f"Downloading {filename} succeed")
    return True


def start_keepass(filename: Path, password: str):
    try:
        process = subprocess.run(
            ["keepass2", f'"{filename}"', f"-pw:{password}"],
            check=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as error:
        raise errors.KeepassClosedWithError(
            f"keepass closed with error(s).\nError :{error}"
        )
    return True


def main():
    file = dict()
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

    database = Path(Path(sys.argv[1]).absolute())
    secrets = Path(sys.argv[2])
    if not download_file(database, secrets):
        return False

    # Create a copy of the database to be compared afterward
    LOGGER.info(f"Creating a copy of {database}")
    copy_path = Path(f"{database.stem}_copy.kdbx")
    copy_path.write_bytes(database.read_bytes())
    LOGGER.info(f"Copy of {database} created")

    #  Execute the keepass app
    if start_keepass(database, environ.copy()["KEEPASS_DB_PWD"]):
        return False

    # Now the user finished to interact with the app, we need to compare both files
    if not filecmp.cmp(database.name, copy_path.name):
        LOGGER.info("Files are different: something has been changed in the db")
    else:
        LOGGER.info("No changed detected in the database. Nothing to be updated.")

    return True


if __name__ == "__main__":
    if main() == True:
        LOGGER.info("Program ended successfully.")
        exit(0)
    else:
        LOGGER.error("Program ended with failure(s).")
        exit(1)
