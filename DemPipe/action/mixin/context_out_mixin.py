from abc import ABC


class ContextOutMixin(ABC):
    def __init__(self, ctx_out=None):
        self.ctx_out = ctx_out

    def _update_context(self, loc_ctx, result):
        if isinstance(self.ctx_out, str):
            loc_ctx.update({self.ctx_out: result})
