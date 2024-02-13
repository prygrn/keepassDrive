class WrongNumberOfArguments(Exception):
    """
    Raised when the module is not executed with the right number of arguments
    """

    pass


class NoFileName(Exception):
    """
    Raised when the user wants to retrieve a file not in the Drive
    """


class KeepassClosedWithErrors(Exception):
    """
    Raised when the keepass app closed with error(s)
    """
