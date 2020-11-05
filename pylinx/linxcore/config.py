import os
from typing import Any

import toml
from click import echo, style, get_current_context, Context

from .exceptions import ConfigException

ROOT_DIR = os.path.join(os.path.dirname(__file__), "../..")

LOGS_DIR = os.path.join(ROOT_DIR, "logs")
if not os.path.isdir(LOGS_DIR):
    os.mkdir(LOGS_DIR)


class TOMLConfig:
    __slots__ = ("data", )

    def __init__(self, json_data: dict):
        self.data = json_data

    @classmethod
    def from_filename(cls, file_path: str):
        with open(file_path, "r", encoding="utf-8") as config_file:
            data = toml.loads(config_file.read())

        return cls(data)

    def get_table(self, name: str, ignore_empty: bool = False) -> "TOMLConfig":
        data = self.data.get(name)

        if data is None and not ignore_empty:
            raise ConfigException(f"Configuration table missing: '{name}'")

        return TOMLConfig(data)

    def get(self, name: str, fallback: Any = None, ignore_empty: bool = False) -> Any:
        data = self.data.get(name)

        if data is None and not ignore_empty:
            raise ConfigException(f"Configuration value missing: '{name}'")

        if data is None:
            return fallback
        else:
            return data


class LinxConfig:
    __slots__ = (
        "_config", "_table_server", "_table_defaults",
        "INSTANCE_URL", "API_KEY", "DEFAULT_EXPIRY_DAYS"
    )

    def __init__(self, config_dict: TOMLConfig):
        self._config = config_dict

        self._table_server = self._config.get_table("Server")
        self._table_defaults = self._config.get_table("Defaults")

        ##########
        # Server
        ##########
        self.INSTANCE_URL = self._table_server.get("linx_instance_url")
        self.API_KEY = self._table_server.get("linx_api_key")

        ##########
        # Server
        ##########
        self.DEFAULT_EXPIRY_DAYS = self._table_defaults.get("default_expiry_days")


pyproject_path = os.path.realpath(os.path.join(ROOT_DIR, "pyproject.toml"))
pyproject_config = TOMLConfig.from_filename(pyproject_path)

PROJECT_VERSION = pyproject_config.get_table("tool").get_table("poetry").get("version")


def load_config(config_file: str) -> LinxConfig:
    # Find and use the proper configuration file
    # Search order is as follows:
    # 1. --config switch
    #    (%linxpath% expands to the parent directory of pylinx install - see pylinx.ps1 and pylinx.sh for a use case)
    # 2. Current directory
    # 3. ~user/.config/pylinx/linxConfig.toml
    ctx: Context = get_current_context()

    if config_file is not None:
        # Load the file passed with --config
        final_config_file = os.path.realpath(config_file.replace("%linxpath%", ROOT_DIR))

        if not os.path.isfile(final_config_file):
            echo(style("Configuration: filename passed via --config does not exist.", fg="bright_red"))
            ctx.exit(1)
        else:
            echo(f"Configuration: using '{final_config_file}'")
    else:
        # Look in the current directory
        final_config_file = os.path.realpath(os.path.join(ctx.obj["working_dir"], "linxConfig.toml"))

        if os.path.isfile(final_config_file):
            # Load the config in current directory
            echo(f"Configuration: using current directory '{final_config_file}'")
        else:
            # Finally, try to load the user config
            final_config_file = os.path.realpath(
                os.path.join(os.path.expanduser("~"), ".config/pylinx/linxConfig.toml")
            )

            if not os.path.isfile(final_config_file):
                echo(style(f"Configuration: no --config file passed, neither current directory "
                           f"nor \"~/.config/pylinx\" contain linxConfig.toml."
                           f"\nPlease pass the file with --config manually, create the configuration "
                           f"in your current directory or in \"~/.config/pylinx\" directory "
                           f"or do so interactively with \"pylinx configure\"."))
                ctx.exit(1)
            else:
                echo(f"Configuration: using user home '{final_config_file}'")

    config = TOMLConfig.from_filename(final_config_file)
    return LinxConfig(config)
