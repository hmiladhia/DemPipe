from DPipe.context import PipeContext
from DPipe.action import SequentialPipe, ActionBase


class PipeExecutorBase:
    def __init__(self):
        self.context = PipeContext()

    def __enter__(self):
        self.start()
        self.context.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit(exc_type, exc_val, exc_tb)
        self.context.quit()

    # Actions
    def start(self):
        pass

    def quit(self, exc_type, exc_val, exc_tb):
        pass

    def execute_action(self, action, *args, **kwargs):
        if not isinstance(action, ActionBase):
            action = ActionBase.parse_action(action, *args, **kwargs)
        return action(*args, local_session=self.context, **kwargs)

    def execute(self, *args):
        pipe = SequentialPipe(*args, handler=self.handler)
        return self.execute_action(pipe)

    def handler(self, action: ActionBase, exception, *args, **kwargs):
        raise exception
