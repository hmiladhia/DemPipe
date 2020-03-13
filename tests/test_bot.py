"""
Credits : htmlcheatsheet was taken from Traversy Media tutorial that you can find at the following link :
    https://www.youtube.com/watch?v=UB1O30fR-EE
"""
import os

import pytest
import selenium

from SeleniumBot.Bot import Action, Bot


class CheatSheetBot(Bot):
    def __init__(self, driver=None, options=None):
        if options is None:
            options = selenium.webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument('--headless')
        super(CheatSheetBot, self).__init__(f'file:///{os.getcwd()}/htmlcheatsheet/index.html', driver, options)

    def my_custom(self, arg1):
        print(f'Hello {arg1}')


@pytest.fixture(scope='session', autouse=True)
def bot():
    with CheatSheetBot() as bot:
        yield bot


@pytest.mark.parametrize('actions', [
    Action.Get,
    [Action.Get],
    (Action.SendKeys, "/html/body/form/div[4]/textarea", "Hello World"),
    (Action.SendKeys, ["/html/body/form/div[4]/textarea", "Hello World"]),
    (Action.SendKeys, {"xpath": "/html/body/form/div[4]/textarea", "text": "Hello World"}),
    [Action.Get, (Action.SendKeys, "/html/body/form/div[4]/textarea", "Hello World")],
])
def test_execute(actions, bot):
    bot.execute(actions, _wait_time=0)


def test_execute_with_two_actions(bot):
    actions = [Action.Get, (Action.SendKeys, "/html/body/form/div[4]/textarea", "Hello World")]
    bot.execute(actions, actions, _wait_time=0)
