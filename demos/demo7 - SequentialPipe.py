from DemPipe import SimplePipeExecutor, SequentialPipe, Action, Trigger

seq_pipe = SequentialPipe([Action(lambda x: x ** 2, 2),
                           Action(lambda x: x * 3, 5)])
actions = [Trigger(lambda x: x == 2, seq_pipe, Action(lambda x: x ** 2, 6), 2),
           Action(lambda a, b: a + b, 2, ctx_in={'b': 'last_value'})]
with SimplePipeExecutor() as pipe:
    print('result:', pipe.execute(actions))  # 17
