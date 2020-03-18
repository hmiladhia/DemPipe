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


def test_pipe_execute_regular_session(pipe):
    actions = [Action(lambda x: x ** 2, 2),
               Action(lambda x: x * 3, sess_in='last_value')]
    assert pipe.execute(actions) == 12


def test_pipe_execute_regular_session_list(pipe):
    actions = [Action(lambda x: x ** 2, 2),
               Action(lambda x: x * 3, sess_in=['last_value'])]
    assert pipe.execute(actions) == 12


def test_pipe_execute_regular_session_dict(pipe):
    actions = [Action(lambda x: x ** 2, 2),
               Action(lambda x: x * 3, sess_in={'x': 'last_value'})]
    assert pipe.execute(actions) == 12


def test_pipe_execute_tuple_action(pipe):
    action = (my_function, [2], dict(param2=9))
    assert pipe.execute(action) == 11


def test_pipe_session_return_single_value(pipe):
    actions = [Action(lambda x: x**2, 3),
               Action(my_function, 2, param2=27, sess_out='test')]
    assert pipe.execute(actions) == 29
    assert pipe.session['last_value'] == 9
    assert pipe.session['test'] == 29

