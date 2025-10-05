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

from launch_frontend_py import group, log
import pytest


def test_kwarg_children():
    g = group(
        namespace='something',
        children=[
            log(level='info', message='list child'),
        ]
    )
    assert len(g.children) == 1
    assert g.get_attr('namespace') == 'something'


def test_list_children():
    g = group([
        log(level='info', message='list child'),
        log(level='info', message='list child 2')
    ])
    assert len(g.children) == 2


def test_positional_children():
    g = group(
        log(level='info', message='positional child'),
        log(level='info', message='positional child 2'),
        log(level='info', message='positional child 3'),
    )
    assert len(g.children) == 3


def test_positional_lists():
    g = group(
        [
            log(level='info', message='positional list 1 child 1'),
            log(level='info', message='positional list 1 child 2'),
        ],
        [
            log(level='info', message='positional list 2 child 1'),
        ]
    )
    assert len(g.children) == 3


def test_bad_arg_combo():
    with pytest.raises(ValueError):
        g = group(
            log(level='info', message='positional child'),
            condition='Something'
        )
        assert g
