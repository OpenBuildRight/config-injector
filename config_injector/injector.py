import json

from collections.abc import MutableMapping
from pathlib import Path
from typing import Dict
from typing import Text

import toml
import yaml

from config_injector.config import SupportsFill
from config_injector.config import fill
from config_injector.exc import FileTypeNotRecognized
from config_injector.utils import EnvFiller


class Injector(MutableMapping):
    def __init__(self, context: Dict = None, fill_env=True):
        self.context = {}
        self.fill_env = fill_env
        self._env_filler = EnvFiller()
        self.load(context)

    def __getitem__(self, k: Text):
        v = self.context[k]
        if hasattr(v, "items"):
            return self.__class__(v)
        else:
            return v

    def __iter__(self):
        return iter(self.context)

    def __setitem__(self, k, v):
        self.context[k] = v

    def __delitem__(self, k):
        self.context.pop(k)

    def __len__(self):
        return len(self.context)

    def clear(self):
        self.context = {}

    def load(self, context: Dict):
        _context = self._env_filler(context)
        self.context.update(_context)

    def load_file(self, file: Path):
        if file.name.lower().endswith(".json"):
            self._load_json_file(file)
        elif file.name.lower().endswith(".toml"):
            self._load_toml_file(file)
        elif file.name.lower().endswith(".yaml") or file.name.lower().endswith(".yml"):
            self._load_yaml_file(file)
        else:
            raise FileTypeNotRecognized(
                f"Unable to determine file type for {file.name}"
            )

    def _load_json_file(self, file: Path):
        with file.open() as f:
            self.load(json.load(f))

    def _load_toml_file(self, file: Path):
        with file.open() as f:
            self.load(toml.load(f))

    def _load_yaml_file(self, file: Path):
        with file.open() as f:
            self.load(yaml.load(f, Loader=yaml.SafeLoader))

    def instantiate(self, config: SupportsFill):
        return fill(config, self.context)
