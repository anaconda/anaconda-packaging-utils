"""
File:           test_jira_api.py
Description:    Tests JIRA (wrapper) API library
"""

from unittest.mock import patch

import pytest

from anaconda_packaging_utils.api import jira_api


@pytest.mark.skip(reason="TODO: Improve this test and ensure the mocker suppresses network calls")
def test_get_jira_smoke() -> None:
    """
    Smoke test that ensures that we return an underlying constructed object.
    """
    with patch("anaconda_packaging_utils.api.jira_api.JIRA"):
        assert isinstance(jira_api.JiraApi().get_jira(), object)
