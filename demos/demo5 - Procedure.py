from DemPipe import PipeExecutorBase, Action, Procedure, ContextSetter

actions = [ContextSetter(last_value=3),
           Procedure(lambda x: x**2, ctx_in='last_value'),
           Action(lambda x: x + 2, ctx_in='last_value')]

with PipeExecutorBase() as pipe:
    print(pipe.execute(actions))  # 5
