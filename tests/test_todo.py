import json

import pytest
from typer.testing import CliRunner

from todo import ReturnCode, __app_name__, __version__, cli
from todo.todo import TodoController

runner = CliRunner()


test_data1 = {
    "title": ["Clean", "the", "house."],
    "description": "A very dirty house.",
    "priority": 1,
    "todo": {
        "id": "0a50d7fa-5f92-11ee-8697-00155d3d2824",
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
        "id": "b72f3c9c-5f91-11ee-8fd4-00155d3d2824",
        "title": "Wash the car.",
        "description": "A very dirty car.",
        "priority": 2,
        "completed": False,
    },
}
test_data3 = {
    "title": "Clean the garden.",
    "description": ["A", "very", "dirty", "garden."],
    "priority": 1,
    "todo": {
        "id": "0a50d7fa-5f92-11ee-8697-00155d3d2825",
        "title": "Clean the garden.",
        "description": "A very dirty garden.",
        "priority": 1,
        "completed": False,
    },
}
test_data4 = {
    "title": ["Clean", "everything."],
    "description": ["Everything", "is", "nasty."],
    "priority": 1,
    "todo": {
        "id": "0a50d7fa-5f92-11ee-8697-00155d3d2826",
        "title": "Clean everything.",
        "description": "Everything is nasty.",
        "priority": 1,
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
    todo = [
        {
            "id": " b72f3c9c-5f91-11ee-8fd4-00155d3d2824",
            "title": "Get some milk",
            "description": "1L of 2% milk.",
            "priority": 2,
            "completed": False,
        }
    ]
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
        pytest.param(
            test_data3["title"],
            test_data3["description"],
            test_data3["priority"],
            (test_data3["todo"], ReturnCode.SUCCESS),
        ),
        pytest.param(
            test_data4["title"],
            test_data4["description"],
            test_data4["priority"],
            (test_data4["todo"], ReturnCode.SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, title, description, priority, expected):
    controller = TodoController(mock_json_file)

    read = controller._db_handler.read_todos()
    assert len(read.todo_list) == 1

    model = controller.add(title, description, priority)
    read = controller._db_handler.read_todos()
    assert len(read.todo_list) == 2

    assert model.error == expected[1]
    assert not model.todo.completed
    assert model.todo.id is not None
    assert model.todo.title == expected[0]["title"]
    assert model.todo.description == expected[0]["description"]
    assert model.todo.priority == expected[0]["priority"]
