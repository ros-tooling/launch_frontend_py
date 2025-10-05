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

from launch_frontend_py import arg, executable, launch


def generate_launch_description():
    return launch([
        arg(name='message', default='hello world'),
        arg(name='condition', default='True'),
        executable(cmd='echo $(var message)', output='both'),
        executable(cmd='echo hello conditional', if_='$(var condition)', output='both'),
        executable(cmd='echo hello not-condition', if_='$(not $(var condition))', output='both'),
    ])
