"""Entry-point script to run the app from the package"""

from todo import __app_name__, cli


def main() -> None:
    """Entry-point function to run the app"""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
