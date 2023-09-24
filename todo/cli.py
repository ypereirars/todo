"""Provides the Command-Line Interface for the application"""

from pathlib import Path
from typing import Optional

from typer import Exit, Option, Typer, colors, echo, secho

from todo import ERRORS, ReturnCode, __app_name__, __version__, config, database

app = Typer()


@app.command()
def init(
    db_path: Optional[str] = Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        help="Path to the to-do database",
        prompt="to-do database location?"
    )
) -> None:
    """Initialize the application's configuration and database"""
    app_return_code = config.init_app(db_path)

    if app_return_code != ReturnCode.SUCCESS:
        secho(
            f'Creating config file failed with "{ERRORS[app_return_code]}"',
            fg=colors.RED
        )
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


def _version_callback(value: bool) -> None:
    """Print the version of the application"""
    if value:
        echo(f"{__app_name__} (v{__version__})")
        raise Exit()


@app.callback()
def main(
    version: Optional[bool] = Option(
        None, "--version", "-v",
        callback=_version_callback,
        is_eager=True,
        help="Show the application's version and exit"
    )
) -> None:
    """Manage your to-do list"""

    return
