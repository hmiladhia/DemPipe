"""
Credits : htmlcheatsheet was taken from Traversy Media tutorial that you can find at the following link :
    https://www.youtube.com/watch?v=UB1O30fR-EE
"""
import os

import pytest

from selenium import webdriver
from SeleniumBot.Bot import Action, Bot
from SeleniumBot.session import PipeSession


class CheatSheetBot(Bot):
    def __init__(self, driver=None, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument('--headless')
        super(CheatSheetBot, self).__init__(f'file:///{os.getcwd()}/htmlcheatsheet/index.html', driver, options)

    @PipeSession.action(default_arg='last_value')
    def my_custom(self, arg1=None, default_arg=None):
        arg = arg1 or default_arg
        print(f'{arg}')
        return arg

    @PipeSession.procedural_action()
    def print_session(self):
        elmt = self.find_element("/html/body/form/div[4]/textarea")
        print(self.session.to_dict())


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
    bot.execute(actions)


def test_execute_with_two_actions(bot):
    actions = [Action.Get, (Action.SendKeys, "/html/body/form/div[4]/textarea", "Hello World")]
    bot.execute(actions, actions)


@pytest.mark.parametrize('actions, expected', [
    ('[Action.Get, (Action.Custom, bot.my_custom, "Hello World")]', "Hello World"),
    ('[Action.Get, (Action.Custom, bot.my_custom)]', f'file:///{os.getcwd()}/htmlcheatsheet/index.html'),

])
def test_session_last(bot, actions, expected):
    result = bot.execute(eval(actions))
    assert result == expected


def test_print_session(bot):
    actions = [Action.Get, (Action.Custom, bot.print_session)]
    result = bot.execute(actions)
    assert result == bot.default_url


def test_execute(bot):
    actions = [(Action.Custom, bot.find_element, "/html/body/form/div[4]/textarea")]
    bot.execute(actions)


def test_screen_shot(bot):
    bot.execute([Action.Get, Action.ScreenShot])
