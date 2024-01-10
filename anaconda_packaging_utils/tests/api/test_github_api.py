"""
File:           test_github_api.py
Description:    Tests GitHub (wrapper) API library
"""

from unittest.mock import patch

from anaconda_packaging_utils.api import github_api


def test_get_github_smoke() -> None:
    """
    Smoke test that ensures that we return an underlying constructed object.
    """
    # TODO: Improve this test, the mocker masks what we are attempting to check for
    with patch("anaconda_packaging_utils.api.github_api.Github"):
        assert isinstance(github_api.GitHubApi().get_github(), object)
