import os
import re

from typing import Callable
from typing import Dict
from typing import List
from typing import SupportsFloat
from typing import SupportsInt
from typing import Text
from typing import Union

from config_injector.exc import EnvironmentVariableNotFound


def get_type(f: Callable):
    return f.__name__


class EnvFiller:
    def __init__(self):
        """
        Object for filling environment variables in json like python objects
        (e.g. dict, list, str, float, int).
        """
        self.env_var_regex = re.compile("\\${[a-zA-Z_][a-zA-Z0-9_]*}")

    @staticmethod
    def _get_env(m: re.Match) -> Text:
        k = m.group(0).replace("${", "").replace("}", "")
        val = os.getenv(str(k))
        if val is None:
            raise EnvironmentVariableNotFound(
                f"Environment variable {k} not found.", variable_name=k
            )
        return str(val)

    def __call__(
        self, o: Union[Dict, List, Text, SupportsInt, SupportsFloat]
    ) -> Union[Dict, List, Text, SupportsInt, SupportsFloat]:
        if isinstance(o, str):
            return self.env_var_regex.sub(self._get_env, o)
        if hasattr(o, "items"):
            return {k: self(v) for k, v in o.items()}
        if hasattr(o, "__iter__"):
            return [self(v) for v in o]
        return o
