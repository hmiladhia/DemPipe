from DemPipe import SimplePipeExecutor, Action, ContextSetter

actions = [ContextSetter(var1=5, var2="test string"),
           Action(lambda x: x ** 2, ctx_in='var1')]
with SimplePipeExecutor() as pipe:
    print(pipe.execute(actions))  # 25

actions = [ContextSetter(lambda c: {'var1': c['var2'] * 3}, var2=4),
           Action(lambda x: x ** 2, ctx_in='var1')]

with SimplePipeExecutor() as pipe:
    print(pipe.execute(actions))  # 144
