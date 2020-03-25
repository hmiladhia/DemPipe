from DemPipe import PipeExecutor, Action, Trigger

with PipeExecutor() as pipe:
    actions = [Action(lambda x: x**2, 2),  # returns 4
               Trigger(lambda x: x == 3,   # returns False -> executes the second action
                       Action(lambda x: x+3, ctx_in='last_value'),  # ignored
                       Action(lambda x: x+7, ctx_in='last_value'),  # returns 11
                       ctx_in='last_value')
              ]
    result = pipe.execute(actions)
    print('result:', result)  # 11
