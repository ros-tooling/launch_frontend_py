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

from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, Log
from launch.utilities import perform_substitutions

THIS_DIR = Path(__file__).parent


def test_load_basic():
    context = LaunchContext()

    include = IncludeLaunchDescription(THIS_DIR / 'launch' / 'basic_launch.py')
    included_entities = include.get_sub_entities()
    launch_desc = included_entities[0]
    assert isinstance(launch_desc, LaunchDescription)

    launchfile_entities = launch_desc.describe_sub_entities()
    assert len(launchfile_entities) == 2

    should_be_declare = launchfile_entities[0]
    should_be_log = launchfile_entities[1]

    assert isinstance(should_be_declare, DeclareLaunchArgument)
    should_be_declare.visit(context)

    assert isinstance(should_be_log, Log)
    should_be_log.visit(context)

    msg = perform_substitutions(context, should_be_log.msg)
    assert msg == 'I am a launch file: foo=bar'
