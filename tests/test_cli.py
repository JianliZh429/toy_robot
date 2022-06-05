import sys
from io import StringIO
from unittest import mock

import pytest

from toy_robot.cli import automatic_mode, interactive_mode


@mock.patch("sys.stdout", new_callable=StringIO)
def test_automatic_mode_commands_1(stdout):
    commands_filepath = "resources/commands_01.txt"
    automatic_mode(commands_filepath)
    assert stdout.getvalue() == "Output: 0,1,NORTH\n"


@mock.patch("sys.stdout", new_callable=StringIO)
def test_automatic_mode_commands_2(stdout):
    commands_filepath = "resources/commands_02.txt"
    automatic_mode(commands_filepath)
    assert stdout.getvalue() == "Output: 0,0,WEST\n"


@mock.patch("sys.stdout", new_callable=StringIO)
def test_automatic_mode_commands_3(stdout):
    commands_filepath = "resources/commands_03.txt"
    automatic_mode(commands_filepath)
    assert stdout.getvalue() == "Output: 3,3,NORTH\n"


@mock.patch("sys.stdout", new_callable=StringIO)
def test_automatic_mode_commands_4_when_move_out_of_table(stdout):
    commands_filepath = "resources/commands_04.txt"
    automatic_mode(commands_filepath)
    assert stdout.getvalue() == (
        "This movement may endanger the robot, refuse to move\n"
        "This movement may endanger the robot, refuse to move\n"
        "This movement may endanger the robot, refuse to move\n"
        "Output: 4,3,NORTH\n"
    )


def test_automatic_mode_commands_5_when_place_command_not_first():
    commands_filepath = "resources/commands_05.txt"
    with pytest.raises(ValueError) as exc_info:
        automatic_mode(commands_filepath)
    assert exc_info.value.args[0] == (
        "Please use PLACE command to put the robot on the table first, then you can order the robot to move"
    )


@mock.patch("sys.stdout", new_callable=StringIO)
def test_interactive_mode(stdout):
    sys.stdin = StringIO(
        "5\n"
        "PLACE 0,0,NORTH\n"
        "MOVE\n"
        "REPORT\n"
        "EOF"
    )
    interactive_mode()
    assert stdout.getvalue() == (
        "Welcome to toy robot game! Choose a table size, then you can command the "
        "robot to move on the table.\n"
        "\n"
        "Please input the table size, default size is 5x5: \n"
        "PLACE command to set the robot position on the table;\n"
        "MOVE command to order the robot move one step forward;\n"
        "LEFT command to order the robot turn left;\n"
        "RIGHT command to order the robot turn right;\n"
        "REPORT command to order the robot report its current position;\n"
        "Ctrl+C or EOF to exit\n"
        "\n"
        "Please input your command: \n"
        "Output: 0,1,NORTH\n"
    )


@mock.patch("sys.stdout", new_callable=StringIO)
def test_interactive_mode_reordered_commands(stdout):
    sys.stdin = StringIO(
        "5\n"
        "PLACE 0,0,NORTH\n"
        "MOVE\n"
        "REPORT\n"
        "right\n"
        "Move\n"
        "REPORT\n"
        "EOF"
    )
    interactive_mode()
    assert stdout.getvalue() == (
        "Welcome to toy robot game! Choose a table size, then you can command the "
        "robot to move on the table.\n"
        "\n"
        "Please input the table size, default size is 5x5: \n"
        "PLACE command to set the robot position on the table;\n"
        "MOVE command to order the robot move one step forward;\n"
        "LEFT command to order the robot turn left;\n"
        "RIGHT command to order the robot turn right;\n"
        "REPORT command to order the robot report its current position;\n"
        "Ctrl+C or EOF to exit\n"
        "\n"
        "Please input your command: \n"
        "Output: 0,1,NORTH\n"
        "Output: 1,1,EAST\n"
    )