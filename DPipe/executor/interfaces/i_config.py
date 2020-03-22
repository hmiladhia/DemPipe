from configDmanager import import_config, Config


class IConfig:
    pipe_name: str

    def __init__(self, config_file=None):
        self.__load_config(config_file)

    def __load_config(self, config_file):
        config = self.__import_config(config_file)
        self.load_config(config)
        return config

    def load_config(self, config):
        self.pipe_name = config.pipe_name

    def __import_config(self, config_file):
        if config_file:
            return import_config(config_file)
        else:
            config = Config(dict())
            self.set_default_config(config)
            return config

    def set_default_config(self, config):
        config.pipe_name = None

    def get_title(self, title=None):
        l_title = []
        if self.pipe_name:
            l_title.append(f'[{self.pipe_name}]')
        if title:
            l_title.append(title)
        return ' - '.join(l_title)
