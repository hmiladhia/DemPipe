import pytest

from DumbPipe import DPipe, Action


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with DPipe() as pipe:
        yield pipe


def my_function(param1, param2=3):
    return param1 + param2


def test_pipe_execute_lambda_action(pipe):
    assert pipe.execute_action(Action(lambda x: x**2, 2)) == 4
    assert pipe.session['last_value'] == 4


def test_pipe_execute_action(pipe):
    assert pipe.execute_action(Action(my_function, 2)) == 5
    assert pipe.session['last_value'] == 5


def test_pipe_execute(pipe):
    actions = [Action(lambda x: x ** 2, 2),
               Action(lambda x: x * 3, 5)]
    assert pipe.execute(actions) == 15


def test_pipe_execute_tuple_action(pipe):
    actions = [(my_function, [2], dict(param2=9))]
    assert pipe.execute(actions) == 11

