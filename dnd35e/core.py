#  MIT License
#
#  Copyright (c) 2019 Anthony Harrison
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

"""Low-level, core functionality for DayDream3.5"""

__all__ = ['DayDreamError', 'Aggregator']

from copy import copy
from functools import reduce
from operator import add
from typing import Any, AbstractSet, Set, Optional
from dataclasses import dataclass


class DayDreamError(Exception):
    """Error for errors raised by module."""


@dataclass(frozen=True)
class Condition:
    """A specific situation to which some kind of bonus applies.

    For example, in the SRD "[a specialist wizard] gains a +2 bonus on
    Spellcraft checks to learn the spells of her chosen school." The
    condition text here would be "to learn the spells of her chosen
    school" which gives the limited conditions in which the bonus
    applies.
    """

    text: str

    def __str__(self) -> str:
        return self.text


def _is_private(name: str) -> bool:
    """Return true if the name is private.

    :param name: name of an attribute
    """
    return name.startswith('_')


def _is_public(name: str) -> bool:
    """Return true if the name is not private, i.e. is public.

    :param name: name of an attribute
    """
    return not name.startswith('_')


class Aggregator:
    """Aggregate values from all objects attached to an instance.

    This overrides attribute look up and allows combining (through
    addition) values defined both on a particular instance and on its
    attributes. This is used to allow multiple different sources to
    modify a value.

    For example, a character's strength is partially inherent and is
    possibly modified by their race and levels in particular classes.
    This class defines the interface by which all of these can be made
    aware of each other with minimal boilerplate. To manage this, a
    character will be an aggregator and have its own `strength`
    attribute (i.e. the inherent part of its strength) and will add to
    this value any attribute that also defines a `strength` attribute.
    In this way, a class and a race that both define `strength` will
    be added to the strength present on the character yielding a total
    for that ability score.
    """

    def __init_subclass__(cls,
                          ignore: Optional[AbstractSet[str]] = None) -> None:
        """Setup attributes to access directly."""
        super().__init_subclass__()

        if ignore is None:
            cls._ignore = set()
        else:
            cls._ignore = set(ignore)

        cls._instance_names = {k for k, v in vars(cls).items()
                               if isinstance(v, property)}

    def __init__(self) -> None:
        """Initialize attribute name tracker."""
        super().__init__()
        self._instance_names: Set[str] = copy(self._instance_names)

    def __setattr__(self, name: str, value: Any) -> None:
        """Track any attributes that are added to an instance."""
        if _is_public(name) and name not in self._known_names:
            self._instance_names.add(name)
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Aggregate value from each attribute if allowed."""
        if _is_private(name) or name in super().__getattribute__('_ignore'):
            result = super().__getattribute__(name)
        else:
            values = []

            try:
                values.append(super().__getattribute__(name))
            except AttributeError:
                pass

            for name_other in super().__getattribute__('_instance_names'):
                if name_other != name:
                    attribute = super().__getattribute__(name_other)
                    if hasattr(attribute, name):
                        values.append(getattr(attribute, name))

            if values:
                result = reduce(add, values)
            else:
                raise AttributeError(f'The desired attribute {name} could not'
                                     f' be found')
        return result

    def __delattr__(self, name: str) -> None:
        """Remove deleted attributes from tracker."""
        super().__delattr__(name)
        self._instance_names.remove(name)

    @property
    def _known_names(self) -> Set[str]:
        """Return all known names."""
        return self._ignore | self._instance_names
