import time

from random import random


from DumbPipe import ActionType, DSession
from DumbPipe._action_base import ActionBase
from DumbPipe._action import Action
from DumbPipe._sequential_pipe import SequentialPipe


class DPipeExec:
    def __init__(self):
        self.session = DSession()

    def __enter__(self):
        self.start()
        self.session.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        self.session.quit()

    # Actions

    @DSession.procedural_action()
    def wait(self, wait_time=None):
        time.sleep(wait_time or random())

    @DSession.procedural_action()
    def start(self):
        pass

    @DSession.procedural_action()
    def quit(self):
        pass

    def execute_action(self, action, *args, **kwargs):
        try:
            return self._execute_action(action, *args, **kwargs)
        except Exception as e:
            self.handle(e, action, *args, **kwargs)

    def _execute_action(self, action: ActionBase, *args, **kwargs):
        assert isinstance(action, ActionBase)
        return action(*args, local_session=self.session, **kwargs)

    def execute(self, *args):
        pipe = SequentialPipe(*args)
        return self.execute_action(pipe)

    def handle(self, exception, action: ActionType, *args, **kwargs):
        raise exception
