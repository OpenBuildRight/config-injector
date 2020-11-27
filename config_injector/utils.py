from typing import Callable


def get_type(f: Callable):
    return f.__name__
