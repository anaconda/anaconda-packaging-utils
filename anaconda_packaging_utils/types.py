"""
File:           types.py
Description:    File that contains common types and type aliases (typedefs).
"""
from typing import Any, Final, Mapping

# Recursive type for handling JSON data. See this post for more info:
#   https://github.com/python/typing/issues/182#issuecomment-1320974824
JsonType = dict[str, "JsonType"] | list["JsonType"] | str | int | float | bool | None

# Type for a schema object used by the `jsonschema` library
SchemaType = Mapping[str, Any]  # type: ignore[misc]

# Common exit codes
EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1
EXIT_CRITICAL_EXCEPTION: Final[int] = 42
