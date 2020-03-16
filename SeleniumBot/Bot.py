import os
import time

from datetime import datetime
from os.path import abspath, dirname, join
from random import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from SeleniumBot import Action
from SeleniumBot.session import PipeSession


class Bot:
    def __init__(self, default_url=None, driver_path=None, options=None, wait=3, by=None):
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
        self.default_by = by or By.XPATH
        self.session = PipeSession()

    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.webdriver_wait = WebDriverWait(self.driver, self.default_wait)
        self.session.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
        self.session.quit()

    @PipeSession.action()
    def find_element(self, locator, by=None):
        return self.webdriver_wait.until(EC.visibility_of_element_located((by or self.default_by, locator)))

    # Actions

    @PipeSession.action()
    def get(self, url=None):
        url = url or self.default_url
        self.driver.get(url)
        return url

    @PipeSession.procedural_action()
    def click(self, locator, by=None):
        element = self.webdriver_wait.until(EC.element_to_be_clickable((by or self.default_by, locator)))
        element.click()

    @PipeSession.procedural_action()
    def send_keys(self, locator, text, by=None):
        self.find_element(locator, by).send_keys(text)

    @PipeSession.action()
    def screen_shot(self, path=None, file_name=None):
        file_path = join(path or os.getcwd(), file_name or f"screenshot-{datetime.now()}.png")
        self.driver.save_screenshot(file_path)
        return file_path

    @PipeSession.procedural_action()
    def wait(self, wait_time=None):
        time.sleep(wait_time or random())

    @PipeSession.procedural_action()
    def quit(self):
        self.driver.quit()

    def execute_action(self, action: Action, *args, **kwargs):
        try:
            try:
                return self._execute_action(action, *args, as_helper=False, **kwargs)
            except TypeError as e:
                if str(e).endswith("got an unexpected keyword argument 'as_helper'"):
                    return self._execute_action(action, *args, **kwargs)
                else:
                    raise e
        except Exception as e:
            self.handle(e)

    def _execute_action(self, action: Action, *args, **kwargs):
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

    def handle(self, exception):
        raise exception
