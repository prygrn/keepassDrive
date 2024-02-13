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

    path_name = Path(sys.argv[1]).absolute()  # Create a Path object with absolute path
    filename = path_name.name
    drive = manager.GDrive(secrets_file=sys.argv[2])
    file = drive.search_file_by_name(filename)
    # file = drive.get_file_by_name(sys.argv[1])
    if file is not None:
        file = drive.download_file(file)
        if not file["is_downloaded"]:
            raise yagerrors.FileDownloadFailedError(
                f"File {file} failed to be downloaded"
            )
    else:
        raise yagerrors.NoFileNameError(f"File {filename} not found in the given Drive")

    # Create a copy of the database to be compared afterward
    copy_path_name = Path(f"{path_name.stem}_copy.kdbx")
    copy_path_name.write_bytes(path_name.read_bytes())

    env = environ.copy()
    #  Execute the keepass app
    try:
        process = subprocess.run(
            ["keepass2", f"{file['name']}", f"-pw:{env['KEEPASS_DB_PWD']}"],
            check=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as error:
        raise errors.KeepassClosedWithError(
            f"keepass closed with error(s).\nError :{error}"
        )

    # Now the user finished to interact with the app, we need to compare both files
    if not filecmp.cmp(filename, copy_path_name.name):
        print("Files seem to be different : something has been changed in the db")
    else:
        print("Files seem to be the same")


if __name__ == "__main__":
    main()
