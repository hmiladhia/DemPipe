from DemPipe.action import ActionBase


class ContextSetter(ActionBase):
    def __init__(self, new=None, **kwargs):
        super(ContextSetter, self).__init__(new, **kwargs)

    def _execute(self, *args, loc_ctx, **kwargs):
        loc_ctx.update(self.kwargs)
        if callable(self.args[0]):
            loc_ctx.update(self.args[0](loc_ctx))

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError()
