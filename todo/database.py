"""Contains code to handle the application's to-do database"""

import configparser
from pathlib import Path

from todo import ReturnCode

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database.

    Args:
        config_file (Path): Path to the configuration file.

    Returns:
        Path: Path to the to-do database.
    """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> ReturnCode:
    """Create the to-do database.

    Args:
        db_path (Path): Path to the to-do database.

    Returns:
        ReturnCode: Return code.    
    """
    try:
        db_path.write_text("[]")  # Empty to-do list
        return ReturnCode.SUCCESS
    except OSError:
        return ReturnCode.DB_WRITE_ERROR
