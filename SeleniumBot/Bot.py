import time

from selenium import webdriver


class Bot:
    def __init__(self, starting_url="", driver=None, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")

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

    # Abstract
    def handle(self, event):
        pass
