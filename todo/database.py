"""Contains code to handle the application's to-do database"""

import configparser
import json
from pathlib import Path
from typing import Any, List, NamedTuple

from todo import ReturnCode

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)


class DBResponse(NamedTuple):
    """Represents the response from the database."""

    todo_list: List[Any]
    error: ReturnCode


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), ReturnCode.SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], ReturnCode.JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], ReturnCode.DB_READ_ERROR)

    def write_todos(self, todo_list: List[Any]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, ReturnCode.SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, ReturnCode.DB_WRITE_ERROR)


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
