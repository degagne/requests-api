from __future__ import absolute_import

from typing import NoReturn


class HTTPError(RuntimeError):
    """ base exception used for this module """
    def __init__(self, message: str) -> NoReturn:
        self.message = message

    def __str__(self):
        return f"{self.errtype}: {self.message}"


class ConfigurationError(HTTPError):
    """ exception raised when method configuration fails """
    errno = 1
    errtype = "CONFIG_ERROR"
    description = "Invalid configuration property (or properties) detected."

    def __init__(self, message: str) -> NoReturn:
        super().__init__(message)


class RequestError(HTTPError):
    """ exception raised for all requests failures """
    errno = 2
    errtype = "HTTP_ERROR"
    description = ("HTTP requests returned an status code 4xx or 5xx, or "
                   "an unexpected status code")

    def __init__(self, message: str) -> NoReturn:
        super().__init__(message)