import os

import pytest

from config_injector.exc import EnvironmentVariableNotFound
from config_injector.utils import EnvFiller


@pytest.fixture()
def test_env_context():
    os.environ["FOO"] = "foo"
    os.environ["TOFU"] = "tofu"
    os.environ["KUNG_FU"] = "kung fu"
    os.environ["mu"] = "μ"


@pytest.mark.parametrize(
    "object,expected",
    [
        ("${FOO} bar", "foo bar"),
        ("abc def", "abc def"),
        ("$abc {def}", "$abc {def}"),
        ("${abc def}", "${abc def}"),
        ("${mu}", "μ"),
        (
            [["abc${FOO}def", "I like ${TOFU}"], {"${KUNG_FU}": "${KUNG_FU}"}],
            [["abcfoodef", "I like tofu"], {"${KUNG_FU}": "kung fu"}],
        ),
        (
            {"a": 1, "b": 1.1, "c": ["${FOO}"], 10: "ten"},
            {"a": 1, "b": 1.1, "c": ["foo"], 10: "ten"},
        ),
    ],
)
def test_env_filler(object, expected, test_env_context):
    env_filler = EnvFiller()
    assert env_filler(object) == expected


def test_env_filler_raises_env_variable_not_found():
    env_filler = EnvFiller()
    with pytest.raises(EnvironmentVariableNotFound):
        env_filler("${NOT_A_VAR}")
