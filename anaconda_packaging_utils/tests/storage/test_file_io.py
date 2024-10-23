"""
File:           test_file_io.py
Description:    Tests file I/O utilities library
"""

from pathlib import Path
from typing import no_type_check
from unittest.mock import mock_open, patch

from anaconda_packaging_utils.storage import file_io


@no_type_check
def test_write_file():
    """
    Tests writing of a file, with a string
    """
    file_path = "/path/to/mocked/file"
    file_data = """
    All work
    and no play
    makes Jack
    a dull boy
    """
    with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
        file_io.write_file(file_path, file_data)
        mock_file.assert_called_with(Path(file_path), "w", encoding="utf-8")
        mock_handler = mock_file.return_value.__enter__.return_value
        mock_handler.write.assert_called_with(file_data)


@no_type_check
def test_write_file_lines():
    """
    Tests writing of a file, with a list of strings
    """
    file_path = "/path/to/mocked/file"
    file_data = [
        "All work",
        "and no play",
    ]
    with patch("builtins.open", mock_open()) as mock_file:
        file_io.write_file(file_path, file_data)
        mock_file.assert_called_with(Path(file_path), "w", encoding="utf-8")
        mock_handler = mock_file.return_value.__enter__.return_value
        mock_handler.writelines.assert_called()


@no_type_check
def test_write_temp_file():
    """
    Tests writing of a temp file
    """
    file_data = "The trial never ends,\nPicard."
    with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
        file_path = file_io.write_temp_file(file_data)
        assert Path("/tmp/") in file_path.parents
        assert file_path.name.startswith(file_io.TEMP_FILE_PREFIX)
        mock_handler = mock_file.return_value.__enter__.return_value
        mock_handler.write.assert_called_with(file_data)


@no_type_check
def test_write_temp_file_with_tag():
    """
    Tests writing of a temp file, with a tag
    """
    file_data = "The trial never ends,\nPicard."
    with patch("builtins.open", mock_open(read_data=file_data)) as mock_file:
        file_path = file_io.write_temp_file(file_data, tag="tng")
        assert Path("/tmp/") in file_path.parents
        assert file_path.name.startswith(f"{file_io.TEMP_FILE_PREFIX}tng-")
        mock_handler = mock_file.return_value.__enter__.return_value
        mock_handler.write.assert_called_with(file_data)
