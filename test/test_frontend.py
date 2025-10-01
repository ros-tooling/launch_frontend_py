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

from pathlib import Path

from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_context import LaunchContext
from launch.launch_description import LaunchDescription

THIS_DIR = Path(__file__).parent


def test_load_basic():
    context = LaunchContext()

    include = IncludeLaunchDescription(str(THIS_DIR / 'launch' / 'basic_launch.py'))
    print(include)
    included_entities = include.get_sub_entities()
    print(included_entities)
    assert len(included_entities) == 1

    launch_desc = included_entities[0]
    assert isinstance(launch_desc, LaunchDescription)

    launchfile_entities = launch_desc.describe_sub_entities()
    assert len(launchfile_entities) == 2

    # The first entity is a declare()
    should_be_declare = launchfile_entities[0]
    assert isinstance(should_be_declare, DeclareLaunchArgument)
    should_be_declare.visit(context)

    # Second is executable()
    should_be_exec = launchfile_entities[1]
    assert isinstance(should_be_exec, ExecuteProcess)

    should_be_exec.prepare(context)
    assert should_be_exec.process_description.final_cmd == ['echo', 'hello world']
