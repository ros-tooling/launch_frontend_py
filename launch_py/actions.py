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

from typing import Any, Callable

from launch.frontend.expose import action_parse_methods

from .entity import Entity, is_reserved_identifier

__all__ = []


def make_action_factory(action_name: str, **kwargs) -> Callable[..., Entity]:
    # Create a factory function for each action entity
    def fn(**kwargs):
        return Entity(action_name, kwargs)  # noqa: F821

    # fn = FunctionType(impl_template.__code__, globals(), name=action_name)
    fn.__doc__ = f'launch_py action: {action_name} (dynamically generated)'
    fn.__name__ = action_name
    fn.__qualname__ = action_name
    fn.__module__ = __name__
    return fn


for action_name in action_parse_methods.keys():
    if is_reserved_identifier(action_name):
        action_name += '_'
    fn = make_action_factory(action_name)
    globals()[action_name] = fn
    __all__.append(action_name)


def __getattr__(name: str) -> Any:
    # This is a workaround for mypy complaint about dynamically created attrs
    import importlib
    if name in __all__:
        return importlib.import_module(f'.{name}', __name__)
    raise AttributeError(f'module {__name__} has no attribute {name}')
