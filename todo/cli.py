"""Provides the Command-Line Interface for the application"""

from typing import Optional

from typer import Exit, Option, Typer, echo

from todo import __app_name__, __version__

app = Typer()


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
