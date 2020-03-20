from DumbPipe.action import ActionBase


class Action(ActionBase):
    def __init__(self, action, *args, sess_in=None, sess_out='last_value', handler=None, **kwargs):
        super(Action, self).__init__(*args, sess_in=sess_in, sess_out=sess_out, handler=handler, **kwargs)
        self.action = action
        self.action_name = self.action_name if self.action.__name__ == '<lambda>' else self.action.__name__

    def _execute(self, *args, local_session, **kwargs):
        f_args, f_kwargs = self.__get_f_args(*args, local_session=local_session, **kwargs)
        result = self.action(*f_args, **f_kwargs)
        if isinstance(self.sess_out, str):
            local_session.update({self.sess_out: result})
        return result

    def __get_f_args(self, *args, local_session=None, **kwargs):
        s_args, s_kwargs = self.__get_s_args(local_session)
        f_args = list(args or self.args) + s_args
        f_kwargs = self.kwargs.copy()
        f_kwargs.update(s_kwargs)
        f_kwargs.update(kwargs)
        return f_args, f_kwargs

    def __get_s_args(self, local_session):
        s_args = []
        s_kwargs = {}
        if isinstance(self.sess_in, dict):
            s_kwargs.update({key: local_session[value] for key, value in self.sess_in.items()})
        elif isinstance(self.sess_in, list):
            s_args = [local_session[arg_name] for arg_name in self.sess_in]
        elif isinstance(self.sess_in, str):
            s_args = [local_session[self.sess_in]]
        return s_args, s_kwargs

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
