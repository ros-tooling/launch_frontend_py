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
from launch_frontend_py import actions
import pytest


@expose_action('while')
class BuiltinNameTest(Action):
    """Test action that exposes a Python builtin name."""

    @classmethod
    def parse(cls, entity, parser):
        _, kwargs = super().parse(entity, parser)
        return cls, kwargs


@expose_action('foo')
class DynamicCreationTest(Action):
    """Test action that exposes an action after first import."""

    @classmethod
    def parse(cls, entity, parser):
        _, kwargs = super().parse(entity, parser)
        return cls, kwargs


def test_dynamic_attrs():
    name = actions.let.__name__
    assert name == 'let'
    str_repr = str(actions.let)
    assert str_repr.startswith('<function let')

    with pytest.raises(AttributeError):
        getattr(actions, 'non_existent_action')

    with pytest.raises(AttributeError):
        _ = actions.other_nonexistent

    test_group = actions.group()
    assert test_group.type_name == 'group'

    test_arg = actions.arg(name='argname', default='argvalue')
    assert test_arg.type_name == 'arg'
    assert test_arg.get_attr('name') == 'argname'
    assert test_arg.get_attr('default') == 'argvalue'

    with pytest.raises(AttributeError):
        test_arg.get_attr('non_existent_attr')


def test_dynamic_create():
    assert actions.foo is not None

    assert actions.foo.__name__ == 'foo'
    assert actions.foo().type_name == 'foo'

    with pytest.raises(AttributeError):
        actions.node


def test_bultin_suffix():
    assert actions.while_.__name__ == 'while_'
    assert actions.while_().type_name == 'while_'
