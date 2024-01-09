"""
File:           testing_utils.py
Description:    Contains constants and other utilities used throughout the unit tests in this project.
"""
import json
from pathlib import Path

import pytest

from anaconda_packaging_utils.storage.config_data import ConfigData
from anaconda_packaging_utils.types import JsonType

# Path to supplementary files used in test cases
TEST_FILES_PATH = "anaconda_packaging_utils/tests/test_aux_files"


def load_json_file(file: Path | str) -> JsonType:
    """
    Loads JSON from a test file.

    This could be turned into a fixture, but `mypy` doesn't play nice with those decorators.

    :param file:    JSON filename of the file to read
    :return: Parsed JSON read from the file
    """
    with open(Path(file), "r", encoding="utf-8") as f:
        j: JsonType = json.load(f)
        return j


@pytest.fixture()
def config_data() -> ConfigData:
    """
    Text fixture that generates a valid `ConfigData` instance with mocked test information.

    As this class follows a singleton pattern, the existence of this fixture is enough to bootstrap-initialize an
    instance to contain information to pass. The API modules tend to rely on this.

    :return: ConfigData instance that can be used for tests
    """
    return ConfigData(f"{TEST_FILES_PATH}/config_files/valid_schema.yaml")
