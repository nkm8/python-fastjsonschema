import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(current_dir, os.pardir))


from pprint import pprint

import pytest

from fastjsonschema import JsonSchemaException, compile
from fastjsonschema.draft04 import CodeGeneratorDraft04


@pytest.fixture
def asserter():
    def f(definition, value, expected):
        # When test fails, it will show up code.
        code_generator = CodeGeneratorDraft04(definition)
        print(code_generator.func_code)
        pprint(code_generator.global_state)

        validator = compile(definition, version=4)
        if isinstance(expected, JsonSchemaException):
            with pytest.raises(JsonSchemaException) as exc:
                validator(value)
            assert exc.value.message == expected.message
        else:
            assert validator(value) == expected
    return f
