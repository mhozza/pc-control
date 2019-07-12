#!/usr/bin/env python

import argparse
import toml
import secrets
import shutil
import os
import platform

from pathlib import Path

SERVICES_LOCATION = Path("/etc/systemd/system")
CONFIG_NAME = "config.toml"
CONFIG_EXAMPLE_NAME = "config.toml.example"
SCRIPT_NAME = "home_commands.py"
SERVICE_NAME = "home-commands.service"
WIN_SERVICE_NAME = "winservice.py"
DEFAULT_DESTINATION = "." if platform.system() == "Windows" else "/opt/scripts/"
WINDOWS_PYTHON_LOCATION = Path("")


def cp(src, dst):
    if src != dst:
        shutil.copyfile(src, dst)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install the home commands server as a service."
    )
    parser.add_argument("-d", "--dest", default=DEFAULT_DESTINATION, help="destination")
    parser.add_argument(
        "--key_length", type=int, default=32, help="Length of the secret key."
    )
    parser.add_argument(
        "-f", "--force_config", action="store_true", help="Overwrite config."
    )

    args = parser.parse_args()
    destination = Path(args.dest)
    if args.force_config or not (destination / CONFIG_NAME).exists():
        config = toml.load(CONFIG_EXAMPLE_NAME)
        config["key"] = secrets.token_hex(args.key_length)
        print("Generated new key:", config["key"])
        with open(destination / CONFIG_NAME, "w") as f:
            toml.dump(config, f)
    print("Copying files...")
    cp(Path(".") / SCRIPT_NAME, destination / SCRIPT_NAME)
    if platform.system() == "Windows":
        winservice = destination / WIN_SERVICE_NAME
        cp(Path(".") / WIN_SERVICE_NAME, winservice)
        print("Installing service...")
        os.system(f"py {winservice} --startup auto install")
        print("Starting service...")
        os.system(f"py {winservice} start")
    else:
        cp(Path(".") / SERVICE_NAME, SERVICES_LOCATION / SERVICE_NAME)
    print("Done.")
