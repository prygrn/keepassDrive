import sys
import logging
import subprocess
from os import environ
from pathlib import Path

import GDrive
import exceptions

ARGUMENTS_NB = 3

LOGGER = logging.getLogger(__name__)


def main():
    file = dict()
    process = None
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
        raise exceptions.WrongNumberOfArguments("Invalid number of arguments")

    name = sys.argv[1]
    drive = GDrive.GDrive(secrets_file=sys.argv[2])
    file = drive.search_file_by_name(name)
    # file = drive.get_file_by_name(sys.argv[1])
    if file is not None:
        file = drive.download_file(file)
        if not file["is_downloaded"]:
            raise GDrive.FileDownloadFailed(
                f"File {file} failed to be downloaded")
    else:
        raise exceptions.NoFileName(
            f"File {name} not found in the given Drive")

    env = environ.copy()
    #  Execute the keepass app
    try:
        process = subprocess.run(["keepass2", f"{file['name']}",
                                  f"-pw:{env['KEEPASS_DB_PWD']}"],
                                 check=True,
                                 stderr=subprocess.STDOUT,
                                 stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as error:
        raise exceptions.KeepassClosedWithErrors(
            f"keepass closed with error(s).\nError :{error}")


if __name__ == "__main__":
    main()
