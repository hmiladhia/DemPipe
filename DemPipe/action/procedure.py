from DemPipe.action import ActionBase


class Procedure(ActionBase):
    def __init__(self, action, *args, ctx_in=None, ctx_out='last_value', handler=None, **kwargs):
        super(Procedure, self).__init__(*args, ctx_in=ctx_in, ctx_out=ctx_out, handler=handler, **kwargs)
        self.action = action
        self.action_name = self.action_name if self.action.__name__ == '<lambda>' else self.action.__name__

    def _execute(self, *args, local_session, **kwargs):
        f_args, f_kwargs = self.__get_f_args(*args, local_session=local_session, **kwargs)
        result = self.action(*f_args, **f_kwargs)
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
        if isinstance(self.ctx_in, dict):
            s_kwargs.update({key: local_session[value] for key, value in self.ctx_in.items()})
        elif isinstance(self.ctx_in, list):
            s_args = [local_session[arg_name] for arg_name in self.ctx_in]
        elif isinstance(self.ctx_in, str):
            s_args = [local_session[self.ctx_in]]
        return s_args, s_kwargs

    @staticmethod
    def _parse_action(t_action, *args, **kwargs):
        raise NotImplementedError()
