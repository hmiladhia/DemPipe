from DemPipe import PipeExecutor, Action

with PipeExecutor(config_file='DemPipe.PipeConfig') as pipe:
    pipe.execute(Action(lambda x: x/0, 2))  # raises ZeroDivisionException
