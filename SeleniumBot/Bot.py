import time

from os.path import abspath, dirname, join

from selenium import webdriver

from SeleniumBot import Action


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

    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def get(self, url=None):
        if not url:
            url = self.default_url
        self.driver.get(url)

    def find_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def click(self, xpath):
        self.find_by_xpath(xpath).click()

    def send_keys(self, xpath, text):
        self.find_by_xpath(xpath).send_keys(text)

    def screen_shot(self, path):
        self.driver.save_screenshot(path)

    def quit(self):
        self.driver.quit()

    def execute_action(self, action: Action, *args, _wait_time=None, **kwargs):
        assert isinstance(action, Action)
        wait_time = _wait_time or 0.5

        if action == Action.Get:
            self.get(*args, **kwargs)
        elif action == Action.Click:
            self.click(*args, **kwargs)
        elif action == Action.SendKeys:
            self.send_keys(*args, **kwargs)
        elif action == Action.ScreenShot:
            self.screen_shot(*args, **kwargs)
        elif action == Action.Custom:
            if 'callback' in kwargs:
                callback = kwargs.pop('callback')
            else:
                callback = args[0]
                args = args[1:]
            callback(*args, **kwargs)
        elif action == Action.Quit:
            self.quit()
        else:
            return
        time.sleep(wait_time)

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
                self.execute_action(action_type, **options, _wait_time=_wait_time)
            elif type(options) == list:
                self.execute_action(action_type, *options, _wait_time=_wait_time)
            else:
                self.execute_action(action_type, options, _wait_time=_wait_time)

    def handle(self, event):
        pass
