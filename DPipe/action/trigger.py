from DPipe.action import Action


class Trigger(Action):
    def __init__(self, trigger_func, true_action, false_action=None, *args, ctx_in=None,
                 ctx_out='trigger_value', handler=None, **kwargs):
        super(Trigger, self).__init__(trigger_func, *args, ctx_in=ctx_in, ctx_out=ctx_out,
                                      handler=handler, **kwargs)
        self.true_action = true_action
        self.false_action = false_action

    def _execute(self, *args, local_session=None, **kwargs):
        if super(Trigger, self)._execute(*args, local_session=local_session, **kwargs):
            return self.true_action(local_session=local_session)
        elif self.false_action:
            return self.false_action(local_session=local_session)
