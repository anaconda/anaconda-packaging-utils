"""
File:           test_jira_api.py
Description:    Tests JIRA (wrapper) API library
"""

from unittest.mock import patch

from anaconda_packaging_utils.api import jira_api


def test_get_jira_smoke() -> None:
    """
    Smoke test that ensures that we return an underlying constructed object.
    """
    # TODO: Improve this test, the mocker masks what we are attempting to check for
    with patch("anaconda_packaging_utils.api.jira_api.JIRA"):
        assert isinstance(jira_api.JiraApi().get_jira(), object)
