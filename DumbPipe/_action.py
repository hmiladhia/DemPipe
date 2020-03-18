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
