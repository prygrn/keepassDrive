import sys
import logging
from pathlib import Path

ARGUMENTS_NB = 3

LOGGER = logging.getLogger(__name__)

class WrongNumberOfArguments(Exception):
    """
    Raised when the module is not executed with the right number of arguments
    """
    
    pass

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
                     - pThe name of the keepass database to be opened
                     - The path/to/the/secrets/file"""
        )
        raise WrongNumberOfArguments("Invalid number of arguments")

if __name__ == "__main__":
    main()
