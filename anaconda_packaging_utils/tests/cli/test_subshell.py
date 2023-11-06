"""
File:           test_subshell.py
Description:    Tests subshell utility library
                TODO Proper mocking for `subprocess.run()`
"""
import platform

import pytest

from anaconda_packaging_utils.cli import subshell

TEST_PATH = "anaconda_packaging_utils/tests"


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_success() -> None:
    """
    Ensures STDOUT is captured and a success code is returned
    """
    result = subshell.run_shell("cat test_aux_files/text.txt", cwd=TEST_PATH)
    assert result.stdout == "All work and no play makes Jack a dull boy\n"
    assert result.stderr == ""
    assert result.returncode == 0


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_failure() -> None:
    """
    Ensures STDERR is captured and a failure code is returned
    """
    result = subshell.run_shell("echo 'error' > /dev/stderr && /usr/bin/false", cwd=TEST_PATH)
    assert result.stdout == ""
    assert result.stderr == "error\n"
    assert result.returncode != 0


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_chain_success() -> None:
    """
    Ensures STDOUT is captured and a success code is returned if all chained
    commands succeed
    """
    results = subshell.run_shell_chain(
        [
            "cat test_aux_files/text.txt",
            "cat test_aux_files/text.txt",
            "cat test_aux_files/text.txt",
        ],
        cwd=TEST_PATH,
    )
    assert len(results) == 3
    for result in results:
        assert result.stdout == "All work and no play makes Jack a dull boy\n"
        assert result.stderr == ""
        assert result.returncode == 0


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_chain_failure_continue() -> None:
    """
    Ensures STDERR is captured and a failure code is returned in the event
    of a critical failure in a chained command
    """
    results = subshell.run_shell_chain(
        [
            "cat test_aux_files/text.txt",
            "echo 'error' > /dev/stderr && /usr/bin/false",
            "cat test_aux_files/text.txt",
        ],
        cwd=TEST_PATH,
    )
    assert len(results) == 3
    assert results[0].stdout == "All work and no play makes Jack a dull boy\n"
    assert results[0].stderr == ""
    assert results[0].returncode == 0
    assert results[1].stdout == ""
    assert results[1].stderr == "error\n"
    assert results[1].returncode != 0
    assert results[2].stdout == "All work and no play makes Jack a dull boy\n"
    assert results[2].stderr == ""
    assert results[2].returncode == 0


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_chain_failure_fail_fast() -> None:
    """
    Ensures STDERR is captured and a failure code is returned in the event
    of a critical failure in a chained command
    """
    results = subshell.run_shell_chain(
        [
            "cat test_aux_files/text.txt",
            "echo 'error' > /dev/stderr && /usr/bin/false",
            "cat test_aux_files/text.txt",
        ],
        cwd=TEST_PATH,
        is_fatal_error=True,
    )
    assert len(results) == 2
    assert results[0].stdout == "All work and no play makes Jack a dull boy\n"
    assert results[0].stderr == ""
    assert results[0].returncode == 0
    assert results[1].stdout == ""
    assert results[1].stderr == "error\n"
    assert results[1].returncode != 0


@pytest.mark.skipif(platform.system() == "Windows", reason="`subshell` is not supported on Windows")
def test_run_shell_chain_can_cd() -> None:
    """
    Ensures that `cd` commands change the current working directory of a series
    of chained shell commands.
    """
    results = subshell.run_shell_chain(
        [
            "pwd",
            "cd /usr/bin",
            "pwd",
        ],
        cwd=TEST_PATH,
        is_fatal_error=True,
    )
    print(results)
    assert len(results) == 3
    assert results[0].stdout.endswith(f"{TEST_PATH}\n")
    assert results[0].stderr == ""
    assert results[0].returncode == 0
    assert results[1].stdout == ""
    assert results[1].stderr == ""
    assert results[1].returncode == 0
    assert results[2].stdout == "/usr/bin\n"
    assert results[2].stderr == ""
    assert results[2].returncode == 0
