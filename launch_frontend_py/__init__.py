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

from typing import Any, Callable, List

from launch.frontend.parser import Parser
from launch.launch_description import LaunchDescription

from .entity import Entity, make_valid_name

__all__ = [
    'launch',
]


def launch(actions: List[Entity]) -> LaunchDescription:
    """Entrypoint of the launchfile, produces a LaunchDescription containing the listed entities."""
    parser = Parser()
    root_entity = Entity('launch', children=actions)
    return parser.parse_description(root_entity)


def __make_action_factory(action_name: str) -> Callable[..., Any]:
    """Create a factory function that constructs an Entity of the given action type."""
    action_name = make_valid_name(action_name)

    def fn(*args, **kwargs):
        return Entity(action_name, *args, **kwargs)

    fn.__doc__ = f'launch_frontend_py action: {action_name} (dynamically generated)'
    fn.__name__ = action_name
    fn.__qualname__ = action_name
    fn.__module__ = __name__
    globals()[action_name] = fn
    __all__.append(action_name)
    return fn


def __getattr__(name: str) -> Any:
    """
    Dynamically create action factory functions on demand.

    This is called in `from actions import <name>`, `getattr(actions, <name>)`, or `actions.<name>`
    """
    import importlib
    from launch.frontend import Parser
    from launch.frontend.expose import action_parse_methods

    if name in __all__:
        # It's already been loaded, just return it
        return importlib.import_module(f'.{name}', __name__)

    # Not loaded here yet, perhaps in an extension that wasn't imported yet
    Parser.load_launch_extensions()

    if name in action_parse_methods:
        return __make_action_factory(name)
    elif name.endswith('_'):
        # The name has a trailing underscore, which we add to actions with reserved Python names
        # Try again without the underscore
        __getattr__(name[:-1])
    else:
        # It's not registered, raise the usual error
        msg = f'module {__name__} has no attribute "{name}"'
        if base_name != name:
            msg += ' (or "{base_name}")'
        raise AttributeError(msg)


def __preseed_all_actions() -> None:
    """
    Pre-seed all available actions into this module.

    This preloads all launch extensions and fills __all__ with available actions.

    This is not necessary, since __getattr__ loads actions on demand,
    but it allows tools and users to see all available actions in __all__.
    """
    from launch.frontend.expose import action_parse_methods
    from launch.frontend import Parser
    Parser.load_launch_extensions()

    action_names = list(action_parse_methods.keys())
    for action_name in action_names:
        __getattr__(action_name)

__preseed_all_actions()
