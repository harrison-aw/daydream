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

"""Implements basic concepts used in game rules."""

__all__ = ['Size', 'AbilityScore']

from typing import Any, Optional, SupportsInt, Iterator, Set, Union
from dataclasses import dataclass

import dnd35e.core as core
import dnd35e.numbers as num


class Progression:
    """A progression of modifiers.

    Character classes have a number of modifiers that increase with
    level progression such as base attack bonus and various saving
    throws (fortitude, reflex, and will). This class allows those to be
    easily created in a list-like object.

    :param modifier_name: name of modifier in progression, defines
        modifier type
    :param values: the values of the modifiers in the the progression
    """

    def __init__(self, modifier_name: str, *values: int) -> None:
        modifier_type = num.ModifierType(modifier_name)
        self._modifiers = [num.Modifier(v, modifier_type)
                           for v in values]

    def __repr__(self) -> str:
        values = ', '.join(str(int(m)) for m in self._modifiers)
        if values:
            modifier_name = repr(self._modifiers[0].type.name)
            values = ', ' + values
        else:
            modifier_name = ''
        return type(self).__name__ + f"({modifier_name}{values})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Progression):
            # pylint: disable=protected-access
            result = self._modifiers == other._modifiers
        else:
            result = NotImplemented
        return result

    def __len__(self) -> int:
        return len(self._modifiers)

    def __getitem__(self, item: int) -> num.Modifier:
        return self._modifiers[item]

    def __iter__(self) -> Iterator[num.Modifier]:
        return iter(self._modifiers)


class Size:
    """Size of a creature.

    :param name: name of the size category this value represents
    :param modifier_value: base value for size modifiers
    """

    modifier_type = num.ModifierType('size')

    @property
    def name(self) -> str:
        """Name of the size category."""
        return self._name

    @property
    def attack(self) -> num.Modifier:
        """Attack bonus modifier."""
        return -self._modifier

    @property
    def armor_class(self) -> num.Modifier:
        """Armor class modifier."""
        return -self._modifier

    @property
    def grapple(self) -> num.Modifier:
        """Grapple attack modifier."""
        return 4 * self._modifier

    @property
    def hide(self) -> num.Modifier:
        """Hide modifier."""
        return -4 * self._modifier

    def __init__(self, name: str, modifier_value: int) -> None:
        self._name = name
        self._modifier = num.Modifier(modifier_value, self.modifier_type)

    def __repr__(self) -> str:
        return (type(self).__name__
                + f'({repr(self._name)}, {int(self._modifier)})')

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Size):
            # pylint: disable=protected-access
            result = (self._name == other._name
                      and self._modifier == other._modifier)
        else:
            result = NotImplemented
        return result


class AbilityScore:
    """Ability score for a creature.

    :param score: value of the ability score, typically between 3 and 20.
    """

    modifier_type = num.ModifierType('ability')

    @property
    def modifier(self) -> num.Modifier:
        """Modifier associated with the ability score."""
        return num.Modifier((self.score - 10) // 2, self.modifier_type)

    def __init__(self, score: int = 10) -> None:
        self.score = score

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.score})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AbilityScore):
            result = self.score == other.score
        else:
            try:
                result = self.score == int(other)
            except TypeError:
                result = NotImplemented
        return result

    def __add__(self, other: SupportsInt) -> Union['AbilityScore',
                                                   'NotImplemented']:
        try:
            value = int(other)
        except TypeError:
            result = NotImplemented
        else:
            result = type(self)(self.score + value)
        return result

    __radd__ = __add__

    def __iadd__(self, other: SupportsInt) -> Union['AbilityScore',
                                                    'NotImplemented']:
        try:
            value = int(other)
        except TypeError:
            result = NotImplemented
        else:
            self.score += value
            result = self
        return result


@dataclass(frozen=True)
class AbilityType:
    # noinspection PyUnresolvedReferences
    """A type classification for abilities.

    Abilities are categorized by their source: natural, supernatural,
    extraordinary, etc. This defines data relevant to the type.

    :param name: name of the type
    :param abbreviation: abbreviated name of the type
    """

    name: str
    abbreviation: Optional[str] = None

    def __str__(self) -> str:
        result = self.name
        if self.abbreviation is not None:
            result += f' ({self.abbreviation})'
        return result


class Ability(core.Aggregator,
              ignore={'name', 'ability_type', 'description'}):
    """Character abilities.

    This represents any ability that a character can gain from any
    source (race, class, feat, etc.). An example is the "Stonecunning"
    ability granted by the Dwarven race.

    :param name: name of the ability
    :param ability_type: type of the ability, describes the source of
        the ability
    :param description: describes what the ability grants and details of
        how it functions
    :param features: objects that programmatically define the behavior
        of the ability such as modifiers it grants.
    """

    default_ability_type = AbilityType('Natural')

    @property
    def name(self) -> str:
        """Get the ability's name."""
        return self._name

    @property
    def ability_type(self) -> AbilityType:
        """Get the ability's type."""
        return self._ability_type

    @property
    def description(self) -> str:
        """Get the ability's description."""
        return self._description

    def __init__(self,
                 name: str,
                 ability_type: Optional[AbilityType] = None,
                 description: str = '',
                 **features: Any) -> None:
        super().__init__()

        self._name = name
        if ability_type is None:
            self._ability_type = AbilityType('')
        else:
            self._ability_type = self.default_ability_type
        self._description = description

        self._features: Set[str] = set()
        for feature, definition in features.items():
            setattr(self, feature, definition)

    def __delattr__(self, name: str) -> None:
        if name in self._features:
            self._features.remove(name)
        super().__delattr__(name)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        ability_name = repr(self._name)
        ability_type = repr(self._ability_type)
        description = repr(self._description)
        prefix = f'{class_name}({ability_name}, {ability_type}, {description}'

        features = ', '.join(f'{name}={repr(getattr(self, name))}'
                             for name in self._features)
        if features:
            result = prefix + ', ' + features + ')'
        else:
            result = prefix + ')'
        return result

    def __str__(self) -> str:
        return self._name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ability):
            # pylint: disable-msg=protected-access
            result = (self._name == other._name
                      and self._ability_type == other._ability_type
                      and self._description == other._description
                      and self._features == other._features
                      and all(getattr(self, a) == getattr(other, a)
                              for a in self._features))
        else:
            result = NotImplemented
        return result
