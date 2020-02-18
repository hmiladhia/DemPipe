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

    def send_keys(self, xpath, text):
        self.find_by_xpath(xpath).send_keys(text)
        time.sleep(0.5)

    def quit(self):
        self.driver.quit()

    def execute_action(self, action: Action, *args, **kwargs):
        assert isinstance(action, Action)
        wait_time = 0.5

        if action == Action.Get:
            self.get(*args, **kwargs)
            wait_time = 1
        elif action == Action.Click:
            self.click(*args, **kwargs)
        elif action == Action.SendKeys:
            self.send_keys(*args, **kwargs)
        elif action == Action.Quit:
            self.quit()
        else:
            return
        time.sleep(wait_time)

    def execute(self, *args):
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
    bot = Bot(r'***REMOVED***')
    try:
        actions = [(Action.Get, r"***REMOVED***"),
                   (Action.Click, r'//*[@id="u_0_7"]'),
                   (Action.SendKeys, [r'//*[@id="email"]', "test@gmail.com"]),
                   (Action.SendKeys, r'//*[@id="pass"]', "mypassword")]
        bot.execute(actions)
    finally:
        time.sleep(3)
        bot.execute(Action.Quit)
