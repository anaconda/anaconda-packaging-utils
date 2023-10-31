"""
File:           file_io.py
Description:    Library that provides tools for common file I/O tasks.
"""

from datetime import datetime
from pathlib import Path
from typing import Final

# Prefix used by temporary files. This helps developers identify the source of excessive writes, if this library is
# being abused or is not cleaning up after itself.
TEMP_FILE_PREFIX: Final[str] = "anaconda-packaging-utils-"


def write_file(file: Path | str, content: str | list[str]) -> None:
    """
    Writes text to a file
    :param file:    File name/path to file to write
    :param content: String (or list of strings) to write to a file. If a list is given, strings are written line-by-line
    """
    # Ensure `path` is always a path.
    file = Path(file)
    with open(file, "w", encoding="utf-8") as f:
        if isinstance(content, list):
            # `writelines()` does not add new lines automatically.
            f.writelines(f"{line}\n" for line in content)
        else:
            f.write(content)


def write_temp_file(content: str | list[str], tag: str = "") -> Path:
    """
    Writes text to a temp file. Unlike the `tempfile` library, these temp files:
      - Are written to `/tmp` so this function will only work on POSIX systems
      - Will write an actual file to disk, available to other programs
        - In other words, the file will remain even if the file handler goes out of scope.

    BE AWARE of the security implications of this.

    :param content: String (or list of strings) to write to a file. If a list is given, strings are written line-by-line
    :param tag:     (Optional) Tag to further help identify the temporary file
    :return: Path to the temp file that was written to
    """
    # Naming the file with some origin information allows others to point fingers when we don't clean-up after ourselves
    if tag:
        tag += "-"
    path = Path(f"/tmp/{TEMP_FILE_PREFIX}{tag}{str(datetime.now())}.out")
    write_file(path, content)
    return path
