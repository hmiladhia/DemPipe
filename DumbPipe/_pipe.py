import time

from random import random


from DumbPipe import DSession
from DumbPipe._action_base import ActionBase
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

    def wait(self, wait_time=None):
        time.sleep(wait_time or random())

    def start(self):
        pass

    def quit(self):
        pass

    def execute_action(self, action, *args, **kwargs):
        if not isinstance(action, ActionBase):
            action = ActionBase.parse_action(action, *args, **kwargs)
        return action(*args, local_session=self.session, **kwargs)

    def execute(self, *args):
        pipe = SequentialPipe(*args, handler=self.handler)
        return self.execute_action(pipe)

    def handler(self, exception, action: ActionBase, *args, **kwargs):
        raise exception
