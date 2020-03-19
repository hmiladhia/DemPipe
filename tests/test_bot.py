"""
Credits : htmlcheatsheet was taken from Traversy Media tutorial that you can find at the following link :
    https://www.youtube.com/watch?v=UB1O30fR-EE
"""
import os
import pickle

import imagehash
import pytest

from selenium import webdriver
from PIL import Image


from SeleniumBot import Bot, Action


class CheatSheetBot(Bot):
    def __init__(self, driver=None, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument('--headless')
        super(CheatSheetBot, self).__init__(driver, options,
                                            default_url=f'file:///{os.getcwd()}/htmlcheatsheet/index.html')


@pytest.fixture(scope='session', autouse=True)
def bot():
    with CheatSheetBot() as bot:
        yield bot


def test_bot_fire_up(bot):
    actions = [bot.get,
               (bot.inner_text, [r'//*[@id="head-one"]'])]
    assert bot.execute(actions) == 'Heading One'


def test_click(bot):
    actions = [bot.get,
               (bot.click, [r'//*[@id="blog-link"]']),
               (bot.inner_text, [r'/html/body/header/h1'])]
    assert bot.execute(actions) == 'My Website'


def test_send_keys(bot):
    actions = [bot.get,
               (bot.send_keys, [r"/html/body/form/div[4]/textarea", "Hello World"]),
               (bot.click, [r'//*[@id="ok-button"]']),
               (bot.inner_text, [r'//*[@id="result"]'])]
    assert bot.execute(actions) == 'Hello World'


def test_screen_shot(bot):
    actions = [bot.get,
               (bot.click, [r'//*[@id="blog-link"]']),
               Action(bot.screen_shot, 'imgs')]
    with open('ref.pickle', 'rb') as file:
        assert pickle.load(file) == imagehash.average_hash(Image.open(bot.execute(actions)))
