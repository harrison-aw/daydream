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

__all__ = ['Size', 'AbilityScore', 'Race']

from collections import Counter
from typing import Any, List, Optional, Iterable, SupportsInt, Iterator, \
    Set, Sequence, Dict, Union

import dnd35e.core as core
import dnd35e.numbers as num


class Progression:
    """A progression of modifiers."""

    def __init__(self, modifier_name: str, *values: int) -> None:
        self._modifier_type = num.ModifierType(modifier_name)
        self._modifiers = [num.Modifier(v, self._modifier_type) for v in values]

    def __repr__(self) -> str:
        values = ', '.join(str(int(m)) for m in self._modifiers)
        if values:
            suffix = f', {values})'
        else:
            suffix = ')'
        return f"{type(self).__name__}('{self._modifier_type.name}'" + suffix

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Progression):
            result = tuple(self) == tuple(other)
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
    """Size of a creature."""

    modifier_type = num.ModifierType('size')

    def __init__(self, name: str, modifier_value: int) -> None:
        self.name = name
        self.modifier = num.Modifier(modifier_value, self.modifier_type)

    @property
    def attack_bonus(self) -> num.Modifier:
        """Attack bonus modifier."""
        return -self.modifier

    @property
    def armor_class(self) -> num.Modifier:
        """Armor class modifier."""
        return -self.modifier

    @property
    def grapple(self) -> num.Modifier:
        """Grapple attack modifier."""
        return 4 * self.modifier

    @property
    def hide(self) -> num.Modifier:
        """Hide modifier."""
        return -4 * self.modifier

    def __repr__(self) -> str:
        return f'{type(self).__name__}({repr(self.name)}, {int(self.modifier)})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Size):
            result = (self.name == other.name
                      and self.modifier == other.modifier)
        else:
            result = NotImplemented
        return result


class AbilityScore:
    """Ability score for a creature."""

    modifier_type = num.ModifierType('ability')

    def __init__(self, score: int = 10) -> None:
        self.score = score

    @property
    def modifier(self) -> num.Modifier:
        """Modifier associated with the ability score."""
        return num.Modifier((self.score - 10) // 2, self.modifier_type)

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

        self._fortitude = num.Modifier()
        self._reflex = num.Modifier()
        self._will = num.Modifier()

        if bonus_languages is not None:
            self.bonus_languages = list(bonus_languages)

        if favored_class is not None:
            self.favored_class = favored_class

        for feature, definition in features.items():
            setattr(self, feature, definition)

    @property
    def fortitude(self) -> num.Modifier:
        """Racial bonus to fortitude save."""
        return self._save_bonus('_fortitude')

    @fortitude.setter
    def fortitude(self, modifier: num.Modifier) -> None:
        self._fortitude = modifier

    @property
    def reflex(self) -> num.Modifier:
        """Racial bonus to reflex save."""
        return self._save_bonus('_reflex')

    @reflex.setter
    def reflex(self, modifier: num.Modifier) -> None:
        self._reflex = modifier

    @property
    def will(self) -> num.Modifier:
        """Racial bonus to will save."""
        return self._save_bonus('_will')

    @will.setter
    def will(self, modifier: num.Modifier) -> None:
        self._will = modifier

    def _save_bonus(self, name: str) -> num.Modifier:
        try:
            specific: num.Modifier = getattr(self, name)
        except AttributeError:
            specific = num.Modifier()

        try:
            generic: num.Modifier = self.saving_throws
        except AttributeError:
            generic = num.Modifier()

        return generic + specific


class ClassFeature:
    """A sequence type for abilities that change with class levels."""

    # pylint: disable=R

    def __init__(self, name: str,
                 description: str = '',
                 **progression: Ability) -> None:
        self.name = name
        self.description = description

        self.progression = {num.ordinal(level): ability
                            for level, ability in progression.items()}

    def __repr__(self) -> str:
        prefix = f'{type(self).__name__}({repr(self.name)},' \
            f' {repr(self.description)}'
        progression = ', '.join(f'{num.ordinal(level)}={repr(ability)}'
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
                 hit_die: num.Die,
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
    def base_attack_bonus(self) -> num.Modifier:
        """Base attack bonus for the given level."""
        return self.class_.base_attack_bonus[self.level]

    @property
    def fort_save(self) -> num.Modifier:
        """Fortitude saving throw bonus for the given level."""
        return self.class_.fort_save[self.level]

    @property
    def ref_save(self) -> num.Modifier:
        """Reflex saving throw bonus for the given level."""
        return self.class_.ref_save[self.level]

    @property
    def will_save(self) -> num.Modifier:
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
