from DemPipe.action import ActionBase
from DemPipe.action.mixin import ContextInMixin


class Procedure(ActionBase, ContextInMixin):
    def __init__(self, action, *args, ctx_in=None, ctx_out='last_value', handler=None, **kwargs):
        super(Procedure, self).__init__(*args, ctx_in=ctx_in, ctx_out=ctx_out, handler=handler, **kwargs)
        self.action = action
        self.action_name = self.action_name if self.action.__name__ == '<lambda>' else self.action.__name__

    def _execute(self, *args, loc_ctx, **kwargs):
        f_args, f_kwargs = self._get_f_args(*args, loc_ctx=loc_ctx, **kwargs)
        result = self.action(*f_args, **f_kwargs)
        return result

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError()
