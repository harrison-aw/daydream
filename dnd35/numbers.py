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

"""Classes and helper function for working with numerical values."""

__all__ = ['Die', 'DicePool']

from typing import Tuple, List, Any, Union, DefaultDict
from copy import deepcopy
from collections import defaultdict
from itertools import chain
from functools import total_ordering
from dataclasses import dataclass


@total_ordering
class Die:
    """Represents a single die.

    :param side_count: number of sides on the die
    """

    @classmethod
    def from_string(cls, die_string: str) -> 'Die':
        """Construct a die from a string.

        :param die_string: a string beginning with 'd' and ending with
            an integer
        """
        if die_string[0] != 'd':
            raise ValueError(
                f"A die string must start with d, got '{die_string}'"
            )

        try:
            side_count = int(die_string[1:])
        except ValueError:
            raise ValueError(
                f"Invalid die string, got '{die_string}', expected something "
                f"like 'd6'"
            ) from None
        else:
            return cls(side_count)

    @property
    def average(self) -> float:
        """Average dice roll."""
        return (self._side_count + 1) / 2

    def __init__(self, side_count: int) -> None:
        self._side_count = side_count

    def __repr__(self) -> str:
        return type(self).__name__ + f'({self._side_count})'

    def __str__(self) -> str:
        return f'd{self._side_count}'

    def __eq__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, Die):
            # pylint: disable=protected-access
            result = self._side_count == other._side_count
        else:
            result = NotImplemented
        return result

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._side_count))

    def __lt__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, Die):
            # pylint: disable=protected-access
            result = self._side_count < other._side_count
        else:
            result = NotImplemented
        return result


class DicePool:
    """A pool of dice.

    :param die_counts: die strings are used to specify how many sides a
        given dice has while the value assigned to the dice string
        represents how many of that kind of die are present, example:
        DicePool(d6=1, d8=4) creates a pool with 1d6 and 4d8 present.
    """

    @property
    def average(self) -> float:
        """Compute the average value of a roll of all dice in the pool."""
        return sum(count * die.average for die, count in self._pool.items())

    def __init__(self, **die_counts: int) -> None:
        self._pool: DefaultDict[Die, int] = defaultdict(int)
        for die_string, count in die_counts.items():
            die = Die.from_string(die_string)
            self._pool[die] += count

    def __eq__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, DicePool):
            # pylint: disable=protected-access
            result = self._sorted == other._sorted
        else:
            result = NotImplemented
        return result

    def __repr__(self) -> str:
        pool_string = ', '.join(f'{die}={count}' for die, count in self._sorted)
        return type(self).__name__ + f'({pool_string})'

    def __add__(self, other: Any) -> Union['DicePool', 'NotImplemented']:
        if isinstance(other, DicePool):
            # pylint: disable=protected-access
            new_pool_args: DefaultDict[str, int] = defaultdict(int)
            for die, count in chain(self._pool.items(), other._pool.items()):
                new_pool_args[str(die)] += count
            result = DicePool(**new_pool_args)
        elif isinstance(other, Die):
            new_pool: DefaultDict[Die, int] = deepcopy(self._pool)
            new_pool[other] += 1
            result = DicePool(**{str(die): count
                                 for die, count in new_pool.items()})
        else:
            result = NotImplemented
        return result

    __radd__ = __add__

    @property
    def _sorted(self) -> List[Tuple[Die, int]]:
        """Returns a sorted list of each die and its count in the pool."""
        result = [(die, count) for die, count in self._pool.items()
                  if count > 0]
        result.sort(key=lambda x: x[0])
        return result


@dataclass(frozen=True)
class ModifierType:
    """Type of a bonus or penalty and its stacking behavior."""
    name: str
    stacks: bool = False


UNTYPED = ModifierType('untyped', stacks=True)


class Modifier:
    """A bonus or penalty to a dice roll.

    :param value: amount to add or subtract from a roll
    :param type_: type of modifier, determines stacking behavior
    """

    def __init__(self, value: int, type_: ModifierType = UNTYPED) -> None:
        self._value = value
        self._type = type_

    def __eq__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, Modifier):
            # pylint: disable=protected-access
            result = self._type == other._type and self._value == other._value
        else:
            result = NotImplemented
        return result

    def __repr__(self) -> str:
        return type(self).__name__ + f'({self._value}, {self._type})'

    def __str__(self) -> str:
        if self._value >= 0:
            result = f'+{self._value}'
        else:
            result = f'{self._value}'
        return result
