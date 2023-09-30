"""Provides the Command-Line Interface for the application"""

from pathlib import Path
from typing import List, Optional

from typer import Argument, Exit, Option, Typer, colors, echo, secho

from todo import ERRORS, ReturnCode, __app_name__, __version__, config, database
from todo.todo import TodoController

app = Typer()


@app.command()
def init(
    db_path: Optional[str] = Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        help="Path to the to-do database",
        prompt="to-do database location?",
    )
) -> None:
    """Initialize the application's configuration and database"""
    app_return_code = config.init_app(db_path)

    if app_return_code != ReturnCode.SUCCESS:
        secho(f'Creating config file failed with "{ERRORS[app_return_code]}"', fg=colors.RED)
        raise Exit(code=app_return_code.value)

    db_return_code = database.init_database(Path(db_path))
    if db_return_code == ReturnCode.SUCCESS:
        secho(f"The to-do database is {db_path}", fg=colors.GREEN)
    else:
        secho(
            f'Creating database failed with "{ERRORS[db_return_code]}"',
            fg=colors.RED,
        )
        raise Exit(1)


@app.command()
def add(
    title: List[str] = Argument(..., help="Title of the to-do item"),
    description: Optional[str] = Option(
        [],
        "--description",
        "-d",
        help="Description of the to-do item. Defaults to empty.",
    ),
    priority: Optional[int] = Option(
        0,
        "--priority",
        "-p",
        min=0,
        max=3,
        help="Priority of the to-do item. It may either be 0 (low), 1 (medium) or 2 (high). Defaults to 0.",
    ),
) -> None:
    """Add a to-do item to the database"""
    controller = get_todoer()

    model = controller.add(title, description, priority)
    if model.error == ReturnCode.SUCCESS:
        secho(
            f'to-do "{model.todo.title}" was added with {model.todo.priority.name.lower()} priority.',
            fg=colors.GREEN,
        )
    else:
        secho(f'Adding to-do item failed with "{ERRORS[model.error]}"', fg=colors.RED)
        raise Exit(1)


@app.command(name="list")
def list_all(
    completed: Optional[bool] = Option(
        None,
        "--completed",
        "-c",
        help="Filter completed to-do items",
    ),
    not_completed: Optional[bool] = Option(
        None,
        "--not-completed",
        "-nc",
        help="Filter not completed to-do items",
    ),
    priority: Optional[int] = Option(
        None,
        "--priority",
        "-p",
        min=0,
        max=3,
        help="Filter to-do items by priority",
    ),
) -> None:
    """List to-do items"""
    controller = get_todoer()

    if completed is not None and not_completed is not None:
        secho("You can't filter by both completed and not completed to-do items", fg=colors.RED)
        raise Exit(1)

    status = None
    if completed is not None:
        status = completed
    elif not_completed is not None:
        status = not not_completed

    todo_list = controller.list(status, priority)

    if len(todo_list) == 0:
        secho("There are no tasks in the to-do list yet", fg=colors.RED)
        raise Exit()

    secho("\nto-do list:\n", fg=colors.BLUE, bold=True)
    columns = (
        f"{' '* 16} ID {' ' * 16} ",
        "| Priority ",
        "| Completed ",
        "| Description  ",
    )
    headers = "".join(columns)
    secho(headers, fg=colors.BLUE, bold=True)
    secho("-" * len(headers), fg=colors.BLUE)

    for todo in todo_list:
        description = (" - " + todo.description) if todo.description else ""
        description = description[: len(columns[3])] + "..." if len(description) > len(columns[3]) else description
        secho(
            f"{todo.id} "
            f"|   {todo.priority.name}{(len(columns[1]) - len(str(todo.priority.name))-4) * ' '}"
            f"|   {todo.completed}{(len(columns[2]) - len(str(todo.completed)) - 4) * ' '}"
            f"| {todo.title}{description}{(len(columns[3]) - len(description) - 2) * ' '}",
            fg=colors.BLUE,
        )
    secho("-" * len(headers) + "\n", fg=colors.BLUE)
    # for todo in model.todo_list:
    #     echo(f"{todo.id} {todo.title} {todo.priority.name.lower()} {todo.completed}")
    # else:
    #     secho(f'Listing to-do items failed with "{ERRORS[model.error]}"', fg=colors.RED)
    #     raise Exit(1)


def _version_callback(value: bool) -> None:
    """Print the version of the application"""
    if value:
        echo(f"{__app_name__} (v{__version__})")
        raise Exit()


def get_todoer() -> TodoController:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        secho(
            'Config file not found. Please, run "rptodo init"',
            fg=colors.RED,
        )
        raise Exit(1)
    if db_path.exists():
        return TodoController(db_path)
    else:
        secho(
            'Database not found. Please, run "rptodo init"',
            fg=colors.RED,
        )
        raise Exit(1)


@app.callback()
def main(
    version: Optional[bool] = Option(
        None,
        "--version",
        "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show the application's version and exit",
    )
) -> None:
    """Manage your to-do list"""

    return
