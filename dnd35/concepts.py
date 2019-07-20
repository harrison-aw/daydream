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

"""Implements basic concepts used in defining game entities."""

__all__ = ['Modifier', 'Size', 'AbilityScore', 'Race']

from collections import Counter
from functools import total_ordering
from typing import Any, Tuple, List, Optional, Iterable, SupportsInt, Iterator, \
    Set, Sequence, Dict, Union

import dnd35.core as core
import dnd35.numbers as numbers


class AmbiguousOperationError(core.DayDreamError):
    """Error for issues with ambiguous operations."""


@total_ordering
class Modifier:
    """A collection of modifiers to a particular value."""

    stackable = {'unnamed', 'dodge'}

    def __init__(self, *conditional: str, **named: int) -> None:
        super().__init__()

        self.conditional = set(conditional)
        self.named = named

    @property
    def is_simple(self) -> bool:
        """True if it has a single named, unconditional modifier."""
        return bool(self.conditional) or len(self.named) != 1

    def __repr__(self) -> str:
        conditional = ', '.join(repr(c)
                                for c in self.conditional)
        named = ', '.join(f'{name}={val}'
                          for name, val in self.named.items())
        args = ', '.join(a
                         for a in [conditional, named] if a)
        return f'{type(self).__name__}({args})'

    def __str__(self) -> str:
        conditional = '\n'.join(self.conditional)
        named = sum(v for v in self.named.values())

        if named == 0:
            if conditional:
                result = conditional
            else:
                result = '+0'
        else:
            if conditional:
                result = f'+{named}\n{conditional}'
            else:
                result = f'+{named}'

        return result

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Modifier):
            result = (self.named == other.named
                      and self.conditional == other.conditional)
        else:
            result = int(self) == other
        return result

    def __lt__(self, other: Any) -> bool:
        try:
            result = int(self) < int(other)
        except TypeError:
            result = NotImplemented
        return result

    def __int__(self) -> int:
        return sum(bonus for bonus in self.named.values())

    def __getitem__(self, item: str) -> int:
        value = self.named.get(item, 0)
        return value

    def __iter__(self) -> Iterator[str]:
        return iter(self.named)

    def __add__(self, other: 'Modifier') -> 'Modifier':
        if isinstance(other, Modifier):
            new_conditional = self.conditional | set(other.conditional)
            names_self = set(self.named)
            names_other = set(other)

            self_only = names_self - names_other
            other_only = names_other - names_self
            both = names_self & names_other

            new_named = {}
            for name in self_only:
                new_named[name] = self.named[name]
            for name in other_only:
                new_named[name] = other[name]

            for name in both:
                if name in self.stackable:
                    new_named[name] = self.named[name] + other[name]
                else:
                    new_named[name] = max(self.named[name], other[name])

            result = type(self)(*new_conditional, **new_named)
        else:
            result = NotImplemented

        return result

    __radd__ = __add__

    def __mul__(self, other: int) -> 'Modifier':
        if self.is_simple:
            raise AmbiguousOperationError(
                'Multiplication of unspecified or complex modifier is ambiguous'
            )
        name, value = self._unique
        return Modifier(**{name: other * value})

    __rmul__ = __mul__

    def __neg__(self) -> 'Modifier':
        if self.is_simple:
            raise AmbiguousOperationError(
                'Negation of unspecified or complex modifier is ambiguous'
            )
        name, value = self._unique
        return Modifier(**{name: -value})

    @property
    def _unique(self) -> Tuple[str, int]:
        # noinspection PyTypeChecker
        return next(iter(self.named.items()))


class Progression:
    """A progression of modifiers."""

    def __init__(self, modifier_name: str, *values: int) -> None:
        self.modifier_name = modifier_name
        self.modifiers = [Modifier(**{modifier_name: v}) for v in values]

    def __repr__(self) -> str:
        values = ', '.join(str(int(m)) for m in self.modifiers)
        if values:
            suffix = f', {values})'
        else:
            suffix = ')'
        return f"{type(self).__name__}('{self.modifier_name}'" + suffix

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Progression):
            result = tuple(self) == tuple(other)
        else:
            result = NotImplemented
        return result

    def __len__(self) -> int:
        return len(self.modifiers)

    def __getitem__(self, item: int) -> Modifier:
        return self.modifiers[item]

    def __iter__(self) -> Iterator[Modifier]:
        return iter(self.modifiers)


class Size:
    """Size of a creature."""

    def __init__(self, name: str, modifier: int) -> None:
        self.name = name
        self.modifier = Modifier(size=modifier)

    @property
    def attack_bonus(self) -> Modifier:
        """Attack bonus modifier."""
        return -self.modifier

    @property
    def armor_class(self) -> Modifier:
        """Armor class modifier."""
        return -self.modifier

    @property
    def grapple(self) -> Modifier:
        """Grapple attack modifier."""
        return self.modifier * 4

    @property
    def hide(self) -> Modifier:
        """Hide modifier."""
        return self.modifier * -4

    def __repr__(self) -> str:
        modifier = self.modifier['size']
        return f'{type(self).__name__}({repr(self.name)}, {modifier})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Size):
            result = (self.name == other.name
                      and self.modifier == other.modifier)
        else:
            result = NotImplemented
        return result


class AbilityScore:
    """Ability score for a creature."""

    def __init__(self, score: int = 10) -> None:
        self.score = score

    @property
    def modifier(self) -> Modifier:
        """Modifier associated with the ability score."""
        return Modifier(ability=(self.score - 10) // 2)

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


class AbilityType:
    """A type classification for abilities."""

    def __init__(self, name: str, abbreviation: Optional[str] = None) -> None:
        self.name = name
        self.abbreviation = abbreviation

    def __repr__(self) -> str:
        return (type(self).__name__
                + f'({repr(self.name)}, {repr(self.abbreviation)})')

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, AbilityType):
            result = (self.name == other.name
                      and self.abbreviation == other.abbreviation)
        else:
            result = NotImplemented
        return result

    def __str__(self) -> str:
        result = self.name
        if self.abbreviation is not None:
            result += f' ({self.abbreviation})'
        return result


class Ability(core.Aggregator,
              ignore={'name', 'ability_type', 'description'}):
    """Character abilities."""

    def __init__(self,
                 name: str,
                 ability_type: Optional[AbilityType] = None,
                 description: str = '',
                 **features: Any) -> None:
        super().__init__()

        self.name = name
        self.ability_type = ability_type
        self.description = description

        self._features: Set[str] = set()
        for feature, definition in features.items():
            setattr(self, feature, definition)

    def __delattr__(self, name: str) -> None:
        if name in self._features:
            self._features.remove(name)
        super().__delattr__(name)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        ability_name = repr(self.name)
        ability_type = repr(self.ability_type)
        description = repr(self.description)
        prefix = f'{class_name}({ability_name}, {ability_type}, {description}'

        features = ', '.join(f'{name}={repr(getattr(self, name))}'
                             for name in self._features)
        if features:
            result = prefix + ', ' + features + ')'
        else:
            result = prefix + ')'
        return result

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ability):
            # pylint: disable-msg=protected-access
            result = (self.name == other.name
                      and self.ability_type == other.ability_type
                      and self.description == other.description
                      and self._features == other._features
                      and all(getattr(self, a) == getattr(other, a)
                              for a in self._features))
        else:
            result = NotImplemented
        return result

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, item: int) -> Any:
        if self.progression is None:
            raise IndexError('Special ability does not have a progression.')

        return self.progression[item]


class Race(core.Aggregator, ignore={'name'}):
    """Data used to define a character race."""

    favored_class = 'Any'

    bonus_languages = [
        'Abyssal', 'Aquan', 'Auran', 'Celestial', 'Common', 'Draconic',
        'Dwarven', 'Elven', 'Giant', 'Gnome', 'Goblin', 'Gnoll', 'Halfling',
        'Ignan', 'Infernal', 'Orc', 'Sylvan', 'Terran', 'Undercommon'
    ]

    def __init__(self,
                 name: str,
                 size: Size,
                 speed: int,
                 languages: Iterable[str],
                 bonus_languages: Optional[Iterable[str]],
                 favored_class: Optional[str],
                 **features: Any) -> None:
        super().__init__()

        self._name = name
        self._size = size
        self._speed = speed
        self._languages = languages

        self._fortitude = Modifier()
        self._reflex = Modifier()
        self._will = Modifier()

        if bonus_languages is not None:
            self.bonus_languages = list(bonus_languages)

        if favored_class is not None:
            self.favored_class = favored_class

        for feature, definition in features.items():
            setattr(self, feature, definition)

    @property
    def fortitude(self) -> Modifier:
        """Racial bonus to fortitude save."""
        return self._save_bonus('_fortitude')

    @fortitude.setter
    def fortitude(self, modifier: Modifier) -> None:
        self._fortitude = modifier

    @property
    def reflex(self) -> Modifier:
        """Racial bonus to reflex save."""
        return self._save_bonus('_reflex')

    @reflex.setter
    def reflex(self, modifier: Modifier) -> None:
        self._reflex = modifier

    @property
    def will(self) -> Modifier:
        """Racial bonus to will save."""
        return self._save_bonus('_will')

    @will.setter
    def will(self, modifier: Modifier) -> None:
        self._will = modifier

    def _save_bonus(self, name: str) -> Modifier:
        try:
            specific: Modifier = getattr(self, name)
        except AttributeError:
            specific = Modifier()

        try:
            generic: Modifier = self.saving_throws
        except AttributeError:
            generic = Modifier()

        return generic + specific


class ClassFeature:
    """A sequence type for abilities that change with class levels."""

    # pylint: disable=R

    def __init__(self, name: str,
                 description: str = '',
                 **progression: Ability) -> None:
        self.name = name
        self.description = description

        self.progression = {core.ordinal(level): ability
                            for level, ability in progression.items()}

    def __repr__(self) -> str:
        prefix = f'{type(self).__name__}({repr(self.name)},' \
            f' {repr(self.description)}'
        progression = ', '.join(f'{core.ordinal(level)}={repr(ability)}'
                                for level, ability in self.progression.items())
        if progression:
            result = prefix + ', ' + progression + ')'
        else:
            result = prefix + ')'
        return result

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ClassFeature):
            result = (self.name == other.name
                      and self.description == other.description
                      and self.progression == other.progression)
        else:
            result = NotImplemented
        return result

    def __getitem__(self, level: int) -> Ability:
        level = max(lvl for lvl in self.progression if lvl <= level)
        return self.progression[level]


class Class:
    """A character class."""

    # pylint: disable=R

    def __init__(self,
                 alignment_restriction: Optional[List[str]],
                 hit_die: numbers.Die,
                 class_skills: List[str],
                 skill_points_per_level: int,
                 base_attack_bonus: Progression,
                 fort_save: Progression,
                 ref_save: Progression,
                 will_save: Progression,
                 *features: ClassFeature):
        super().__init__()
        self.alignment_restriction = alignment_restriction
        self.hit_die = hit_die
        self.class_skills = class_skills
        self.skill_points_per_level = skill_points_per_level
        self.base_attack_bonus = base_attack_bonus
        self.fort_save = fort_save
        self.ref_save = ref_save
        self.will_save = will_save
        self.features = features


class ClassLevel(core.Aggregator, ignore={'class_', 'level'}):
    """Attained level of a particular class."""

    def __init__(self, class_: Class, level: int) -> None:
        super().__init__()
        self.class_ = class_
        self.level = level

    @property
    def base_attack_bonus(self) -> Modifier:
        """Base attack bonus for the given level."""
        return self.class_.base_attack_bonus[self.level]

    @property
    def fort_save(self) -> Modifier:
        """Fortitude saving throw bonus for the given level."""
        return self.class_.fort_save[self.level]

    @property
    def ref_save(self) -> Modifier:
        """Reflex saving throw bonus for the given level."""
        return self.class_.ref_save[self.level]

    @property
    def will_save(self) -> Modifier:
        """Will saving throw bonus for the given level."""
        return self.class_.will_save[self.level]


class Feat:
    """Ability chosen every few levels or granted by a class."""

    # pylint: disable=R

    def __init__(self, name: str) -> None:
        self.name = name


class Character(core.Aggregator, ignore={'classes'}):
    """A character of some level."""

    # pylint: disable=R

    def __init__(self,
                 race: Race,
                 classes: Dict[Class, int],
                 feats: Sequence[Feat]) -> None:
        super().__init__()

        self.race = race
        self.classes = Counter(classes)
        self.feats = list(feats)

    @property
    def level(self) -> int:
        """The characters level."""
        return len(self.classes)
