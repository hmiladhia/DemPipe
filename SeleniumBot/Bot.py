import os
import time

from datetime import datetime
from os.path import abspath, dirname, join
from random import random


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from SeleniumBot import SelAction
from DumbPipe import DSession, DPipe


class Bot(DPipe):
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
        self.webdriver_wait = None
        self.default_wait = wait
        self.default_url = default_url
        self.default_by = by or By.XPATH
        super(Bot, self).__init__()

    # Actions
    @DSession.action()
    def find_element(self, locator, by=None):
        return self.webdriver_wait.until(ec.visibility_of_element_located((by or self.default_by, locator)))

    @DSession.action()
    def get(self, url=None):
        url = url or self.default_url
        self.driver.get(url)
        return url

    @DSession.procedural_action()
    def click(self, locator, by=None):
        element = self.webdriver_wait.until(ec.element_to_be_clickable((by or self.default_by, locator)))
        element.click()

    @DSession.procedural_action()
    def send_keys(self, locator, text, by=None):
        self.find_element(locator, by).send_keys(text)

    @DSession.action()
    def screen_shot(self, path=None, file_name=None):
        file_path = join(path or os.getcwd(),
                         file_name or f"screenshot-{datetime.now().strftime('%y%m%d-%H%M%S.%f')}.png")
        self.driver.save_screenshot(file_path)
        return file_path

    @DSession.procedural_action()
    def start(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.webdriver_wait = WebDriverWait(self.driver, self.default_wait)

    @DSession.procedural_action()
    def quit(self):
        self.driver.quit()

    def _execute_action(self, action: SelAction, *args, **kwargs):
        assert isinstance(action, SelAction)
        if action == SelAction.Get:
            return self.get(*args, **kwargs)
        elif action == SelAction.Click:
            return self.click(*args, **kwargs)
        elif action == SelAction.SendKeys:
            return self.send_keys(*args, **kwargs)
        elif action == SelAction.ScreenShot:
            return self.screen_shot(*args, **kwargs)
        else:
            return super(Bot, self)._execute_action(action, *args, **kwargs)
