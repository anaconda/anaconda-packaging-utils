"""
File:           subshell.py
Description:    Utility library that provides a simplified interface for running commands in Linux through a
                "subshell-like" interface.
"""

import logging as log
import subprocess


def run_shell(cmd: str, capture_output: bool = True, cwd: str = "") -> subprocess.CompletedProcess[str]:
    """
    Utility wrapper around `subprocess.run()` that provides the ability to run shell commands outside of Python.
    :param cmd: Command to execute
    :param capture_output: (Optional) Indicates if the output is directly printed to the console or if it is buffered
        and put into a string. If the called command prompts for input that can't be suppressed (like a password) this
        flag should be set to `False`
    :param cwd: (Optional) "Current Working Directory", changes the path that the shell operates in. Effectively acts as
        if you ran `cd` prior to the command.
    :returns: Process object including a POSIX-style return code
    """
    output = subprocess.run(
        cmd,
        encoding="utf-8",
        capture_output=capture_output,
        cwd=cwd,
        shell=True,
        check=False,
    )
    log.debug("run_shell() - Executed: `%s`", cmd)
    if cwd:
        log.debug("  |- Executed in directory: %s", cwd)
    if output.stdout:
        log.debug("  |- STDOUT: %s", output.stdout)
    if output.stderr:
        log.debug("  |- STDERR: %s", output.stderr)
    return output


def run_shell_chain(
    cmds: list[str],
    capture_output: bool = True,
    cwd: str = "",
    is_fatal_error: bool = False,
) -> list[subprocess.CompletedProcess[str]]:
    """
    Runs a series of shell commands in a chain. If one command fails, the whole chain fails and execution stops. Note:
    `cd` commands are specially processed and run with the "Current Working Directory" (cwd) feature of `subprocess.run`
    :param cmds: List of commands to execute in a sequence
    :param capture_output: (Optional) Indicates if the output is directly printed to the console or if it is buffered
        and put into a string. If the called command prompts for input that can't be suppressed (like a password) this
        flag should be set to `False`
    :param is_fatal_error: (Optional) Stops chain execution on first command that returns a non-zero return code. The
        calling program can determine which command failed by looking at the length of the returned list and/or by
        looking at the `args` member of last-returned completed process object.
    :param cwd: (Optional) "Current Working Directory", changes the path that the shell operates in. Effectively acts as
        if you ran `cd` prior to the command. Note that if subsequent `cd` commands are used, this value is overwritten.
    :returns: Process object including a POSIX-style return code
    """
    completed_procs = []
    for cmd in cmds:
        # Handle `cd` as a special command that just sets the current working directory
        if cmd.startswith("cd "):
            cwd = cmd[len("cd ") :]
            log.debug("run_shell_chain() - Chained command cd'd into: `%s`", cwd)
            # Mock a completed process so that the calling code doesn't have to handle counting `cd` calls.
            completed_procs.append(subprocess.CompletedProcess(args=cmd, stdout="", stderr="", returncode=0))
            continue
        proc = run_shell(cmd, capture_output, cwd)
        completed_procs.append(proc)
        if is_fatal_error and proc.returncode:
            log.error(
                "run_shell_chain() - Command in critical chain returned an" " error: `%s`",
                cmd,
            )
            break
    return completed_procs
