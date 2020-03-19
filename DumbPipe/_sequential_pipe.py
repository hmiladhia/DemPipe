from DumbPipe._action_base import ActionBase
from DumbPipe._action import Action


class SequentialPipe(ActionBase):
    def __init__(self, *args, sess_out='last_value'):
        super(SequentialPipe, self).__init__(*args, sess_out=sess_out)
        self.actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                self.actions.extend(arg)
            else:
                self.actions.append(arg)

    def _execute(self, *args, local_session=None, **kwargs):
        ret = None
        action: ActionBase
        for action in self.actions:
            if not isinstance(action, ActionBase):
                action = Action.parse_action(action)
            ret = action(local_session=local_session)
        return ret
