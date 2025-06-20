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

from launch_frontend_py import launch
from launch_frontend_py.actions import arg, executable, group, include, let, log, set_env

THIS_DIR = Path(__file__).parent


def generate_launch_description():
    return launch([
        arg(name='arg1', default='arg1_value'),
        let(name='arg2', value='let_$(var arg1)'),
        executable(
            cmd='echo hello launch_frontend_py executable',
            output='screen',
        ),
        log(level='INFO', message='Log warning: arg1=$(var arg1), arg2=$(var arg2)'),
        group(
            children=[
                set_env(
                    name='MY_ENV_VAR',
                    value='my_value',
                ),
                log(level='WARNING', message='In group env MY_ENV_VAR=$(env MY_ENV_VAR)'),
            ]
        ),
        log(level='ERROR', message='Outside group: env MY_ENV_VAR=$(env MY_ENV_VAR "<unset>")'),
        include(
            file=f'{THIS_DIR}/include_launch.py',
            arg=[
                arg(name='foo', value='True'),
            ],
        ),
    ])
