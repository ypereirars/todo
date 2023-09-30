"""Provides code to connect the CLI with the to-do database"""
from enum import IntEnum
from typing import List, NamedTuple, Optional
from uuid import uuid1

from todo import ReturnCode
from todo.database import DatabaseHandler


class TodoPriority(IntEnum):
    Low = 0
    Medium = 1
    High = 2


class Todo:
    """Represents a to-do item"""

    def __init__(
        self,
        id: str,
        title: str,
        description: str = "",
        priority: TodoPriority = TodoPriority.Low,
        completed: bool = False,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.priority = TodoPriority(priority)
        self.completed = completed

    def __repr__(self) -> str:
        return f"Todo: {self.id} {self.title} {self.completed}"


class TodoModel(NamedTuple):
    todo: Todo
    error: int


class TodoController:
    def __init__(self, db_path: str) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(
        self, title: str | List[str], description: str | List[str] = "", priority: TodoPriority = TodoPriority.Low
    ) -> TodoModel:
        """Add a to-do item to the database

        Args:
            title (str): The title of the to-do item
            description (str, optional): A description to the to-do item. Defaults to "".
            priority (TodoPriority, optional): To-do priority. It may be low, medium or high. Defaults to Low.

        Returns:
            Todo: The to-do item added to the database
        """
        if isinstance(title, list):
            title = " ".join(title)
        if isinstance(description, list):
            description = " ".join(description)

        todo = Todo(str(uuid1()), title, description, priority, False)

        read = self._db_handler.read_todos()

        if read.error == ReturnCode.DB_READ_ERROR:
            return TodoModel(todo, read.error)

        read.todo_list.append(todo.__dict__)

        write = self._db_handler.write_todos(read.todo_list)

        return TodoModel(todo, write.error)

    def list(self, completed: Optional[bool] = None, priority: Optional[int] = None) -> List[Todo]:
        read = self._db_handler.read_todos()

        todo_list = read.todo_list

        todo_list = (
            [todo for todo in todo_list if todo["completed"] == completed] if completed is not None else todo_list
        )

        todo_list = [todo for todo in todo_list if todo["priority"] == priority] if priority is not None else todo_list

        return [Todo(**todo) for todo in todo_list]

    def complete(self, todo_id: str) -> TodoModel:
        read = self._db_handler.read_todos()

        if read.error == ReturnCode.DB_READ_ERROR:
            return TodoModel(None, read.error)

        found = False
        for todo in read.todo_list:
            if str(todo["id"]).startswith(todo_id) and len(todo_id) > 5:
                todo["completed"] = True
                found = True
                break

        if found:
            write = self._db_handler.write_todos(read.todo_list)
            return TodoModel(Todo(**todo), write.error)
        else:
            return TodoModel(Todo(**todo), ReturnCode.ID_ERROR)
