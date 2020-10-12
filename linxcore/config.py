import os
from typing import Any

import toml

from .exceptions import ConfigException

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..")


class TOMLConfig:
    __slots__ = ("data", )

    def __init__(self, json_data: dict):
        self.data = json_data

    @classmethod
    def from_filename(cls, file_path: str):
        with open(file_path, "r") as config_file:
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


config = TOMLConfig.from_filename(os.path.join(SCRIPT_DIR, "./config/linxConfig.toml"))

##########
# Tables
##########
TABLE_SERVER = config.get_table("Server")

##########
# Server
##########
INSTANCE_URL = TABLE_SERVER.get("linx_instance_url")
API_KEY = TABLE_SERVER.get("linx_api_key")
