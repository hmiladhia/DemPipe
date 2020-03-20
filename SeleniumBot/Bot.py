import os

from datetime import datetime
from os.path import abspath, dirname, join


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from DumbPipe import PipeExecutor


class Bot(PipeExecutor):
    def __init__(self, driver_path=None, options=None, default_url=None, wait=3, by=None,
                 config_file=None):
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
        super(Bot, self).__init__(config_file=config_file)

    # Actions
    def find_element(self, locator, by=None):
        return self.webdriver_wait.until(ec.visibility_of_element_located((by or self.default_by, locator)))

    def inner_text(self, locator, by=None):
        return self.find_element(locator, by).text

    def get(self, url=None):
        url = url or self.default_url
        self.driver.get(url)
        return url

    def click(self, locator, by=None):
        element = self.webdriver_wait.until(ec.element_to_be_clickable((by or self.default_by, locator)))
        element.click()

    def send_keys(self, locator, text, by=None):
        self.find_element(locator, by).send_keys(text)

    def screen_shot(self, path=None, file_name=None):
        file_path = join(path or os.getcwd(),
                         file_name or f"screenshot-{datetime.now().strftime('%y%m%d-%H%M%S.%f')}.png")
        self.driver.save_screenshot(file_path)
        return file_path

    def start(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.webdriver_wait = WebDriverWait(self.driver, self.default_wait)

    def quit(self, exc_type, exc_val, exc_tb):
        super(Bot, self).quit(exc_type, exc_val, exc_tb)
        self.driver.quit()
