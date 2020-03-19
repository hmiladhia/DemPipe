from abc import ABC


class ActionBase(ABC):
    def __init__(self, *args, sess_in=None, sess_out='last_value', **kwargs):
        self.sess_in = sess_in or []
        self.sess_out = sess_out
        self.args = args
        self.kwargs = kwargs
        self.action_name = self.__class__.__name__

    def __call__(self, *args, local_session=None, **kwargs):
        return self._execute(*args, local_session=local_session, **kwargs)

    def _execute(self, *args, local_session, **kwargs):
        raise NotImplementedError('You need to overide this method')

    def __str__(self):
        args = [str(arg) for arg in self.args] + [f'{key}={value}' for key, value in self.kwargs.items()]
        return f"{self.action_name}({', '.join(args)})"

    def __repr__(self):
        args = [str(arg) for arg in self.args] + [f'{key}={value}' for key, value in self.kwargs.items()]
        return f"{self.action_name}({', '.join(args)}, sess_in={self.sess_in}, sess_out={self.sess_out})"
