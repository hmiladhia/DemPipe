from DemPipe.action import ActionBase


class SequentialPipe(ActionBase):
    def __init__(self, *args, ctx_out='last_value', handler=None):
        super(SequentialPipe, self).__init__(*args, ctx_out=ctx_out, handler=handler)
        self.actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                self.actions.extend(arg)
            else:
                self.actions.append(arg)

    def _execute(self, *args, loc_ctx=None, **kwargs):
        ret = None
        action: ActionBase
        for action in self.actions:
            if not isinstance(action, ActionBase):
                action = ActionBase.parse_action(action)
            ret = action(loc_ctx=loc_ctx)
        return ret

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        return SequentialPipe(*t_action)
