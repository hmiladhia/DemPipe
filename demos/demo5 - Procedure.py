from DemPipe import SimplePipeExecutor, Action, Procedure, ContextSetter

actions = [ContextSetter(last_value=3),
           Procedure(lambda x: x**2, ctx_in='last_value'),
           Action(lambda x: x + 2, ctx_in='last_value')]

with SimplePipeExecutor() as pipe:
    print('result:', pipe.execute(actions))  # 5
