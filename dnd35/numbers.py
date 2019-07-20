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

from typing import Tuple, List, Any, Union, DefaultDict, Dict, Optional
from copy import deepcopy
from collections import defaultdict
from itertools import chain
from functools import total_ordering
from dataclasses import dataclass

import dnd35.core as core


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

    def __str__(self) -> str:
        return f'{self.name}'


UNTYPED = ModifierType('untyped', stacks=True)


class ModifierCombinationError(core.DayDreamError):
    """Error raised when combining modifiers cannot be accomplished."""


class DifferentModifierTypesError(ModifierCombinationError):
    """Error for attempting to add two modifiers with different types.

    Modifiers only track a single type and, therefore, cannot support
    addition between different types.
    """


class BonusAndPenaltyCombinationError(ModifierCombinationError):
    """Error raised when attempting to add an unstackable bonus and penalty.

    This situation can cause a loss of information. The best bonus and
    the worst penalty should both apply.
    """


class DifferentConditionsError(ModifierCombinationError):
    """Error raised when attempting to add modifiers with different conditions.

    Modifiers only track a single numerical bonus and cannot, therefore,
    handle multiple conditions that would necessitate multiple different.
    values.
    """


@total_ordering
@dataclass(frozen=True)
class Modifier:
    # noinspection PyUnresolvedReferences
    """A bonus or penalty to a dice roll or other value.

    :param value: the numerical value of the modifier
    :param type: the type of modifier, used to determine stacking rules
    :param condition: optional, a limited situation to which the
        modifier applies
    """

    value: int = 0
    type: ModifierType = UNTYPED
    condition: Optional[core.Condition] = None

    @property
    def is_bonus(self) -> bool:
        """Determine if the modifier is a bonus."""
        return self.value >= 0

    @property
    def is_penalty(self) -> bool:
        """Determine if the modifier is a penalty."""
        return self.value <= 0

    def __str__(self) -> str:
        type_string = str(self.type)
        if (not type_string.endswith('bonus')
                or not type_string.endswith('penalty')):
            if self.value >= 0:
                type_string += ' bonus'
            else:
                type_string += ' penalty'

        if self.condition is not None:
            condition_string = ' ' + str(self.condition)
        else:
            condition_string = ''

        return f'{self.value:+} {type_string}{condition_string}'

    def __add__(self, other: Any) -> Union['Modifier', 'NotImplemented']:
        if isinstance(other, Modifier):
            # pylint: disable=protected-access

            if self.type != other.type:
                raise DifferentModifierTypesError(
                    f'Cannot add modifiers of different types: {self.type} '
                    f'and {other.type}'
                )

            if self.type.stacks:
                result = Modifier(self.value + other.value, self.type)
            else:
                if self.is_bonus and other.is_bonus:
                    result = Modifier(max(self.value, other.value), self.type)
                elif self.is_penalty and other.is_penalty:
                    result = Modifier(min(self.value, other.value), self.type)
                else:
                    raise BonusAndPenaltyCombinationError(
                        f'Combining a bonus and a penalty loses information: '
                        f'{self.value:+} and {other.value:+}'
                    )
        else:
            result = NotImplemented
        return result

    def __lt__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, Modifier):
            # pylint: disable=protected-access
            if self.type != other.type:
                raise DifferentModifierTypesError(
                    f'Cannot compare modifiers of different types: '
                    f'{self.type} and {other.type}'
                )

            result = self.value < other.value
        elif isinstance(other, int):
            result = self.value < other
        else:
            result = NotImplemented
        return result


_ModifierKey = Tuple[ModifierType, bool, Optional[core.Condition]]


class ModifierTotal:
    """A sum of modifiers.

    :param modifiers: a collection of modifiers
    """

    def value(self, *conditions_met: core.Condition) -> int:
        """Get the numerical value of the total."""
        return sum(mod.value for mod in self._modifiers.values()
                   if (mod.condition is None
                       or mod.condition in conditions_met))

    @property
    def conditions(self) -> List[core.Condition]:
        """Get all of the conditions present in modifiers."""
        return [key[2] for key in self._modifiers if key[2] is not None]

    def __init__(self, *modifiers: Modifier):
        self._modifiers: Dict[_ModifierKey, Modifier] = {}
        for mod in modifiers:
            key = (mod.type,
                   mod.type.stacks or mod.is_bonus,
                   mod.condition)
            if key in self._modifiers:
                self._modifiers[key] += mod
            else:
                self._modifiers[key] = mod

    def __repr__(self) -> str:
        args = ', '.join(repr(mod) for mod in self._modifiers.values())
        return type(self).__name__ + f'({args})'

    def __eq__(self, other: Any) -> Union[bool, 'NotImplemented']:
        if isinstance(other, ModifierTotal):
            # pylint: disable=protected-access
            result = self._modifiers == other._modifiers
        else:
            result = NotImplemented
        return result
