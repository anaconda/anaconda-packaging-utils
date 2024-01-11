"""
File:           test_github_api.py
Description:    Tests GitHub (wrapper) API library
"""

from unittest.mock import patch

import pytest

from anaconda_packaging_utils.api import github_api


@pytest.mark.skip(reason="TODO: Improve this test and ensure the mocker suppresses network calls")
def test_get_github_smoke() -> None:
    """
    Smoke test that ensures that we return an underlying constructed object.
    """
    with patch("anaconda_packaging_utils.api.github_api.Github"):
        assert isinstance(github_api.GitHubApi().github, object)
