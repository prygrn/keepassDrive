class SecretFileNotFoundError(Exception):
    """
    Raised when a client secret file is not found
    """

    pass


class TokenFileInvalidError(Exception):
    """
    Raised when a token file is invalid
    """

    pass


class TokenFileNotFoundError(Exception):
    """
    Raised when a token file is not found
    """

    pass


class DriveIsEmptyError(Exception):
    """
    Raised when the given Google Drive is empty
    """

    pass


class FileDownloadFailedError(Exception):
    """
    Raised when a file has failed to be downloaded
    """

    pass


class NoFileNameError(Exception):
    """
    Raised when the user wants to retrieve a filename not in the Drive
    """

    pass


class SearchFileHttpError(Exception):
    """
    Raised when an HTTP error is returned while searching for a given file
    """

    pass


class UpdateFileHttpError(Exception):
    """
    Raised when an HTTP error is returned while updating a given file
    """

    pass


class NoUploaderFindError(Exception):
    """
    Raised when the Uploader class has not been correctly constructed
    """

    pass
