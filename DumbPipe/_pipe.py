import time

from random import random


from DumbPipe import ActionType, DSession


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

    def execute_action(self, action: ActionType, *args, **kwargs):
        try:
            try:
                return self._execute_action(action, *args, as_helper=False, **kwargs)
            except TypeError as e:
                if str(e).endswith("got an unexpected keyword argument 'as_helper'"):
                    return self._execute_action(action, *args, **kwargs)
                else:
                    raise e
        except Exception as e:
            self.handle(e, action, *args, **kwargs)

    def _execute_action(self, action: ActionType, *args, **kwargs):
        assert isinstance(action, ActionType)

        if action == ActionType.Quit:
            return self.quit()
        elif action == ActionType.Wait:
            return self.wait(*args, **kwargs)
        elif action == ActionType.Custom:
            if 'callback' in kwargs:
                callback = kwargs.pop('callback')
            else:
                callback = args[0]
                args = args[1:]
            return callback(*args, **kwargs)
        else:
            return

    def execute(self, *args, _wait_time=None):
        actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                actions.extend(arg)
            else:
                actions.append(arg)

        for action in actions:
            options = []
            if type(action) == ActionType:
                action_type = action
            elif hasattr(action, '__len__') and len(action) == 2:
                action_type = action[0]
                options = action[1]
            elif hasattr(action, '__len__') and len(action) > 0:
                action_type = action[0]
                options = list(action[1:])
            else:
                raise ValueError("Action doesn't fit any format")

            if type(options) == dict:
                self.execute_action(action_type, **options)
            elif type(options) == list:
                self.execute_action(action_type, *options)
            else:
                self.execute_action(action_type, options)
        return self.session.get_last_value()

    def handle(self, exception, action: ActionType, *args, **kwargs):
        raise exception
