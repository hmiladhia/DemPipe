from enum import Enum


class Action(Enum):
    Get = 0
    Click = 1
    SendKeys = 2
    ScreenShot = 3
    Quit = -1
