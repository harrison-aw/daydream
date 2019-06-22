from typing import Any
from collections import defaultdict

from .core import Aggregator, Value


class Conditional(Value, value_name='static'):
    """An addable and comparable type that can have optional conditional elements.

    Only addition makes sense for a conditional value.
    """

    def __init__(self, static: Any, *conditionals: Any):
        """Initialize static and conditional parts of the value."""
        self.static = static
        self.conditionals = list(conditionals)

    def __repr__(self):
        conditionals = ', '.join(repr(c) for c in self.conditionals)
        return f'{type(self).__name__}({self.static}, {conditionals})'

    def __add__(self, other: Any) -> 'Conditional':
        try:
            static = self.static + other.static
            conditionals = (self.conditionals
                            + [c
                               for c in other.conditionals
                               if c not in self.conditionals])
        except AttributeError:
            try:
                static = self.static + other
                conditionals = self.conditionals
            except TypeError:
                return NotImplemented
        return type(self)(static, *conditionals)

    def __radd__(self, other: Any) -> 'Conditional':
        try:
            static = other + self.static
        except TypeError:
            return NotImplemented
        return type(self)(static, *self.conditionals)

    def __iadd__(self, other: Any) -> 'Conditional':
        try:
            conditionals = [c
                            for c in other.conditionals
                            if c not in self.conditionals]
            static = other.static
        except AttributeError:
            try:
                self.static += other
            except TypeError:
                return NotImplemented
        else:
            self.conditionals.extend(conditionals)
            self.static += static
        return self


class Size(Value, value_name='modifier'):
    """Size of a creature."""

    def __init__(self, modifier: int) -> None:
        self.modifier = modifier

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.modifier})'

    @property
    def attack_bonus(self) -> int:
        return self.modifier

    @property
    def armor_class(self) -> int:
        return self.modifier

    @property
    def grapple(self) -> int:
        return -2 * self.modifier

    @property
    def hide(self) -> int:
        return 2 * self.modifier


class AbilityScore(Value, value_name='score'):
    """Ability score for a creature."""

    def __init__(self, score: int = 10) -> None:
        self.score = score

    @property
    def modifier(self) -> int:
        return (self.score - 10) // 2


class Bonus(Value, value_name='bonus'):
    """A collection of modifiers to a roll."""

    stackable = {'untyped', 'dodge'}

    def __init__(self, **bonuses: int) -> None:
        self.bonuses = defaultdict(int, bonuses)

    def __repr__(self) -> str:
        args = ', '.join(f'{type_}={bonus}'
                         for type_, bonus in self.bonuses.items())
        return f'{type(self).__name__}({args})'

    def __eq__(self, other: Any) -> bool:
        try:
            return self.bonuses == other.bonuses
        except AttributeError:
            return NotImplemented

    @property
    def bonus(self) -> int:
        """Combine all bonus modifiers."""
        return sum(bonus for bonus in self.bonuses.values())

    def __add__(self, other: Any) -> 'Bonus':
        try:
            types = list(set(self.bonuses) | set(other.bonuses))

            new_bonuses = {}
            for type_ in types:
                if type_ in self.stackable:
                    new_bonuses[type_] = (self.bonuses[type_]
                                          + other.bonuses[type_])
                else:
                    new_bonuses[type_] = max(self.bonuses[type_],
                                             other.bonuses[type_])
            return type(self)(**new_bonuses)
        except AttributeError:
            return NotImplemented

    __radd__ = __add__

    def __iadd__(self, other: Any) -> 'Bonus':
        try:
            for type_, bonus in other.types.items():
                if type_ in self.stackable:
                    self.bonuses[type_] = self.bonuses[type_] + bonus
                else:
                    self.bonuses[type_] = max(self.bonuses[type_], bonus)
            return self
        except AttributeError:
            return NotImplemented


class Entity(Aggregator, ignore={'name'}):
    """An named collection of attributes."""

    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            setattr(self, name, value)


class _Any:
    """An object that is equal to every other object."""

    def __eq__(self, other: Any) -> bool:
        return True


any_ = _Any()
