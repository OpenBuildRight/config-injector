try:
    from importlib.metadata import version as get_version
except ImportError:
    from importlib_metadata import version as get_version

from config_injector.config import config
from config_injector.injector import Injector


__version__ = get_version(__package__)
