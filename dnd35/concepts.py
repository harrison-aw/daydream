"""Implements basic concepts used in defining game entities."""

from functools import total_ordering
from itertools import chain, groupby
from typing import Any, Tuple, List, Optional, Iterable, SupportsInt, Iterator, \
    AbstractSet, FrozenSet, Set

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
class Modifier:
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
        if isinstance(other, Modifier):
            result = (self.named() == other.named()
                      and self.conditional == other.conditional)
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

    def __iter__(self) -> Iterator[str]:
        return iter(self._named)

    def named(self) -> AbstractSet[Tuple[str, int]]:
        """Collection of name-bonus pairs."""
        return self._named.items()

    def __add__(self, other: 'Modifier') -> 'Modifier':
        if isinstance(other, Modifier):
            new_conditional = self._conditional | set(other.conditional)
            names_self = set(self._named)
            names_other = set(other)

            self_only = names_self - names_other
            other_only = names_other - names_self
            both = names_self & names_other

            new_named = {}
            for name in self_only:
                new_named[name] = self._named[name]
            for name in other_only:
                new_named[name] = other[name]

            for name in both:
                if name in self.stackable:
                    new_named[name] = self._named[name] + other[name]
                else:
                    new_named[name] = max(self._named[name], other[name])

            result = type(self)(*new_conditional, **new_named)
        else:
            result = NotImplemented

        return result

    __radd__ = __add__

    def __mul__(self, other: int) -> 'Modifier':
        if self._conditional or len(self._named) != 1:
            raise ValueError('Multiplication of compound modifier is ambiguous')

        name, value = next(iter(self._named.items()))

        return Modifier(**{name: other * value})

    __rmul__ = __mul__

    def __neg__(self) -> 'Modifier':
        if self._conditional or len(self._named) != 1:
            raise ValueError('Multiplication of compound modifier is ambiguous')

        name, value = next(iter(self._named.items()))

        return Modifier(**{name: -value})

    @property
    def conditional(self) -> FrozenSet[str]:
        """Conditional bonuses."""
        return frozenset(self._conditional)


class Size:
    """Size of a creature."""

    def __init__(self, modifier: int) -> None:
        self._modifier = Modifier(size=modifier)

    def __repr__(self) -> str:
        modifier = self._modifier['size']
        return f'{type(self).__name__}({modifier})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Size):
            result = self._modifier == other.modifier
        else:
            result = NotImplemented
        return result

    def __hash__(self) -> int:
        return hash(('Size', self._modifier))

    @property
    def modifier(self) -> Modifier:
        """Base modifier."""
        return self._modifier

    @property
    def attack_bonus(self) -> Modifier:
        """Attack bonus modifier."""
        return -self._modifier

    @property
    def armor_class(self) -> Modifier:
        """Armor class modifier."""
        return -self._modifier

    @property
    def grapple(self) -> Modifier:
        """Grapple attack modifier."""
        return self._modifier * 4

    @property
    def hide(self) -> Modifier:
        """Hide modifier."""
        return self._modifier * -4


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

        self._name = name
        self._parameter = parameter
        self._description = description
        self._features: Set[str] = set()

        for feature, definition in features.items():
            setattr(self, feature, definition)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if not name.startswith('_'):
            self._features.add(name)

    def __repr__(self) -> str:
        class_name = type(self).__name__
        features = ', '.join(f'{name}={getattr(self, name)}' for name in self._features)

        prefix = f'{class_name}({self._name}, {self._parameter}, {self._description}'
        if features:
            result = prefix + ', ' + features + ')'
        else:
            result = prefix + ')'
        return result


class Race(core.Aggregator, ignore={'name'}):
    """Data used to define a character race."""

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

        self._fortitude = Modifier()
        self._reflex = Modifier()
        self._will = Modifier()

        if bonus_languages is not None:
            self.bonus_languages = bonus_languages

        if favored_class is not None:
            self.favored_class = favored_class

        for feature, definition in features.items():
            setattr(self, feature, definition)

    def _save_bonus(self, name: str) -> Modifier:
        try:
            generic = self.saving_throws
        except AttributeError:
            generic = Modifier()

        return generic + getattr(self, name)

    @property
    def fortitude(self) -> Modifier:
        """Racial bonus to fortitude save."""
        return self._save_bonus('_fortitude')

    @fortitude.setter
    def fortitude(self, bonus: Modifier) -> None:
        self._fortitude = bonus

    @property
    def reflex(self) -> Modifier:
        """Racial bonus to reflex save."""
        return self._save_bonus('_reflex')

    @reflex.setter
    def reflex(self, bonus: Modifier) -> None:
        self._reflex = bonus

    @property
    def will(self) -> Modifier:
        """Racial bonus to will save."""
        return self._save_bonus('_will')

    @will.setter
    def will(self, bonus: Modifier) -> None:
        self._will = bonus


class Class(core.Aggregator):
    """A character class."""

    def __init__(self,
                 alignment_restriction: Optional[List[str]],
                 hit_die: Dice,
                 class_skills: List[str],
                 skill_points_per_level: int,
                 base_attack_bonus: List[Modifier],
                 fort_save: List[Modifier],
                 ref_save: List[Modifier],
                 will_save: List[Modifier],
                 special: List[List[Any]],
                 **features: Any):
        super().__init__()
        self.alignment_restriction = alignment_restriction
        self.hit_die = hit_die
        self.class_skills = class_skills
        self.skill_points_per_level = skill_points_per_level
        self.base_attack_bonus = base_attack_bonus
        self.fort_save = fort_save
        self.ref_save = ref_save
        self.will_save = will_save
        self.special = special
        self.features = features


__all__ = ['Modifier', 'Size', 'AbilityScore', 'Race']
