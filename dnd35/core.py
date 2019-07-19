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

__all__ = ['DayDreamError', 'Aggregator', 'ordinal']

from copy import copy
from functools import reduce
from operator import add
from typing import Any, AbstractSet, Set, Optional, overload


class DayDreamError(Exception):
    """Error for errors raised by module."""


class Aggregator:
    """Aggregate values from all objects attached to an instance."""

    def __init_subclass__(cls, ignore: Optional[AbstractSet[str]] = None) -> None:
        """Setup attributes to access directly."""
        super().__init_subclass__()

        if ignore is None:
            ignore = set()

        cls._ignore = ignore
        cls._instance_names = [k for k, v in vars(cls).items() if isinstance(v, property)]

    def __init__(self) -> None:
        """Initialize attribute name tracker."""
        super().__init__()
        self._instance_names = copy(self._instance_names)

    def __setattr__(self, name: str, value: Any) -> None:
        """Track any attributes that are added to an instance."""
        if not name.startswith('_') and name not in self._known_names:
            self._instance_names.append(name)
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Aggregate value from each attribute if allowed."""
        if name.startswith('_') or name in super().__getattribute__('_ignore'):
            result = super().__getattribute__(name)
        else:
            values = []

            try:
                val = super().__getattribute__(name)
            except AttributeError:
                pass
            else:
                values.append(val)

            for other_name in super().__getattribute__('_instance_names'):
                if other_name != name:
                    attribute = super().__getattribute__(other_name)
                    try:
                        val = getattr(attribute, name)
                    except AttributeError:
                        pass
                    else:
                        values.append(val)

            if values:
                result = reduce(add, values)
            else:
                raise AttributeError
        return result

    def __delattr__(self, name: str) -> None:
        """Remove deleted attributes from tracker."""
        super().__delattr__(name)
        i = super().__getattribute__('_instance_names').index(name)
        del super().__getattribute__('_instance_names')[i]

    @property
    def _known_names(self) -> Set[str]:
        return set(self._ignore | set(self._instance_names))


_ORDINALS = ('zeroth', 'first', 'second', 'third', 'fourth', 'fifth',
             'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh',
             'twelfth', 'thirteenth', 'fourteenth', 'sixteenth',
             'eighteenth', 'nineteenth', 'twentieth')


def _integer_to_ordinal(value: int) -> str:
    if value < 0:
        raise ValueError('Cannot convert a negative number to an ordinal')

    try:
        return _ORDINALS[value]
    except IndexError:
        raise NotImplementedError('Cannot convert a number greater than twenty'
                                  ' to an ordinal') from None


def _ordinal_to_integer(value: str) -> int:
    try:
        return _ORDINALS.index(value)
    except ValueError:
        raise ValueError(f'Unable to convert {value} to an integer')


@overload
def ordinal(value: int) -> str:  # pylint: disable-msg=unused-argument
    """Convert an integer to an ordinal string."""
    ...


@overload
def ordinal(value: str) -> int:  # pylint: disable-msg=function-redefined,unused-argument
    """Convert an ordinal string into the corresponding integer."""
    ...


def ordinal(value):  # pylint: disable-msg=function-redefined
    """Convert an ordinal string to its corresponding integer or vice versa."""
    if isinstance(value, int):
        result = _integer_to_ordinal(value)
    elif isinstance(value, str):
        result = _ordinal_to_integer(value)
    else:
        raise NotImplementedError(f'Unable to convert {type(value)}')
    return result
