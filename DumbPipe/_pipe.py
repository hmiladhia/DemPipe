import time

from random import random


from DumbPipe import ActionType, DSession
from DumbPipe._action import Action


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
            if not isinstance(action, Action):
                action = Action.parse_action(action)
            return self._execute_action(action, *args, **kwargs)
        except Exception as e:
            self.handle(e, action, *args, **kwargs)

    def _execute_action(self, action: Action, *args, **kwargs):
        assert isinstance(action, Action)
        result = action(*args, local_session=self.session, **kwargs)
        return result

    def execute(self, *args):
        actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                actions.extend(arg)
            else:
                actions.append(arg)
        ret = None
        for action in actions:
            ret = self.execute_action(action)
        return ret

    def handle(self, exception, action: ActionType, *args, **kwargs):
        raise exception
