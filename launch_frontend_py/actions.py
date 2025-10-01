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

import builtins
import keyword
from typing import Any, Callable

from .entity import Entity

__all__ = []


def is_reserved_identifier(name: str) -> bool:
    """Check if a name is a reserved identifier in Python."""
    return keyword.iskeyword(name) or name in dir(builtins)


def _make_action_factory(action_name: str) -> Callable[..., Any]:
    """Create a factory function that constructs an Entity of the given action type."""
    if is_reserved_identifier(action_name):
        action_name += '_'

    def fn(*args, **kwargs):
        return Entity(action_name, *args, **kwargs)

    fn.__doc__ = f'launch_frontend_py action: {action_name} (dynamically generated)'
    fn.__name__ = action_name
    fn.__qualname__ = action_name
    fn.__module__ = __name__
    globals()[action_name] = fn
    __all__.append(action_name)
    return fn


def _preseed_all_actions() -> None:
    """
    Pre-seed all available actions into this module.

    This is called at module load time, but will not have access to actions from plugin packages
    (such as launch_ros) until they have been imported into the Python process.
    """
    from launch.frontend.expose import action_parse_methods

    for action_name in action_parse_methods.keys():
        _make_action_factory(action_name)


def __getattr__(name: str) -> Any:
    """
    Dynamically create action factory functions on demand.

    This is called when user `from launch_frontend_py.actions import <name>`.
    """
    from launch.frontend.expose import action_parse_methods
    import importlib

    # If it's already been created, return
    if name in __all__:
        return importlib.import_module(f'.{name}', __name__)

    # If not, perhaps it was exposed later or not accessed yet
    base_name = name[:-1] if name.endswith('_') else name
    if base_name in action_parse_methods:
        return _make_action_factory(name)
    else:
        msg = f'module {__name__} has no attribute "{name}"'
        if base_name != name:
            msg += ' (or "{base_name}")'
        raise AttributeError(msg)


_preseed_all_actions()
