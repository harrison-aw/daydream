# OPEN GAME LICENSE Version 1.0a
#
# The following text is the property of Wizards of the Coast, Inc. and
# is Copyright 2000 Wizards of the Coast, Inc ("Wizards"). All Rights
# Reserved.
#
#     Definitions:
#         "Contributors" means the copyright and/or trademark owners who
#             have contributed Open Game Content;
#         "Derivative Material" means copyrighted material including
#             derivative works and translations (including into other
#             computer languages), potation, modification, correction,
#             addition, extension, upgrade, improvement, compilation,
#             abridgment or other form in which an existing work may be
#             recast, transformed or adapted;
#         "Distribute" means to reproduce, license, rent, lease, sell,
#             broadcast, publicly display, transmit or otherwise
#             distribute;
#         "Open Game Content" means the game mechanic and includes the
#             methods, procedures, processes and routines to the extent
#             such content does not embody the Product Identity and is
#             an enhancement over the prior art and any additional
#             content clearly identified as Open Game Content by the
#             Contributor, and means any work covered by this License,
#             including translations and derivative works under
#             copyright law, but specifically excludes Product Identity.
#         "Product Identity" means product and product line names, logos
#             and identifying marks including trade dress; artifacts;
#             creatures characters; stories, storylines, plots, thematic
#             elements, dialogue, incidents, language, artwork, symbols,
#             designs, depictions, likenesses, formats, poses, concepts,
#             themes and graphic, photographic and other visual or audio
#             representations; names and descriptions of characters,
#             spells, enchantments, personalities, teams, personas,
#             likenesses and special abilities; places, locations,
#             environments, creatures, equipment, magical or
#             supernatural abilities or effects, logos, symbols, or
#             graphic designs; and any other trademark or registered
#             trademark clearly identified as Product identity by the
#             owner of the Product Identity, and which specifically
#             excludes the Open Game Content;
#         "Trademark" means the logos, names, mark, sign, motto, designs
#             that are used by a Contributor to identify itself or its
#             products or the associated products contributed to the
#             Open Game License by the Contributor
#         "Use", "Used" or "Using" means to use, Distribute, copy, edit,
#             format, modify, translate and otherwise create Derivative
#             Material of Open Game Content.
#         "You" or "Your" means the licensee in terms of this agreement.
#     The License: This License applies to any Open Game Content that
#         contains a notice indicating that the Open Game Content may
#         only be Used under and in terms of this License. You must
#         affix such a notice to any Open Game Content that you Use. No
#         terms may be added to or subtracted from this License except
#         as described by the License itself. No other terms or
#         conditions may be applied to any Open Game Content distributed
#         using this License.
#     Offer and Acceptance: By Using the Open Game Content You indicate
#         Your acceptance of the terms of this License.
#     Grant and Consideration: In consideration for agreeing to use this
#         License, the Contributors grant You a perpetual, worldwide,
#         royalty-free, non-exclusive license with the exact terms of
#         this License to Use, the Open Game Content.
#     Representation of Authority to Contribute: If You are contributing
#         original material as Open Game Content, You represent that
#         Your Contributions are Your original creation and/or You have
#         sufficient rights to grant the rights conveyed by this License.
#     Notice of License Copyright: You must update the COPYRIGHT NOTICE
#         portion of this License to include the exact text of the
#         COPYRIGHT NOTICE of any Open Game Content You are copying,
#         modifying or distributing, and You must add the title, the
#         copyright date, and the copyright holder’s name to the
#         COPYRIGHT NOTICE of any original Open Game Content you
#         Distribute.
#     Use of Product Identity: You agree not to Use any Product
#         Identity, including as an indication as to compatibility,
#         except as expressly licensed in another, independent Agreement
#         with the owner of each element of that Product Identity. You
#         agree not to indicate compatibility or co-adaptability with
#         any Trademark or Registered Trademark in conjunction with a
#         work containing Open Game Content except as expressly licensed
#         in another, independent Agreement with the owner of such
#         Trademark or Registered Trademark. The use of any Product
#         Identity in Open Game Content does not constitute a challenge
#         to the ownership of that Product Identity. The owner of any
#         Product Identity used in Open Game Content shall retain all
#         rights, title and interest in and to that Product Identity.
#     Identification: If you distribute Open Game Content You must
#         clearly indicate which portions of the work that you are
#         distributing are Open Game Content.
#     Updating the License: Wizards or its designated Agents may publish
#         updated versions of this License. You may use any authorized
#         version of this License to copy, modify and distribute any
#         Open Game Content originally distributed under any version of
#         this License.
#     Copy of this License: You MUST include a copy of this License with
#         every copy of the Open Game Content You Distribute.
#     Use of Contributor Credits: You may not market or advertise the
#         Open Game Content using the name of any Contributor unless You
#         have written permission from the Contributor to do so.
#     Inability to Comply: If it is impossible for You to comply with
#         any of the terms of this License with respect to some or all
#         of the Open Game Content due to statute, judicial order, or
#         governmental regulation then You may not Use any Open Game
#         Material so affected.
#     Termination: This License will terminate automatically if You fail
#         to comply with all terms herein and fail to cure such breach
#         within 30 days of becoming aware of the breach. All
#         sublicenses shall survive the termination of this License.
#     Reformation: If any provision of this License is held to be
#         unenforceable, such provision shall be reformed only to the
#         extent necessary to make it enforceable.
#     COPYRIGHT NOTICE
#
#     Open Game License v 1.0a Copyright 2000, Wizards of the Coast, Inc.
#
#     System Reference Document Copyright 2000-2003, Wizards of the Coast, Inc.;
#     Authors Jonathan Tweet, Monte Cook, Skip Williams, Rich Baker,
#     Andy Collins, David Noonan, Rich Redman, Bruce R. Cordell,
#     John D. Rateliff, Thomas Reid, James Wyatt, based on original
#     material by E. Gary Gygax and Dave Arneson.
#
#     Creature Collection Volume 1 Copyright 2000, Clark Peterson.
#
#     Modern System Reference Document Copyright 2002, Wizards of the Coast, Inc.;
#     Authors Bill Slavicsek, Jeff Grubb, Rich Redman, Charles Ryan,
#     based on material by Jonathan Tweet, Monte Cook, Skip Williams,
#     Richard Baker,Peter Adkison, Bruce R. Cordell, John Tynes,
#     Andy Collins, and JD Wiker
#
#     Monster Manual II Copyright 2002, Wizards of the Coast, Inc.
#
#     Swords of Our Fathers Copyright 2003, The Game Mechanics.
#
#     Mutants & Masterminds Copyright 2002, Green Ronin Publishing.
#
#     Unearthed Arcana Copyright 2004, Wizards of the Coast, Inc.;
#     Andy Collins, Jesse Decker, David Noonan, Rich Redman.
#
#     The Hypertext d20 SRD Copyright 2004, Jans W Carton; transferred
#     to BoLS Interactive, 2016.
#
#     daydream Copyright 2019, Anthony Harrison
#
# END OF LICENSE
"""Classes and helper function for working with numerical values."""

__all__ = ['ordinal', 'Die', 'DicePool', 'ModifierType', 'Modifier',
           'ModifierCombinationError', 'DifferentModifierTypesError',
           'BonusAndPenaltyCombinationError', 'DifferentConditionsError',
           'Modifier', 'ModifierTotal']

from typing import Tuple, List, Any, Union, DefaultDict, Dict, Optional, \
    overload, Iterator
from copy import deepcopy
from collections import defaultdict
from itertools import chain
from functools import total_ordering
from dataclasses import dataclass

import defn.core as core


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
def ordinal(value: int) -> str:  # pylint: disable=unused-argument
    """Convert an integer to an ordinal string."""
    ...


@overload
def ordinal(value: str) -> int:  # pylint: disable=unused-argument, function-redefined, line-too-long
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
                    result = type(self)(max(self.value, other.value),
                                        self.type)
                elif self.is_penalty and other.is_penalty:
                    result = type(self)(min(self.value, other.value),
                                        self.type)
                else:
                    raise BonusAndPenaltyCombinationError(
                        f'Combining a bonus and a penalty loses information: '
                        f'{self.value:+} and {other.value:+}'
                    )
        else:
            result = NotImplemented
        return result

    def __mul__(self, other: Any) -> Union['Modifier', 'NotImplemented']:
        if isinstance(other, int):
            result = type(self)(self.value * other, self.type, self.condition)
        else:
            result = NotImplemented
        return result

    __rmul__ = __mul__

    def __neg__(self) -> 'Modifier':
        return type(self)(-self.value, self.type, self.condition)

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

    def __int__(self) -> int:
        return self.value


_ModifierKey = Tuple[ModifierType, bool, Optional[core.Condition]]


def _key(modifier: Modifier) -> _ModifierKey:
    return (modifier.type,
            modifier.type.stacks or modifier.is_bonus,
            modifier.condition)


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
            key = _key(mod)
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

    def __add__(self, other: Any) -> Union['ModifierTotal', 'NotImplemented']:
        if isinstance(other, ModifierTotal):
            # pylint: disable=protected-access
            result = type(self)(*self._modifiers.values(),
                                *other._modifiers.values())
        elif isinstance(other, Modifier):
            result = type(self)(other, *self._modifiers.values())
        else:
            result = NotImplemented
        return result

    __radd__ = __add__


class Progression:
    """A progression of modifiers.

    :param modifier_name: name of modifier in progression, defines
        modifier type
    :param values: the values of the modifiers in the the progression
    """

    def __init__(self, modifier_type: ModifierType, *values: int) -> None:
        self._modifiers = [Modifier(v, modifier_type)
                           for v in values]

    def __repr__(self) -> str:
        values = ', '.join(str(int(m)) for m in self._modifiers)
        if values:
            modifier_type = repr(self._modifiers[0].type)
            values = ', ' + values
        else:
            modifier_type = ''
        return type(self).__name__ + f"({modifier_type}{values})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Progression):
            # pylint: disable=protected-access
            result = self._modifiers == other._modifiers
        else:
            result = NotImplemented
        return result

    def __len__(self) -> int:
        return len(self._modifiers)

    def __getitem__(self, item: int) -> Modifier:
        return self._modifiers[item]

    def __iter__(self) -> Iterator[Modifier]:
        return iter(self._modifiers)