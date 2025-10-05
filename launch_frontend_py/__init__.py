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

from typing import Any, List

from launch.frontend.parser import Parser
from launch.launch_description import LaunchDescription

from . import actions
from .entity import Entity


def launch(actions: List[Entity]) -> LaunchDescription:
    parser = Parser()
    root_entity = Entity('launch', children=actions)
    return parser.parse_description(root_entity)


def __getattr__(name: str) -> Any:
    """Forward attribute access to the dynamic actions module."""
    import importlib

    if name in __all__:
        return importlib.import_module(f'.{name}', __name__)

    return getattr(actions, name)


__all__ = [
    'launch',
]
