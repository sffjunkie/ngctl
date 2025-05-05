import logging
import subprocess


def command_exists(command: str) -> bool:
    proc = subprocess.run(["command", "-v", command], shell=True)
    ok = proc.returncode == 0
    if ok == 0:
        logging.debug(f"Command `{command}' found.")
    return ok


def command_output(args: list[str]) -> str:
    proc = subprocess.run(args, capture_output=True)
    return proc.stdout.decode("utf-8").strip("\n")
