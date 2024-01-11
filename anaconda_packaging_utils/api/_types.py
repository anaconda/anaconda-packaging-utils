"""
File:           _types.py
Description:    Contains types and classes used internally for the API modules.
"""


class BaseApiException(Exception):
    """
    Generic exception indicating an unrecoverable failure of this API.

    This exception is meant to condense many possible failures into one generic error. The thinking is, if the calling
    code runs into any API failure, there isn't much that can be done. So it is easier for the caller to handle one
    exception than many exception types.
    """

    def __init__(self, message: str):
        """
        Constructs an API exception
        :param message: String description of the issue encountered.
        """
        super().__init__(message if len(message) else "An unknown API issue was encountered.")
