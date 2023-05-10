from urllib.parse import unquote
from datetime import datetime
from time import perf_counter

from config.urls import url_patterns


def parse_request_params(params):
    data = {}
    if params:
        for param in unquote(params).split("&"):
            key, value = param.split("=")
            data[key] = value
    return data


class BaseLogger(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=BaseLogger):
    def __init__(self, name):
        self.name = name

    def log(self, message):
        with open(f"./var/log/{self.name}.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] : {message}\n")


def route(path):
    def wrapper(cls):
        def _wrapper(*args, **kwargs):
            return url_patterns[path](*args, **kwargs)

        view = url_patterns.get(path)
        if not view:
            url_patterns[path] = cls()

        return _wrapper

    return wrapper


def debug(func):
    def timed(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter() - start
        print(f"debug -> {func.__qualname__} done {end:2.2f} ms")
        return result

    return timed


if __name__ == "__main__":
    print(parse_request_params("key=value&spam=eggs"))
    print(parse_request_params(""))
