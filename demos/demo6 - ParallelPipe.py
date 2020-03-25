import time

from DemPipe import SimplePipeExecutor, ParallelPipe, Action

t0 = time.time()
actions = ParallelPipe(Action(lambda sec: time.sleep(sec) or sec, 0.2),
                       Action(lambda sec: time.sleep(sec) or sec, 0.5),
                       Action(lambda sec: time.sleep(sec) or sec, 0.3),
                       Action(lambda sec: time.sleep(sec) or sec, 0.2))

with SimplePipeExecutor() as pipe:
    print('result:', pipe.execute(actions))  # [0.2, 0.5, 0.3, 0.2]
    print('time:', time.time() - t0)
