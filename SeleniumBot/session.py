import functools

from collections.abc import MutableMapping


class SeleniumSession(MutableMapping):
    def __init__(self):
        self._memory = None

    def start(self):
        self._memory = {'_': None}

    def quit(self):
        self._memory = None

    def to_dict(self):
        return self._memory or dict()

    def __call__(self, **s_kwargs):
        s_kwargs = {key: self[value] for key, value in s_kwargs.items()}

        def decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                try:
                    result = function(*args, _last=self['_'], **s_kwargs, **kwargs)
                except TypeError as e:
                    if '_last' in str(e):
                        result = function(*args, **s_kwargs, **kwargs)
                    else:
                        raise e
                self['_'] = result
                return result
            return wrapper
        return decorator

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

    @staticmethod
    def session_context(_session_name='session', **s_kwargs):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                session_decorator = getattr(args[0], _session_name)(**s_kwargs)
                func = session_decorator(function)
                return func(*args, **kwargs)
            return wrapper
        return decorator
