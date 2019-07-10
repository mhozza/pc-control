#!/usr/bin/env python

import argparse
import toml
import secrets
import shutil

from pathlib import Path

SERVICES_LOCATION = Path("/etc/systemd/system")
CONFIG_NAME = "config.toml"
CONFIG_EXAMPLE_NAME = "config.toml.example"
SCRIPT_NAME = "home_commands.py"
SERVICE_NAME = "home-commands.service"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Install the home commands server as a service."
    )
    parser.add_argument("-d", "--dest", default="/opt/scripts/", help="destination")
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

    shutil.copyfile(Path(".") / SCRIPT_NAME, destination / SCRIPT_NAME)
    shutil.copyfile(Path(".") / SERVICE_NAME, SERVICES_LOCATION / SERVICE_NAME)
