from os.path import abspath, dirname, join
from random import random

from selenium import webdriver

from SeleniumBot import Action
from SeleniumBot.session import SeleniumSession


class Bot:
    def __init__(self, default_url=None, driver_path=None, options=None):
        if options is None:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--incognito")
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
        else:
            self.options = options
        self.driver_path = driver_path or join(dirname(abspath(__file__)), 'chromedriver.exe')
        self.driver = None
        self.default_url = default_url
        self.session = SeleniumSession()

    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.session.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        self.session.quit()

    @SeleniumSession.session_context()
    def get(self, url=None):
        url = url or self.default_url
        self.driver.get(url)
        return url

    @SeleniumSession.session_context()
    def find_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    @SeleniumSession.session_context()
    def click(self, xpath, _last=None):
        self.find_by_xpath(xpath).click()
        return _last

    @SeleniumSession.session_context()
    def send_keys(self, xpath, text, _last=None):
        self.find_by_xpath(xpath).send_keys(text)
        return None

    @SeleniumSession.session_context()
    def screen_shot(self, path):
        self.driver.save_screenshot(path)
        return path

    @SeleniumSession.session_context()
    def wait(self, time=None, _last=None):
        time.sleep(time or random())
        return _last

    @SeleniumSession.session_context()
    def quit(self):
        return self.driver.quit()

    def execute_action(self, action: Action, *args, **kwargs):
        assert isinstance(action, Action)

        if action == Action.Get:
            return self.get(*args, **kwargs)
        elif action == Action.Click:
            return self.click(*args, **kwargs)
        elif action == Action.SendKeys:
            return self.send_keys(*args, **kwargs)
        elif action == Action.ScreenShot:
            return self.screen_shot(*args, **kwargs)
        elif action == Action.Wait:
            return self.wait(*args, **kwargs)
        elif action == Action.Custom:
            if 'callback' in kwargs:
                callback = kwargs.pop('callback')
            else:
                callback = args[0]
                args = args[1:]
            return callback(*args, **kwargs)
        elif action == Action.Quit:
            return self.quit()
        else:
            return

    def execute(self, *args, _wait_time=None):
        selenium_actions = []
        for arg in args:
            if not isinstance(arg, tuple) and hasattr(arg, '__iter__'):
                selenium_actions.extend(arg)
            else:
                selenium_actions.append(arg)

        for action in selenium_actions:
            options = []
            if type(action) == Action:
                action_type = action
            elif hasattr(action, '__len__') and len(action) == 2:
                action_type = action[0]
                options = action[1]
            elif hasattr(action, '__len__') and len(action) > 0:
                action_type = action[0]
                options = list(action[1:])
            else:
                raise ValueError("Action doesn't fit any format")

            if type(options) == dict:
                self.execute_action(action_type, **options)
            elif type(options) == list:
                self.execute_action(action_type, *options)
            else:
                self.execute_action(action_type, options)
        return self.session['_']

    def handle(self, event):
        pass
