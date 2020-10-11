import os
import configparser

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..")

config = configparser.ConfigParser()
config.read(os.path.join(SCRIPT_DIR, "./config/linxConfig.ini"))

INSTANCE_URL = config.get("Server", "linx_instance_url")
API_KEY = config.get("Server", "linx_api_key")

DEFAULT_DELETE_KEY = config.get("Defaults", "delete_key")