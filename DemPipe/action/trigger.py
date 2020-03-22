from DemPipe.action import Action


class Trigger(Action):
    def __init__(self, trigger_func, true_action, false_action=None, *args, ctx_in=None,
                 ctx_out='trigger_value', handler=None, **kwargs):
        super(Trigger, self).__init__(trigger_func, *args, ctx_in=ctx_in, ctx_out=ctx_out,
                                      handler=handler, **kwargs)
        self.true_action = true_action
        self.false_action = false_action

    def _execute(self, *args, loc_ctx=None, **kwargs):
        if super(Trigger, self)._execute(*args, loc_ctx=loc_ctx, **kwargs):
            return self.true_action(loc_ctx=loc_ctx)
        elif self.false_action:
            return self.false_action(loc_ctx=loc_ctx)
