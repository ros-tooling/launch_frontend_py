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

from launch_frontend_py import launch
from launch_frontend_py.actions import arg, log


def generate_launch_description():
    return launch([
        arg(name='foo'),
        log(
            level='INFO',
            message='I am an included launch file: foo=$(var foo)',
        ),
        # TODO(emerson) make if_ work
        # log(
        #     if_='$(var foo)',
        #     level='INFO',
        #     message='This conditional log only happened because foo is true',
        # ),
        # log(
        #     if_='$(not $(var foo))',
        #     level='INFO',
        #     message='This conditional log only happened because foo is false',
        # ),
    ])
