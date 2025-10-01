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
from launch.launch_description import LaunchDescription
from launch.launch_service import LaunchService

THIS_DIR = Path(__file__).parent


def test_load_basic():
    include = IncludeLaunchDescription(str(THIS_DIR / 'launch' / 'basic_launch.py'))

    ls = LaunchService()
    ld = LaunchDescription([include])
    ls.include_launch_description(ld)

    ls.context.launch_configurations['condition'] = 'False'
    assert 0 == ls.run()

    included_entities = include.get_sub_entities()
    assert len(included_entities) == 1

    launch_desc = included_entities[0]
    assert isinstance(launch_desc, LaunchDescription)

    launchfile_entities = launch_desc.describe_sub_entities()
    expected_types = (
        DeclareLaunchArgument,
        DeclareLaunchArgument,
        ExecuteProcess,
        ExecuteProcess,
        ExecuteProcess,
    )
    assert len(launchfile_entities) == len(expected_types)
    assert all(isinstance(e, t) for e, t in zip(launchfile_entities, expected_types))

    assert launchfile_entities[2].process_description.final_cmd == ['echo', 'hello world']
    assert launchfile_entities[3].process_description.final_cmd is None
    assert launchfile_entities[4].process_description.final_cmd == [
        'echo', 'hello', 'not-condition']
