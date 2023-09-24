""""Contains code to handle the application's configuration file"""

import configparser
from pathlib import Path

import typer

from todo import ReturnCode, __app_name__

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_app(db_path: str) -> ReturnCode:
    """Initialize the application."""
    config_code = _init_config_file()

    if config_code != ReturnCode.SUCCESS:
        return config_code

    database_code = _create_database(db_path)
    if database_code != ReturnCode.SUCCESS:
        return database_code

    return ReturnCode.SUCCESS


def _init_config_file() -> ReturnCode:
    """Initialize the configuration file.

    Returns:
        ReturnCode: Return code.
    """
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return ReturnCode.DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return ReturnCode.FILE_ERROR

    return ReturnCode.SUCCESS


def _create_database(db_path: str) -> ReturnCode:
    """Create the database.

    Args:
        db_path (str): Path to the database.

    Returns:
        ReturnCode: Return code.
    """
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return ReturnCode.DB_WRITE_ERROR
    return ReturnCode.SUCCESS
