import pytest

from DemPipe import PipeExecutorBase, Action, ContextSetter, Procedure


@pytest.fixture(scope='session', autouse=True)
def pipe():
    with PipeExecutorBase() as pipe:
        yield pipe


def test_context_setter(pipe):
    actions = [ContextSetter(variable1=5, variable2="love"), Action(lambda x: x**2, ctx_in='variable1')]
    assert pipe.execute(actions) == 25


def test_context_setter_lambda(pipe):
    actions = [ContextSetter(lambda c: {'variable1': c['variable2'] * 3}, variable2=4),
               Action(lambda x: x**2, ctx_in='variable1')]
    assert pipe.execute(actions) == 144


def test_procedure(pipe):
    actions = [ContextSetter(last_value=3),
               Procedure(lambda x: x**2, ctx_in='last_value'),
               Action(lambda x: x + 2, ctx_in='last_value')]
    assert pipe.execute(actions) == 5
