class Action:
    id = -1

    def __init__(self, action, *args, sess_in=None, sess_out='last_value', **kwargs):
        self.sess_in = sess_in or []
        self.sess_out = sess_out
        self.__class__.id += 1
        self.id = self.id
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, local_session=None, **kwargs):
        return self._execute(*args, local_session=local_session, **kwargs)

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

    def __str__(self):
        args = [str(arg) for arg in self.args] + [f'{key}={value}' for key, value in self.kwargs.items()]
        return f"{'Action' if self.action.__name__ == '<lambda>' else self.action.__name__}({', '.join(args)})"

    @staticmethod
    def parse_action(t_action):
        args = []
        kwargs = {}
        if callable(t_action):
            action_func = t_action
        elif hasattr(t_action, '__len__') and 0 < len(t_action) <= 3:
            action_func = t_action[0]
            if len(t_action) > 1:
                args = t_action[1]
            if len(t_action) > 2:
                kwargs = t_action[2]
        else:
            raise ValueError("Action doesn't fit any format")
        return Action(action_func, *args, **kwargs)
