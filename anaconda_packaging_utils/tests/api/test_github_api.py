"""
File:           test_github_api.py
Description:    Tests GitHub (wrapper) API library
"""

from unittest.mock import patch

import pytest
from github import Github

from anaconda_packaging_utils.api import github_api


def test_access_raises() -> None:
    """
    Ensures that we are capturing and re-throwing exceptions that occur in an API access callback.
    """
    with patch("anaconda_packaging_utils.api.github_api.Github"):

        def _to_throw(j: Github) -> None:
            raise ValueError()

        with pytest.raises(github_api.ApiException):
            github_api.GitHubApi().access_github(_to_throw)
