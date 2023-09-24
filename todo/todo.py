"""Provides code to connect the CLI with the to-do database"""
from typing import Any, Dict, NamedTuple

from todo.database import DatabaseHandler


class Todo:
    """Represents a to-do item"""

    def __init__(self, id: int, title: str, description: str, completed: bool) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed

    def __repr__(self) -> str:
        return f"Todo: {self.id} {self.title} {self.completed}"


class TodoModel(NamedTuple):
    todo: Todo
    error: int
