from DemPipe.action import Procedure
from DemPipe.action.mixin import ContextOutMixin


class Action(Procedure, ContextOutMixin):
    def __init__(self, action, *args, ctx_in=None, ctx_out='last_value', handler=None, **kwargs):
        super(Action, self).__init__(action, *args, ctx_in=ctx_in, ctx_out=ctx_out, handler=handler, **kwargs)

    @ContextOutMixin.update_context
    def _execute(self, *args, loc_ctx, **kwargs):
        return super(Action, self)._execute(*args, loc_ctx=loc_ctx, **kwargs)

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        args = []
        kwargs = {}
        if callable(t_action):
            action_func = t_action
        elif isinstance(t_action, tuple) and 0 < len(t_action) <= 3:
            action_func = t_action[0]
            if len(t_action) > 1:
                args = t_action[1]
            if len(t_action) > 2:
                kwargs = t_action[2]
        else:
            raise ValueError("Action doesn't fit any format")
        return Action(action_func, *args, **kwargs)
