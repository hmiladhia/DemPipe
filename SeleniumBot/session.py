import functools

from collections.abc import MutableMapping


class PipeSession(MutableMapping):
    def __init__(self):
        self._memory = None

    def start(self):
        self._memory = {'last_value': None, 'trigger': False}

    def quit(self):
        self._memory = None

    def get_last_value(self):
        return self['last_value']

    def to_dict(self):
        return self._memory or dict()

    def __call__(self, _action_type, **s_kwargs):
        s_kwargs = {key: self[value] for key, value in s_kwargs.items()}

        def decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                as_helper = kwargs.pop('as_helper', True)
                result = function(*args, **s_kwargs, **kwargs)
                if not as_helper:
                    if _action_type == 'action':
                        self['last_value'] = result
                    elif _action_type == 'trigger':
                        self['trigger'] = result
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
    def __action_template(_action_type, _session_name='session', **s_kwargs):
        def decorator(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                session_decorator = getattr(args[0], _session_name)(_action_type, **s_kwargs)
                func = session_decorator(function)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @classmethod
    def procedural_action(cls, _session_name='session', **s_kwargs):
        return cls.__action_template('proc', _session_name, **s_kwargs)

    @classmethod
    def action(cls, _session_name='session', **s_kwargs):
        return cls.__action_template('action', _session_name, **s_kwargs)

    @classmethod
    def trigger(cls, _session_name='session', **s_kwargs):
        return cls.__action_template('trigger', _session_name, **s_kwargs)
