from DemPipe.action import ActionBase


class ContextSetter(ActionBase):
    def __init__(self, new=None, **kwargs):
        super(ContextSetter, self).__init__(new, **kwargs)

    def _execute(self, *args, local_session, **kwargs):
        local_session.update(self.kwargs)
        if callable(self.args[0]):
            local_session.update(self.args[0](local_session))

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError()
