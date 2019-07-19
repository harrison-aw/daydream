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

__all__ = ['Die', 'Dice', 'BadDiceError']

from typing import Tuple, Optional, Iterable, List, Any, Union
from itertools import chain, groupby

import dnd35.core as core


class Die:
    """Represents a single die.

    :param side_count: number of sides on the die
    """

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


DiceCounts = Tuple[int, Optional[int]]
AbstractDicePool = Iterable[DiceCounts]
DicePool = List[DiceCounts]


class BadDiceError(core.DayDreamError):
    """Error for issues with dice value."""


class Dice:
    """Represents a pool of dice."""

    def __init__(self,
                 side_count: Optional[int] = None,
                 die_count: Optional[int] = None,
                 pool: Optional[AbstractDicePool] = None) -> None:
        if side_count is None:
            if die_count is None:
                self.pool: DicePool = []
            else:
                raise BadDiceError('Cannot create dice with an unspecified number of sides.')
        else:
            self.pool = [(side_count, die_count)]

        if pool is not None:
            self.pool = self._combine(self.pool, pool)

    @property
    def average(self) -> float:
        """Average dice roll."""
        result = 0.
        for side_count, dice_count in self.pool:
            if dice_count is None:
                dice_count = 1
            result += dice_count * (side_count + 1) / 2
        return result

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Dice):
            result = set(self.pool) == set(other.pool)
        else:
            result = NotImplemented
        return result

    def __hash__(self) -> int:
        return hash((type(self).__name__, tuple(self.pool)))

    def __repr__(self) -> str:
        if len(self.pool) == 1:
            side_count, dice_count = self.pool[0]
            if dice_count is None:
                args = f'{side_count}'
            else:
                args = f'{side_count}, {dice_count}'
        else:
            args = f'pool={self.pool}'

        return f'{type(self).__name__}({args})'

    def __str__(self) -> str:
        terms = []
        for side_count, dice_count in self.pool:
            if dice_count is None:
                terms.append(f'd{side_count}')
            else:
                terms.append(f'{dice_count}d{side_count}')

        return ' + '.join(terms)

    def __add__(self, other: 'Dice') -> 'Dice':
        if isinstance(other, Dice):
            result = Dice(pool=self._combine(self.pool, other.pool))
        else:
            result = NotImplemented

        return result

    @staticmethod
    def _combine(first_pool: AbstractDicePool, second_pool: AbstractDicePool,
                 _key=lambda c: c[0]) -> DicePool:
        """Combine two dice pools."""
        result: DicePool = []

        combinable: DicePool = []
        for side_count, dice_count in chain(first_pool, second_pool):
            if dice_count is None:
                result.append((side_count, dice_count))
            else:
                combinable.append((side_count, dice_count))

        result.sort(key=_key)
        combinable.sort(key=_key)

        result.extend((side_count, sum(c[1] for c in counts))
                      for side_count, counts in groupby(combinable, key=_key))
        return result
