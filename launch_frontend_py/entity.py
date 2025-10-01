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

"""Module for launch_frontend_py Entity class."""
from collections.abc import Iterable
from typing import (
    List,
    Optional,
    Set,
    Text,
    Union,
)

from launch.frontend.entity import Entity as BaseEntity
from launch.frontend.type_utils import check_is_list_entity
from launch.utilities.type_utils import (
    AllowedTypesType,
    AllowedValueType,
    is_instance_of,
)

from .util import is_reserved_identifier


class Entity(BaseEntity):
    """Single item in the intermediate front_end representation."""

    def __init__(
            self,
            type_name: Text,
            *args: BaseEntity,
            **kwargs,
    ) -> None:
        """Create an Entity."""
        if args and kwargs:
            raise ValueError(
                'Entity cannot take both positional arguments and keyword arguments. '
                f'Provided args={args}, kwargs={kwargs}. '
                'To provide attributes & children, pass `children` kwarg with type list[Entity]')

        if kwargs:
            self.__attrs = kwargs
        else:
            children: list[BaseEntity] = []
            for child in args:
                if isinstance(child, Iterable):
                    children.extend(child)
                else:
                    children.append(child)
            self.__attrs = {'children': children}

        self.__type_name = type_name
        self.__read_keys: Set[Text] = set()

    @property
    def type_name(self) -> Text:
        """Get Entity type."""
        return self.__type_name

    @property
    def parent(self) -> Optional['Entity']:
        """Get Entity parent."""
        return None

    @property
    def children(self) -> List[BaseEntity]:
        """Get the Entity's children."""
        if 'children' not in self.__attrs:
            raise ValueError(
                f'Expected entity `{self.__type_name}` to have children entities.')
        self.__read_keys.add('children')

        children: List[BaseEntity] = self.__attrs['children']
        return children

    def assert_entity_completely_parsed(self):
        unparsed_keys = set(self.__attrs.keys()) - self.__read_keys
        if unparsed_keys:
            raise ValueError(
                f'Unexpected key(s) found in `{self.__type_name}`: {unparsed_keys}'
            )

    def get_attr(  # type: ignore[override]
        self,
        name: Text,
        *,
        data_type: AllowedTypesType = str,
        optional: bool = False,
        can_be_str: bool = True,
    ) -> Optional[Union[
        AllowedValueType,
        List['Entity'],
    ]]:
        """
        Access an attribute of the entity.

        See :py:meth:`launch.frontend.Entity.get_attr`.
        Does not apply type coercion, only checks if the read value is of the correct type.
        """
        # Reserved identifiers are all suffixed with an underscore
        if is_reserved_identifier(name):
            name += '_'

        if name not in self.__attrs:
            if not optional:
                raise AttributeError(
                    "Can not find attribute '{}' in Entity '{}'".format(
                        name, self.type_name))
            else:
                return None
        self.__read_keys.add(name)
        data = self.__attrs[name]
        if check_is_list_entity(data_type):
            if isinstance(data, list) and isinstance(data[0], dict):
                return [Entity(name, **child) for child in data]
            elif isinstance(data, list) and isinstance(data[0], Entity):
                return data
            raise TypeError(
                "Attribute '{}' of Entity '{}' expected to be a list of dictionaries.".format(
                    name, self.type_name
                )
            )
        if not is_instance_of(data, data_type, can_be_str=can_be_str):
            raise TypeError(
                "Attribute '{}' of Entity '{}' expected to be of type '{}', got '{}'".format(
                    name, self.type_name, data_type, type(data)
                )
            )
        return data

    def __repr__(self) -> str:
        """Return a string representation of the Entity."""
        return f'Entity(type_name={self.__type_name}, attrs={self.__attrs})'
