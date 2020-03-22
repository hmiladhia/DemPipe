from collections.abc import MutableMapping


class PipeContext(MutableMapping):
    def __init__(self):
        self._memory = None

    def start(self):
        self._memory = {'last_value': None, 'trigger_value': None}

    def quit(self):
        self._memory = None

    def get_last_value(self):
        return self['last_value']

    def to_dict(self):
        return self._memory or dict()

    def __iter__(self):
        return iter(self._memory)

    def __getitem__(self, item):
        return self._memory[item]

    def __setitem__(self, key, value):
        self._memory[key] = value

    def __len__(self):
        return len(self._memory)

    def __delitem__(self, v) -> None:
        del self._memory[v]
