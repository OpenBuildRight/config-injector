# config-injector
Config-injector is a very simple framework which aims to do only two things: (1) define configurable functions and (2) inject configuration data into those functions at runtime.

## Installation
Install with pip.
```bash
pip install config-injector
```

## Getting Started
Annotate any callable as a configurable function using `@config`. Note that the `@config` decorator requires that you provide callable functions for each argument. These callable functions should return the expected type. The object is to break all arguments down to fundamental types: string, integer, float or dictionary.

```python
from collections import namedtuple
from typing import Text, Dict, SupportsInt
from pathlib import Path

from config_injector import config, Injector


MockThing0 = namedtuple("MockThing0", ["arg_1", "arg_2", "arg_3", "arg_4"])

@config(arg_1=str, arg_2=str, arg_3=str, arg_4=str)
def mock_thing_0(arg_1: Text, arg_2: Text, arg_3: Text, arg_4: Text):
    return MockThing0(arg_1, arg_2, arg_3, arg_4)


@config(arg_5=int, arg_6=int, arg_7=int, arg_8=int)
def mock_thing_1(arg_5, arg_6, arg_7, arg_8):
    return {"key_a": arg_5, "key_b": arg_6, "key_c": arg_7, "key_d": arg_8}

@config(t0=mock_thing_0, t1=mock_thing_1, arg_9=str)
def mock_things(t0: MockThing0, t1: Dict[SupportsInt], arg_9: Text):
    return (t0, t1, arg_9)

def get_things(config_file=Path("config.json")):
    injector = Injector()
    injector.load_file(config_file)
    return injector["things"].instantiate(mock_things)
```

Now that the configurable functions are annotated, we can write a configuration for them.

```json
{
  "things": {
    "t0": {"arg_1": "a", "arg_2": "b", "arg_3": "c", "arg_4": "d"},
    "t1": {"arg_5": 1, "arg_6": 2, "arg_7": 3, "arg_8": 4},
    "arg_9": "e"
  }
}
```

This configuration file can be loaded in the runtime portion of our implementation using `get_things()` to instantiate the configured objects created by our functions.