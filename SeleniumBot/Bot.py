import time
from selenium import webdriver

from SeleniumBot import Action


class Bot:
    def __init__(self, default_url=None, driver=None, options=None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')

        if driver is None:
            from os.path import abspath, dirname, join
            driver = webdriver.Chrome(executable_path=join(dirname(abspath(__file__)), "chromedriver.exe"),
                                      options=options)

        self.driver = driver
        self.default_url = default_url

    def get(self, url=None):
        if not url:
            url = self.default_url
        self.driver.get(url)

    def find_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def click(self, xpath):
        self.find_by_xpath(xpath).click()
        time.sleep(0.5)

    def quit(self):
        self.driver.quit()

    def execute_action(self, action: Action, *args, **kwargs):
        assert type(action) == Action
        wait_time = 0.2

        if action == Action.Get:
            self.get(*args, **kwargs)
            wait_time = 1
        elif action == Action.Click:
            self.click(*args, **kwargs)
        elif action == Action.Quit:
            self.quit()
        else:
            return
        time.sleep(wait_time)

    def execute(self, selenium_actions: list, *args):
        for arg in args:
            selenium_actions.extend(arg)

        for action in selenium_actions:
            action_type = action[0]
            options = action[1]
            if type(options) == dict:
                print(options)
                self.execute_action(action_type, **options)
            elif type(options) == list:
                self.execute_action(action_type, *options)
            else:
                self.execute_action(action_type, options)

    # Abstract
    def handle(self, event):
        pass


if __name__ == "__main__":
    bot = Bot('***REMOVED***')
    # actions = [(Action.Get, {"url": r"https://twitter.com/login?lang=fr"})]
    actions = [(Action.Get, r"***REMOVED***"), (Action.Click, r'//*[@id="u_0_7"]')]
    bot.execute(actions)
    print("Going to quit")
    time.sleep(1)
    bot.quit()
