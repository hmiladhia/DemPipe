import time
from selenium import webdriver

from SeleniumBot import Action


class Bot:
    def __init__(self, starting_url="", driver=None, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')

        if driver is None:
            driver = webdriver.Chrome(options=options)

        self.driver = driver
        self.starting_url = starting_url

    def get(self, url=None):
        if not url:
            url = self.starting_url
        self.driver.get(url)

    def find_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def click(self, xpath):
        self.find_by_xpath(xpath).click()
        time.sleep(0.5)

    def execute_action(self, action, **kwargs):
        assert type(action) == Action
        wait_time = 0.2

        if action == Action.Get:
            self.get(kwargs.get('url'))
            wait_time = 1
        elif action == Action.Click:
            self.click(kwargs['xpath'])
        else:
            return
        time.sleep(wait_time)

    # Abstract
    def handle(self, event):
        pass


if __name__ == "__main__":
    bot = Bot('***REMOVED***')
    bot.execute_action(Action.Get, url=None)