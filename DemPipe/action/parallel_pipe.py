import concurrent.futures

from DemPipe.action import ActionBase


class ParallelPipe(ActionBase):
    def __init__(self, *args, ctx_out=None, handler=None):
        super(ParallelPipe, self).__init__(*args, ctx_out=ctx_out, handler=handler)
        self.actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                self.actions.extend(arg)
            else:
                self.actions.append(arg)

    def _execute(self, *args, loc_ctx=None, **kwargs):
        ret = []
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            action: ActionBase
            for action in self.actions:
                if not isinstance(action, ActionBase):
                    action = ActionBase.parse_action(action)
                results.append(executor.submit(action, loc_ctx=loc_ctx))

        for result in results:
            ret.append(result.result())

        return ret

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError()
