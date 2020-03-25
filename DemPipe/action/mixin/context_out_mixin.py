from abc import ABC
from functools import wraps


class ContextOutMixin(ABC):
    def __init__(self, ctx_out=None):
        self.ctx_out = ctx_out

    def _update_context(self, loc_ctx, result):
        if isinstance(self.ctx_out, str):
            loc_ctx.update({self.ctx_out: result})

    @staticmethod
    def update_context(func):
        @wraps(func)
        def wrapper(self, *args, loc_ctx=None, **kwargs):
            result = func(self, *args, loc_ctx=loc_ctx, **kwargs)
            self._update_context(loc_ctx, result)
            return result
        return wrapper
