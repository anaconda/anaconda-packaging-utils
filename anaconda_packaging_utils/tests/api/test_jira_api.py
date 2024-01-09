"""
File:           test_jira_api.py
Description:    Tests JIRA (wrapper) API library
"""

from unittest.mock import patch

import pytest
from jira.client import JIRA

from anaconda_packaging_utils.api import jira_api


def test_access_raises() -> None:
    """
    Ensures that we are capturing and re-throwing exceptions that occur in an API access callback.
    """
    with patch("anaconda_packaging_utils.api.jira_api.JIRA"):

        def _to_throw(j: JIRA) -> None:
            raise ValueError()

        with pytest.raises(jira_api.ApiException):
            jira_api.JiraApi().access_jira(_to_throw)
