import json

import pytest
from typer.testing import CliRunner

from todo import __app_name__, __version__, cli

runner = CliRunner()


test_data1 = {
    "title": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "title": "Clean the house.",
        "priority": 1,
        "description": "",
        "completed": False,
    },
}
test_data2 = {
    "title": ["Wash the car"],
    "priority": 2,
    "todo": {
        "title": "Wash the car.",
        "priority": 2,
        "completed": False,
    },
}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} (v{__version__})\n"


@pytest.fixture
def mock_json_file(temp_path):
    todo = [{
        "title": "Get some milk",
        "description": "1L of 2% milk.",
        "priority": 2,
        "completed": False
    }]
    db_file = temp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

