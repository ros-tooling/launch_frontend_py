# Copyright 2025 Polymath Robotics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch.action import Action
from launch.frontend import expose_action
import pytest


@expose_action('while')
class BuiltinNameTest(Action):
    """Test action that exposes a Python builtin name."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def parse(cls, entity, parser):
        _, kwargs = super().parse(entity, parser)
        return cls, kwargs

    def execute(self, context):
        del context


from launch_py import actions  # noqa: I100, E402


def test_dynamic_attrs():
    name = actions.let.__name__
    assert name == 'let'
    str_repr = str(actions.let)
    assert str_repr.startswith('<function let')

    assert actions.while_.__name__ == 'while_'

    with pytest.raises(AttributeError):
        getattr(actions, 'non_existent_action')

    test_group = actions.group()
    assert test_group.type_name == 'group'

    test_arg = actions.arg(name='argname', default='argvalue')
    assert test_arg.type_name == 'arg'
    assert test_arg.get_attr('name') == 'argname'
    assert test_arg.get_attr('default') == 'argvalue'

    with pytest.raises(AttributeError):
        test_arg.get_attr('non_existent_attr')
