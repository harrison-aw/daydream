"""Implements basic concepts used in defining game entities."""

from functools import total_ordering
from itertools import chain, groupby
from typing import Any, Tuple, List, Optional, Iterable, SupportsInt

import dnd35.core as core

_DiceCounts = Tuple[int, Optional[int]]
_AbstractDicePool = Iterable[_DiceCounts]
_DicePool = List[_DiceCounts]


class BadDiceError(core.DayDreamError):
    """Error for issues with dice value."""


class Dice:
    """Represents a pool of dice."""

    def __init__(self,
                 side_count: Optional[int] = None,
                 die_count: Optional[int] = None,
                 pool: Optional[_AbstractDicePool] = None) -> None:
        if side_count is None:
            if die_count is None:
                self._pool: _DicePool = []
            else:
                raise BadDiceError('Cannot create dice with an unspecified number of sides.')
        else:
            self._pool = [(side_count, die_count)]

        if pool is not None:
            self._pool = self._combine(self._pool, pool)

    @staticmethod
    def _combine(first_pool: _AbstractDicePool, second_pool: _AbstractDicePool,
                 _key=lambda c: c[0]) -> _DicePool:
        """Combine two dice pools."""
        result: _DicePool = []

        combinable: _DicePool = []
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

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Dice):
            result = self.pool == other.pool
        else:
            result = NotImplemented
        return result

    def __hash__(self) -> int:
        return hash(('Dice', tuple(self._pool)))

    def __repr__(self) -> str:
        if len(self._pool) == 1:
            side_count, dice_count = self._pool[0]
            if dice_count is None:
                args = f'{side_count}'
            else:
                args = f'{side_count}, {dice_count}'
        else:
            args = f'pool={self._pool}'

        return f'{type(self).__name__}({args})'

    def __str__(self) -> str:
        terms = []
        for side_count, dice_count in self._pool:
            if dice_count is None:
                terms.append(f'd{side_count}')
            else:
                terms.append(f'{dice_count}d{side_count}')

        return ' + '.join(terms)

    def __add__(self, other: 'Dice') -> 'Dice':
        if isinstance(other, Dice):
            result = Dice(pool=self._combine(self._pool, other.pool))
        else:
            result = NotImplemented

        return result

    @property
    def average(self) -> float:
        """Average dice roll."""
        result = 0.
        for side_count, dice_count in self._pool:
            if dice_count is None:
                dice_count = 1
            result += dice_count * (side_count + 1) / 2
        return result

    @property
    def pool(self) -> Tuple[_DiceCounts, ...]:
        """The encoded version of the dice pool."""
        return tuple(self._pool)


@total_ordering
class Bonus:
    """A collection of modifiers to a particular value."""

    stackable = {'unnamed', 'dodge'}

    def __init__(self, *conditional: str, **named: int) -> None:
        super().__init__()

        self._conditional = set(conditional)
        self._named = named

    def __repr__(self) -> str:
        conditional = ', '.join(repr(c) for c in self._conditional)
        named = ', '.join(f'{name}={val}' for name, val in self._named.items())
        args = ', '.join(a for a in [conditional, named] if a)
        return f'{type(self).__name__}({args})'

    def __str__(self) -> str:
        conditional = '\n'.join(self._conditional)
        named = sum(v for v in self._named.values())

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
        if isinstance(other, Bonus):
            result = (self._named == other._named
                      and self._conditional == other._conditional)
        else:
            result = int(self) == other
        return result

    def __hash__(self) -> int:
        conditional = tuple(sorted(self._conditional))
        typed = tuple(self._named.items())
        return hash(('Bonus', conditional, typed))

    def __lt__(self, other: Any) -> bool:
        return int(self) < other

    def __int__(self) -> int:
        return sum(bonus for bonus in self._named.values())

    def __getitem__(self, item: str) -> int:
        value = self._named.get(item, 0)
        return value

    def __add__(self, other: 'Bonus') -> 'Bonus':
        try:
            new_conditional = self._conditional | other._conditional
            names_self = set(self._named)
            names_other = set(other._named)
        except AttributeError:
            result = NotImplemented
        else:
            self_only = names_self - names_other
            other_only = names_other - names_self
            both = names_self & names_other

            new_named = {}
            for name in self_only:
                new_named[name] = self._named[name]
            for name in other_only:
                new_named[name] = other._named[name]

            for name in both:
                if name in self.stackable:
                    new_named[name] = self._named[name] + other._named[name]
                else:
                    new_named[name] = max(self._named[name], other._named[name])

            result = type(self)(*new_conditional, **new_named)

        return result

    __radd__ = __add__


class Size:
    """Size of a creature."""

    def __init__(self, modifier: int) -> None:
        self.__modifier = modifier

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.__modifier})'

    def __eq__(self, other: Any) -> bool:
        try:
            result = self.__modifier == other.modifier
        except AttributeError:
            result = self.__modifier == other
        return result

    def __hash__(self) -> int:
        return hash(('Size', self.__modifier))

    @property
    def modifier(self) -> int:
        """Base modifier."""
        return self.__modifier

    @property
    def attack_bonus(self) -> int:
        """Attack bonus modifier."""
        return self.__modifier

    @property
    def armor_class(self) -> int:
        """Armor class modifier."""
        return self.__modifier

    @property
    def grapple(self) -> int:
        """Grapple attack modifier."""
        return -2 * self.__modifier

    @property
    def hide(self) -> int:
        """Hide modifier."""
        return 2 * self.__modifier


class AbilityScore:
    """Ability score for a creature."""

    def __init__(self, score: int = 10) -> None:
        self.score = score

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.score})'

    def __eq__(self, other: Any) -> bool:
        try:
            result = self.score == other.score
        except AttributeError:
            result = self.score == other
        return result

    def __add__(self, other: SupportsInt) -> 'AbilityScore':
        try:
            value = int(other)
        except TypeError:
            result = NotImplemented
        else:
            result = type(self)(self.score + value)
        return result

    __radd__ = __add__

    def __iadd__(self, other: SupportsInt) -> 'AbilityScore':
        try:
            value = int(other)
        except TypeError:
            result = NotImplemented
        else:
            self.score += value
            result = self
        return result

    @property
    def modifier(self) -> int:
        """Modifier associated with the ability score."""
        return (self.score - 10) // 2


class Special(core.Aggregator, ignore={'name', 'description'}):
    """Special abilities."""

    def __init__(self,
                 name: str,
                 parameter: Optional[Any] = None,
                 description: Optional[str] = None,
                 **features: Any) -> None:
        super().__init__()

        self.name = name
        self.parameter = parameter
        self.description = description

        for feature, definition in features.items():
            setattr(self, feature, definition)


class Race(core.Aggregator, ignore={'name'}):
    favored_class = 'Any'

    bonus_languages = ['Abyssal', 'Aquan', 'Auran', 'Celestial', 'Common',
                       'Draconic', 'Dwarven', 'Elven', 'Giant', 'Gnome',
                       'Goblin', 'Gnoll', 'Halfling', 'Ignan', 'Infernal',
                       'Orc', 'Sylvan', 'Terran', 'Undercommon']

    def __init__(self,
                 name: str,
                 size: Size,
                 speed: int,
                 languages: List[str],
                 bonus_languages: Optional[List[str]],
                 favored_class: Optional[str],
                 **features: Any) -> None:
        super().__init__()

        self.name = name
        self.size = size
        self.speed = speed
        self.languages = languages

        self._fortitude = Bonus()
        self._reflex = Bonus()
        self._will = Bonus()

        if bonus_languages is not None:
            self.bonus_languages = bonus_languages

        if favored_class is not None:
            self.favored_class = favored_class

        for feature, definition in features.items():
            setattr(self, feature, definition)

    def _save_bonus(self, name: str) -> Bonus:
        try:
            generic = self.saving_throws
        except AttributeError:
            generic = Bonus()

        return generic + getattr(self, name)

    @property
    def fortitude(self) -> Bonus:
        return self._save_bonus('_fortitude')

    @fortitude.setter
    def fortitude(self, bonus: Bonus) -> None:
        self._fortitude = bonus

    @property
    def reflex(self) -> Bonus:
        return self._save_bonus('_reflex')

    @reflex.setter
    def reflex(self, bonus: Bonus) -> None:
        self._reflex = bonus

    @property
    def will(self) -> Bonus:
        return self._save_bonus('_will')

    @will.setter
    def will(self, bonus: Bonus) -> None:
        self._will = bonus


class Class(core.Aggregator):
    def __init__(self,
                 alignment_restriction: Optional[List[str]],
                 hit_die: Dice,
                 class_skills: List[str],
                 skill_points_per_level: int,
                 base_attack_bonus: List[Bonus],
                 fort_save: List[Bonus],
                 ref_save: List[Bonus],
                 will_save: List[Bonus],
                 special: List[List[Any]],
                 **features: Any):
        super().__init__()
        self.alignment_restriction = alignment_restriction
        self.hit_die = hit_die
        self.class_skills = class_skills
        self.skill_points_per_level = skill_points_per_level


__all__ = ['Bonus', 'Size', 'AbilityScore', 'Race']
