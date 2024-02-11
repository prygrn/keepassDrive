import secrets
import sys
import logging
from pathlib import Path
from GDrive import GDrive

ARGUMENTS_NB = 3

LOGGER = logging.getLogger(__name__)


class WrongNumberOfArguments(Exception):
    """
    Raised when the module is not executed with the right number of arguments
    """

    pass


class NoFileName(Exception):
    """
    Raised when the user wants to retrieve a file not in the Drive
    """


def main():
    current_directory = Path.cwd()

    logging.basicConfig(
        filename=f"{current_directory.name}.log",
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
        raise WrongNumberOfArguments("Invalid number of arguments")

    name = sys.argv[1]
    drive = GDrive(secrets_file=sys.argv[2])
    drive.list_files()
    file = drive.get_file_by_name(sys.argv[1])
    if file is not None:
        print(file['id'])
        file = drive.download_file(file)
    else:
        raise NoFileName(f"File {file['name']} unknown")


if __name__ == "__main__":
    main()
