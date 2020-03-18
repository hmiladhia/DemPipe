from DumbPipe._action import Action


class Trigger(Action):
    def __init__(self, trigger_func, true_action, false_action=None, *args, sess_in=None, sess_out='trigger_value', **kwargs):
        self.true_action = true_action
        self.false_action = false_action
        super(Trigger, self).__init__(trigger_func, *args, sess_in=sess_in, sess_out=sess_out, **kwargs)

    def __call__(self, *args, local_session=None, **kwargs):
        if self._execute(*args, local_session=local_session, **kwargs):
            return self.true_action(local_session=local_session)
        elif self.false_action:
            return self.false_action(local_session=local_session)
