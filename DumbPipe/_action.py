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
        self.local_session = {}

    def __call__(self, *args, **kwargs):
        result = self.action(*self.args, *args, **self.kwargs, **kwargs)
        if isinstance(self.sess_out, str):
            self.local_session = {self.sess_out: result}
        return result

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
