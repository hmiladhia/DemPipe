from os.path import abspath, dirname, join
from random import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from SeleniumBot import Action
from SeleniumBot.session import PipeSession


class Bot:
    def __init__(self, default_url=None, driver_path=None, options=None, wait=3):
        if options is None:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--incognito")
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
        else:
            self.options = options
        self.driver_path = driver_path or join(dirname(abspath(__file__)), 'chromedriver.exe')
        self.driver = None
        self.default_wait = wait
        self.default_url = default_url
        self.session = PipeSession()

    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.wait = WebDriverWait(self.driver, self.default_wait)
        self.session.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        self.session.quit()

    def find_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    # Actions

    @PipeSession.action()
    def get(self, url=None):
        url = url or self.default_url
        self.driver.get(url)
        return url

    @PipeSession.procedural_action()
    def click(self, xpath, by=None):
        if by is None:
            by = By.XPATH
        element = self.wait.until(EC.element_to_be_clickable((by, xpath)))
        element.click()

    @PipeSession.procedural_action()
    def send_keys(self, xpath, text):
        self.find_by_xpath(xpath).send_keys(text)

    @PipeSession.action()
    def screen_shot(self, path):
        self.driver.save_screenshot(path)
        return path

    @PipeSession.procedural_action()
    def wait(self, time=None):
        time.sleep(time or random())

    @PipeSession.procedural_action()
    def quit(self):
        self.driver.quit()

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
        return self.session.get_last_value()

    def handle(self, event):
        pass
