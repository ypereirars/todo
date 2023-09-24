from typer.testing import CliRunner

from todo import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} (v{__version__})\n"
