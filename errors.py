class WrongNumberOfArgumentsError(Exception):
    """
    Raised when the module is not executed with the right number of arguments
    """

    pass


class KeepassClosedWithError(Exception):
    """
    Raised when the keepass app closed with error(s)
    """
    pass
