from abc import ABC

from typing import List, Dict, Any


class ContextInMixin(ABC):
    args: List
    kwargs: Dict
    ctx_in: Any

    def _get_f_args(self, *args, loc_ctx=None, **kwargs):
        s_args, s_kwargs = self.__get_s_args(loc_ctx)
        f_args = list(args or self.args) + s_args
        f_kwargs = self.kwargs.copy()
        f_kwargs.update(s_kwargs)
        f_kwargs.update(kwargs)
        return f_args, f_kwargs

    def __get_s_args(self, loc_ctx):
        s_args = []
        s_kwargs = {}
        if isinstance(self.ctx_in, dict):
            s_kwargs.update({key: loc_ctx[value] for key, value in self.ctx_in.items()})
        elif isinstance(self.ctx_in, list):
            s_args = [loc_ctx[arg_name] for arg_name in self.ctx_in]
        elif isinstance(self.ctx_in, str):
            s_args = [loc_ctx[self.ctx_in]]
        return s_args, s_kwargs
