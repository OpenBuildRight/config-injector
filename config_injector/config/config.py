from abc import ABC
from typing import (Any, Callable, Dict, List, SupportsFloat, SupportsInt,
                    Text, Tuple, Union)

from config_injector.config.exc import (DoesNotSupportBuild,
                                        InvalidConfigValue, KeyNotInConfig,
                                        TypeNotDefined)
from config_injector.config.utils import get_type

JsonTypes = Union[Dict, List, bool, SupportsInt, SupportsFloat, Text]
ComponentCallable = Union[Any, Tuple[Any]]


class SupportsBuild(ABC):
    def __build__(self, **kwargs: Dict):
        ...


def build(f: SupportsBuild, config: Dict) -> Any:
    try:
        return f.__build__(**config)
    except AttributeError as e:
        if not hasattr(f, "__build__"):
            raise DoesNotSupportBuild(f"{f} does not support build.", e)
        else:
            raise e


class Config(SupportsBuild):
    def __init__(self, callback: Callable, **arg_callables: ComponentCallable):
        """
        A configurable component containing hints for json parsing.

        :param callback: The function to call. The function should return an object.
        :param arg_callables: The callables for the arguments to the callback with matching
           argument names. These callables can be overloaded by providing a tuple.
        """
        self.callback = callback
        self.arg_callables = arg_callables

    def __call__(self, *args, **kwargs) -> Any:
        return self.callback(*args, **kwargs)

    @property
    def __name__(self):
        if hasattr(self.callback, "__name__"):
            return self.callback.__name__
        else:
            raise AttributeError(f"{self.callback} has no attribute {__name__}")

    def get_arg_type(self, arg_name, arg):
        _arg_tp = self.arg_callables[arg_name]
        try:
            type_map = {get_type(x): x for x in _arg_tp}
        except TypeError:
            type_map = None
        if type_map:
            # Handle "oneOf" types defined with a type property.
            try:
                type_name = arg.pop("type")
            except KeyError:
                raise KeyNotInConfig(
                    f"Config key type not found in configuration arguments for {arg_name}"
                )
            except TypeError:
                raise InvalidConfigValue(f"Config value for {arg_name} is invalid.")
            try:
                arg_tp = type_map[type_name]
            except KeyError:
                raise TypeNotDefined(
                    f"Configuration type {type_name} not defined for {arg_name}"
                )
        else:
            arg_tp = _arg_tp
        return arg_tp

    def __build__(self, **kwargs: JsonTypes) -> Any:
        """
        Cast data from parsed json prior to calling the callback.

        :param kwargs: Key word arguments consisting of only json types.
        :return:
        """
        kwargs_cast = {}
        for arg_name, arg in kwargs.items():
            arg_tp = self.get_arg_type(arg_name, arg)
            if arg_name in self.arg_callables:
                if hasattr(arg, "items") and hasattr(arg_tp, "__build__"):
                    arg_cast = build(arg_tp, arg)
                else:
                    arg_cast = arg_tp(arg)
            else:
                arg_cast = arg
            kwargs_cast[arg_name] = arg_cast
        return self(**kwargs_cast)


def config(**arg_callables: ComponentCallable) -> Callable[[], Config]:
    """
    Decorator for functions with hints for json decoding.

    :param key: The key to use for the configuration.
    :param kwargs: The type for each argument in the function f.
    :return:
    """

    def wrapper(f) -> Config:
        _key = get_type(f)
        component = Config(f, **arg_callables)
        return component

    return wrapper
