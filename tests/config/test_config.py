from collections import namedtuple

import pytest

from config_injector.config.config import build, config


class DictEq:
    def __eq__(self, other):
        return vars(self) == vars(other)


MockThing0 = namedtuple("MockThing", ["arg1", "arg2", "arg3", "arg4"])


@config(arg1=str, arg2=str, arg3=int, arg4=int)
def factory_1(arg1, arg2, arg3, arg4):
    return MockThing0(arg1, arg2, arg3, arg4)


class EqVarMixin:
    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({vars(self)})"


@config(cats1=int, cats2=str)
class MockThing1(EqVarMixin):
    def __init__(self, cats1, cats2):
        self.cats1 = cats1
        self.cats2 = cats2


@config(dogs1=float, dogs2=str)
class MockThing2(EqVarMixin):
    def __init__(self, dogs1=1000.0, dogs2="2000"):
        self.dogs1 = dogs1
        self.dogs2 = dogs2


@config(pets1=MockThing1, pets2=MockThing2, owner=int)
class MockThing3(EqVarMixin):
    def __init__(self, pets1=None, pets2=None, owner=1):
        self.pets1 = pets1
        self.pets2 = pets2
        self.owner = owner


@config(pets=(MockThing1, MockThing2))
class MockThing4(EqVarMixin):
    def __init__(self, pets):
        self.pets = pets


@pytest.mark.parametrize(
    "f,config,expected",
    [
        (
            factory_1,
            {"arg1": "1", "arg2": 2, "arg3": "3", "arg4": 4},
            MockThing0(arg1="1", arg2="2", arg3=3, arg4=4),
        ),
        (MockThing1, {"cats1": 1, "cats2": 2}, MockThing1(1, "2")),
        (MockThing2, {"dogs1": 1, "dogs2": 2}, MockThing2(1.0, "2")),
        (
            MockThing3,
            {
                "pets1": {"cats1": 1, "cats2": 2},
                "pets2": {"dogs1": 3, "dogs2": 4},
                "owner": 2,
            },
            MockThing3(pets1=MockThing1(1, "2"), pets2=MockThing2(3.0, "4"), owner=2),
        ),
        (
            MockThing4,
            {"pets": {"type": "MockThing1", "cats1": 1, "cats2": 2}},
            MockThing4(MockThing1(1, "2")),
        ),
        (
            MockThing4,
            {"pets": {"type": "MockThing2", "dogs1": 1, "dogs2": 2}},
            MockThing4(MockThing2(1.0, "2")),
        ),
    ],
)
def test_foo(f, config, expected):
    assert expected == build(f, config)
