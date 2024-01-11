"""
File:           jira_api.py
Description:    Wrapper library that provides tools for using the Python JIRA API. The primary purpose of this wrapper
                is to simplify and standardize the authentication process.

                JIRA API links:
                  - Source: https://github.com/pycontribs/jira
                  - Docs: https://jira.readthedocs.io/index.html#
"""
import logging
from typing import Final

from jira.client import JIRA

from anaconda_packaging_utils.api._types import BaseApiException
from anaconda_packaging_utils.storage.config_data import ConfigData

# Logging object for this module
log = logging.getLogger(__name__)


class ApiException(BaseApiException):
    """
    Generic exception indicating an unrecoverable failure of this API. See the base class for more context.
    """

    pass


class JiraApi:
    """
    Singleton wrapper to the Python Jira project. This "ensures" that we only construct and authenticate the underlying
    Jira object once.
    """

    # The Jira API is wrapped in a list as a cheesy way to work around an initialization problem. Defaulting to `None`
    # or using an `Optional` causes the static analyzer to freak out on every use of the `__jira`, even if the static
    # variable has to have been initialized by instance-method call time.
    __jira: list[JIRA] = []

    # Where our JIRA boards are hosted
    __JIRA_HOST_URL: Final[str] = "https://anaconda.atlassian.net/"

    def __init__(self) -> None:
        """
        Constructs a JiraApi instance
        :raises ApiException: If there was a failure to authenticate.
        """
        if not JiraApi.__jira:
            data_store: Final[ConfigData] = ConfigData()
            try:
                JiraApi.__jira.append(
                    JIRA(
                        JiraApi.__JIRA_HOST_URL,
                        basic_auth=(data_store["user_info.email"], data_store["token.jira"]),
                    )
                )
            except Exception as e:
                raise ApiException("Failed to auth or connect to JIRA") from e

    @property
    def jira(self) -> JIRA:
        """
        Exposes an authenticated JIRA API instance directly to the caller, allowing for full use of the API.
        As this is a member function, successful construction of a `JiraApi` instance must have occurred previously
        for this to be able to be called.
        :returns: Authenticated instance of the underlying JIRA API
        """
        return JiraApi.__jira[0]
