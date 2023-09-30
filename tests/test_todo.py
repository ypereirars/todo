import json

import pytest
from typer.testing import CliRunner

from todo import ReturnCode, __app_name__, __version__, cli
from todo.todo import TodoController

runner = CliRunner()


test_data1 = {
    "title": "Clean the house.",
    "description": "A very dirty house.",
    "priority": 1,
    "todo": {
        "title": "Clean the house.",
        "description": "A very dirty house.",
        "priority": 1,
        "completed": False,
    },
}
test_data2 = {
    "title": "Wash the car.",
    "description": "A very dirty car.",
    "priority": 2,
    "todo": {
        "title": "Wash the car.",
        "description": "A very dirty car.",
        "priority": 2,
        "completed": False,
    },
}


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} (v{__version__})\n"


@pytest.fixture
def mock_json_file(tmp_path):
    """Docstring"""
    todo = [{"title": "Get some milk", "description": "1L of 2% milk.", "priority": 2, "completed": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file


@pytest.mark.parametrize(
    "title, description, priority, expected",
    [
        pytest.param(
            test_data1["title"],
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], ReturnCode.SUCCESS),
        ),
        pytest.param(
            test_data2["title"],
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], ReturnCode.SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, title, description, priority, expected):
    controller = TodoController(mock_json_file)
    todo = controller.add(title, description, priority)

    assert not todo.completed
    assert todo.title == expected[0]["title"]
    assert todo.description == expected[0]["description"]
    assert todo.priority == expected[0]["priority"]
