# DemPipe

## Installation

A simple pip install will do :

```bash
python -m pip install DemPipe
```

## Use
```python
from DemPipe import PipeExecutor, Action

with PipeExecutor() as pipe:
    actions = [Action(lambda x: x**2, 2),  # returns 4
               Action(lambda x: x+3, ctx_in='last_value', ctx_out='my_result_name'),  # returns 4+3
               Action(lambda x: x*2, ctx_in='my_result_name')  # returns 2*7
              ]
    result = pipe.execute(actions)
    print('result:', result)  # 14
    print('result (from context):', pipe.context['last_value'])  # 14
    print('my_result_name:', pipe.context['my_result_name'])  # 7
```

You can also use a Trigger Action for conditional Actions in the pipeline ! 
```python
from DemPipe import PipeExecutor, Action, Trigger

with PipeExecutor() as pipe:
    actions = [Action(lambda x: x**2, 2),  # returns 4
               Trigger(lambda x: x==3,   # returns False -> executes the second action
                       Action(lambda x: x+3, ctx_in='last_value'),  # ignored
                       Action(lambda x: x+7, ctx_in='last_value'),  # returns 11
                       ctx_in='last_value')
              ]
    result = pipe.execute(actions)
    print('result:', result)  # 11
```

## Error Handling
In case an error occurs, you can configure an automatic e-mail to be sent with the traceback and the error message :
- Create a config file containing your credentials : 
```json
{
  "mail": {
    "mail_server": "smtp.gmail.com",
	"mail_port": 587,
	"mail_user": "${os_environ[user]}",
	"mail_password": "${os_environ[password]}",
	"mail_use_tls": true,
	"mail_default_receiver": "${os_environ[receiver]}"
  },
  "pipe_name": "My Pipe"
}
```

- Specify **config_file** to the **PipeExecutor**
```python
from DemPipe import PipeExecutor, Action

with PipeExecutor(config_file='ConfigsFolder.MyConfig') as pipe:
    pipe.execute(Action(lambda x: x/0, 2))  # raises ZeroDivisionException
```

## Other Types of actions

In addition to Trigger and Action there exist other kinds of actions :

- **ContextSetter**: Makes it easier to set context values :

```python
from DemPipe import SimplePipeExecutor, Action, ContextSetter

actions = [ContextSetter(var1=5, var2="test string"),
           Action(lambda x: x ** 2, ctx_in='var1')]
with SimplePipeExecutor() as pipe:
    print(pipe.execute(actions))  # 25

actions = [ContextSetter(lambda c: {'var1': c['var2'] * 3}, var2=4),
           Action(lambda x: x ** 2, ctx_in='var1')]

with SimplePipeExecutor() as pipe:
    print(pipe.execute(actions))  # 144
```

- **Procedure**: Same as an action but doesn't update the current context with its return value :

```python
from DemPipe import SimplePipeExecutor, Action, Procedure, ContextSetter

actions = [ContextSetter(last_value=3),
           Procedure(lambda x: x**2, ctx_in='last_value'),
           Action(lambda x: x + 2, ctx_in='last_value')]

with SimplePipeExecutor() as pipe:
    print(pipe.execute(actions))  # 5

```