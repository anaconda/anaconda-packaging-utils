"""
File:           config_data.py
Description:    Utility library that parses the standard configuration file used by the scripts. Also provides
                mechanisms for accessing these user-specified constant values.
"""
import json
from pathlib import Path
from threading import Lock
from typing import Final, no_type_check

import yaml
from jsonschema import validate as schema_validate

from anaconda_packaging_utils.types import SchemaType

## Types ##
# typedef for config file format
ConfigType = dict[str, dict[str, str]]

## Constants ##
CONFIG_FILE_NAME: Final[str] = ".anaconda-packaging-utils-config.yaml"
# Note that `mypy` takes issue with `Path.home()` for returning "Any"
CONFIG_FILE_DEFAULT_PATH: Final[Path] = Path.home() / Path(CONFIG_FILE_NAME)  # type: ignore


@no_type_check
def _generate_config_schema() -> SchemaType:
    """
    Initialization of `CONFIG_FILE_SCHEMA` is wrapped in a function so that we can bypass the `mypy` type checking on
    every schema line with the `@no_type_check` decorator.

    `types-jsonschema` defines their schema type with an `Any`, and that upsets `mypy` to the point where it'll throw
    multiple errors on almost every line of the schema definition.
    :return: Config Data Schema
    """
    return {
        "type": "object",
        "required": [
            "token",
            "local_path",
        ],
        "properties": {
            "token": {
                "type": "object",
                "required": ["github"],
                "properties": {"github": {"type": "string"}},
            },
            "local_path": {
                "type": "object",
                "required": ["aggregate"],
                "properties": {"aggregate": {"type": "string"}},
            },
        },
    }


CONFIG_FILE_SCHEMA: Final[SchemaType] = _generate_config_schema()


## Class ##
class ConfigData:
    """
    On first construction, this class automatically loads the standard configuration file for `anaconda-packaging-utils`
    tools. After that, the instance provides a mechanism for accessing configuration information.

    This provides Singleton-like access. The shared cache is thread-safe.

    This class uses a "key-path" to identify unique keys. A "key-path" is a fully-formed key that separates multiple
    keys by a `.` operator.

    For example, to get the path to the local `aggregate` repo, use:
      local_path.aggregate
    """

    # We use static members to cache information on first read. Every subsequent construction within the runtime of a
    # program will read from the cached value, ensuring a single source of read-only truth.
    _config_tbl: dict[str, str] = {}
    _file_path: Path = Path()
    _mutex = Lock()

    def __init__(self, file_path: str | Path = CONFIG_FILE_DEFAULT_PATH) -> None:
        """
        Constructs and initializes a ConfigData object that allows for access of useful user-defined values.

        Note that `file_path` should only be needed to be used for testing purposes. Subsequent constructions with
        different `file_path` values will result in the invalidation of the shared cache.

        :param file_path:           (Optional) The path to a standard configuration file. Defaults to a file in the home
                                    directory.
        :raises FileNotFoundError:  If the configuration file is not found
        :raises ValidationError:    If the configuration file does not match the valid schema.
        """
        with ConfigData._mutex:
            # Ensure `file_path` is of type `Path()` for comparison
            file_path = Path(file_path)
            if ConfigData._file_path != file_path:
                ConfigData._file_path = Path(file_path)
                # Read in the file and validate the schema
                raw_tbl: ConfigType = {}
                with open(ConfigData._file_path, "r", encoding="utf-8") as f:
                    raw_tbl = yaml.safe_load(f)
                schema_validate(raw_tbl, CONFIG_FILE_SCHEMA)

                # Initialize the lookup table
                for top_key, inner_tbl in raw_tbl.items():
                    for inner_key, value in inner_tbl.items():
                        ConfigData._config_tbl[f"{top_key}.{inner_key}"] = value

    def __str__(self) -> str:
        """
        Pretty-prints the configuration data key-value map as a string. Use only for debugging purposes.
        :return: Pretty-printed version of the key-value table.
        """
        with ConfigData._mutex:
            return json.dumps(ConfigData._config_tbl, indent=2)

    def __contains__(self, key: str) -> bool:
        """
        Returns true if a key-path is found.
        :return: True if the key-path is found. False otherwise.
        """
        with ConfigData._mutex:
            return key in ConfigData._config_tbl

    def __getitem__(self, key: str) -> str:
        """
        Returns a value by a key-path.
        :param key:         Full key that describes a value
        :raises KeyError:   If the key is not found
        :return: The value found at the provided key
        """
        with ConfigData._mutex:
            return ConfigData._config_tbl[key]
