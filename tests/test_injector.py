from collections import namedtuple
from typing import Text

import pytest

from config_injector import Injector
from config_injector import config


MockThing0 = namedtuple("MockThing0", ["arg_1", "arg_2", "arg_3", "arg_4"])
MockThing1 = namedtuple("MockThing1", ["arg_5", "arg_6", "arg_7", "arg_8"])


@config(arg_1=str, arg_2=str, arg_3=str, arg_4=str)
def mock_thing_0(arg_1: Text, arg_2: Text, arg_3: Text, arg_4: Text):
    return MockThing0(arg_1, arg_2, arg_3, arg_4)


@config(arg_5=int, arg_6=int, arg_7=int, arg_8=int)
def mock_thing_1(arg_5, arg_6, arg_7, arg_8):
    return MockThing1(arg_5, arg_6, arg_7, arg_8)


@config(t0=mock_thing_0, t1=mock_thing_1, arg_9=str)
def mock_things(t0: MockThing0, t1: MockThing1, arg_9: Text):
    return (t0, t1, arg_9)


@pytest.fixture()
def context():
    return {
        "things": {
            "t0": {"arg_1": "a", "arg_2": "b", "arg_3": "c", "arg_4": "d"},
            "t1": {"arg_5": 1, "arg_6": 2, "arg_7": 3, "arg_8": 4},
            "arg_9": "e",
        }
    }


@pytest.fixture()
def injector(context):
    return Injector(context)


def test_injector_inject(injector):
    thing_1: MockThing1 = injector["things"]["t1"].instantiate(mock_thing_1)
    assert injector["things"]["t1"]["arg_5"] == thing_1.arg_5
    assert injector["things"]["t1"]["arg_6"] == thing_1.arg_6


def test_injector_inject_nested(injector):
    things = injector["things"].instantiate(mock_things)
    assert isinstance(things[0], MockThing0)
    assert isinstance(things[1], MockThing1)
    assert injector["things"]["t0"]["arg_1"] == things[0].arg_1
    assert injector["things"]["t1"]["arg_5"] == things[1].arg_5
    assert injector["things"]["arg_9"] == things[2]
