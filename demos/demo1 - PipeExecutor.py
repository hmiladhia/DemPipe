from DemPipe import SimplePipeExecutor, Action

with SimplePipeExecutor() as pipe:
    actions = [Action(lambda x: x**2, 2),  # returns 4
               Action(lambda x: x+3, ctx_in='last_value', ctx_out='my_result_name'),  # returns 4+3
               Action(lambda x: x*2, ctx_in='my_result_name')  # returns 2*7
              ]
    result = pipe.execute(actions)
    print('result:', result)  # 14
    print('result (from context):', pipe.context['last_value'])  # 14
    print('my_result_name:', pipe.context['my_result_name'])  # 7
