from abc import ABC


class ActionBase(ABC):
    def __init__(self, *args, ctx_in=None, ctx_out='last_value', handler=None, **kwargs):
        self.ctx_in = ctx_in or []
        self.ctx_out = ctx_out
        self.args = args
        self.kwargs = kwargs
        self.action_name = self.__class__.__name__
        self._handler = handler

    def __call__(self, *args, local_session=None, **kwargs):
        try:
            return self._execute(*args, local_session=local_session, **kwargs)
        except Exception as e:
            self.handler(e, *args, **kwargs)

    def _execute(self, *args, local_session, **kwargs):
        raise NotImplementedError('You need to overide this method')

    def __str__(self):
        args = [str(arg) for arg in self.args] + [f'{key}={value}' for key, value in self.kwargs.items()]
        return f"{self.action_name}({', '.join(args)})"

    def __repr__(self):
        args = [str(arg) for arg in self.args] + [f'{key}={value}' for key, value in self.kwargs.items()]
        return f"{self.action_name}({', '.join(args)}, ctx_in={self.ctx_in}, ctx_out={self.ctx_out})"

    def handler(self, e, *args, **kwargs):
        if self._handler:
            self._handler(self, e, *args, **kwargs)
        else:
            raise e

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _child_parse(cls, t_action, *args, **kwargs):
        for sub_cls in cls.__subclasses__():
            try:
                return sub_cls.parse_action(t_action, *args, **kwargs)
            except (ValueError, NotImplementedError):
                continue
        raise ValueError

    @classmethod
    def parse_action(cls, t_action, *args, **kwargs):
        try:
            return cls._parse_action(t_action, *args, **kwargs)
        except (ValueError, NotImplementedError):
            return cls._child_parse(t_action, *args, **kwargs)
