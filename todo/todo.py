"""Provides code to connect the CLI with the to-do database"""
from enum import Enum
from typing import NamedTuple

from todo.database import DatabaseHandler


class TodoPriority(Enum):
    Low = 0
    Medium = 1
    High = 2


class Todo:
    """Represents a to-do item"""

    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        priority: TodoPriority = TodoPriority.Low,
        completed: bool = False
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed

    def __repr__(self) -> str:
        return f"Todo: {self.id} {self.title} {self.completed}"


class TodoModel(NamedTuple):
    todo: Todo
    error: int
