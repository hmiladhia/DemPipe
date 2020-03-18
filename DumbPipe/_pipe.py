import time

from random import random


from DumbPipe import ActionType, DSession
from DumbPipe._action import Action


class DPipe:
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

    def _execute_action(self, action: Action, *args, **kwargs):
        assert isinstance(action, Action)
        result = action(*args, **kwargs)
        self.session.update(action.local_session)
        return result

    def execute(self, *args):
        actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                actions.extend(arg)
            else:
                actions.append(arg)

        for action in actions:
            if isinstance(action, Action):
                self.execute_action(action)
            else:
                args = []
                kwargs = {}
                if callable(action) == ActionType:
                    action_func = action
                elif hasattr(action, '__len__') and 0 < len(action) <= 3:
                    action_func = action[0]
                    if len(action) > 1:
                        args = action[1]
                    if len(action) > 2:
                        kwargs = action[2]
                else:
                    print(len(action))
                    raise ValueError("Action doesn't fit any format")

                self.execute_action(Action(action_func, *args, **kwargs))
        return self.session.get_last_value()

    def handle(self, exception, action: ActionType, *args, **kwargs):
        raise exception
