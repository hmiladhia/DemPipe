import pytest

from DumbPipe import DPipeExec, Action, Trigger, SequentialPipe


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with DPipeExec() as pipe:
        yield pipe


class DebugAction(Action):
    def __call__(self, *args, local_session=None, **kwargs):
        print(local_session.to_dict())
        return self._execute(*args, local_session=local_session, **kwargs)


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


def test_pipe_trigger_true(pipe):
    actions = [Trigger(lambda x: x == 2, Action(lambda x: x**2, 3), Action(lambda x: x**2, 6), 2),
               Action(my_function, 2, sess_in={'param2': 'last_value'})]
    assert pipe.execute(actions) == 11


def test_pipe_trigger_false(pipe):
    actions = [Trigger(lambda x: x == 2, Action(lambda x: x**2, 3), Action(lambda x: x**2, 6), 3),
               Action(my_function, 2, sess_in={'param2': 'last_value'})]
    assert pipe.execute(actions) == 38


@pytest.mark.parametrize("action, expected", [
    (Action(lambda x: x**2, 2), 'Action'),
    (Action(my_function, 2), 'my_function'),
    (Trigger(lambda x: x == 2, lambda x: x, 2), 'Trigger'),
    (Trigger(my_function, lambda x: x, 2), 'my_function'),
])
def test_action_name(action, expected):
    assert action.action_name == expected


def test_seq_pipe(pipe):
    actions = SequentialPipe([Action(lambda x: x ** 2, 2),
                              Action(lambda x: x * 3, 5)])
    assert pipe.execute(actions) == 15


def test_pipe_trigger_seq_pipe(pipe):
    seq_pipe = SequentialPipe([Action(lambda x: x ** 2, 2),
                              Action(lambda x: x * 3, 5)])
    actions = [Trigger(lambda x: x == 2, seq_pipe, Action(lambda x: x**2, 6), 2),
               Action(my_function, 2, sess_in={'param2': 'last_value'})]
    assert pipe.execute(actions) == 17
