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
"""Implements basic concepts used in game rules."""

__all__ = ['Size', 'AbilityScore', 'AbilityType',
           'Ability', 'Synergy', 'Skill', 'Feat', 'Class', 'Character']

from dataclasses import dataclass, field
from typing import Any, Optional, SupportsInt, Set, Union, Tuple

import defn.core as core
import defn.numbers as num


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


class Synergy(core.Reference):
    """Implements skill synergies in 3.5e.

    :param name: name of the referenced attribute
    :param target: type or name of the object with the referenced
        attribute
    :param modifier: this is added to the dereferenced value
    :param condition: condition for synergy bonus to apply
    """

    def __init__(self,
                 name: str,
                 target: Union[type, str] = 'Character',
                 modifier: Any = None,
                 condition: Optional[num.Condition] = None) -> None:
        super().__init__(name, target, modifier)
        self._condition = condition

    def __repr__(self) -> str:
        return (type(self).__name__
                + f'({repr(self._name)}, {self._type_name()}, '
                + f'{repr(self._modifier)}, {repr(self._condition)})')

    def _dereference_name(self, instance):
        if self._refers_to(instance):
            result = getattr(instance, self._name)
            try:
                if result >= 5:
                    if self._condition is None:
                        result = num.Modifier(2)
                    else:
                        result = num.Modifier(2, condition=self._condition)
                else:
                    result = num.Modifier(0)
            except TypeError:
                pass
        else:
            result = self
        return result


class _BaseSkill:
    @property
    def ranks(self) -> int:
        """Number of ranks invested in skill."""
        return self._ranks

    @property
    def modifier(self) -> core.Reference:
        """Modifier for rolls related to this skill."""
        return self._skill.key_ability + num.Modifier(self.ranks)

    def __init__(self, ranks: int) -> None:
        self._ranks = ranks

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, *, skill: 'Skill') -> None:
        super().__init_subclass__()
        cls._skill = skill

        setattr(cls, skill.key_ability.name, skill.key_ability)
        for synergy in skill.synergies:
            setattr(cls, synergy.name, synergy)

    def __repr__(self) -> str:
        return type(self).__name__ + f'({self._ranks})'

    _skill: 'Skill'


@dataclass(frozen=True)
class Skill:
    # noinspection PyUnresolvedReferences
    """A skill for a character in 3.5e.

    :param name: name of skill
    :param key_ability: Ability score that modifies the skill
    :param trained_only: If True, skill is only usable if ranks have
        been invested
    :param armor_check_penalty: If True, skill is penalized by wearing
        heavy armor
    :param synergies: References to skills that are increased if at
        least 5 ranks are invested in this skill
    """

    name: str
    key_ability: core.Reference
    trained_only: bool = False
    armor_check_penalty: bool = False
    synergies: Tuple[Synergy, ...] = field(default_factory=tuple)

    def __call__(self, ranks: int) -> _BaseSkill:
        # noinspection PyArgumentList,PyTypeChecker,PyUnresolvedReferences
        class_ = type(self._class_name(),  # type: ignore[call-overload]
                      (_BaseSkill,),
                      {},
                      skill=self)
        instance: _BaseSkill = class_(ranks)
        return instance

    def _class_name(self) -> str:
        return self.name.title()\
            .replace(' ', '')\
            .replace('(', '')\
            .replace(')', '')


@dataclass(frozen=True)
class Feat:
    # noinspection PyUnresolvedReferences
    """Represents a feat in 3.5e.

    :param name: name of feat
    :param type: type of feat
    :param fighter_feat: if True, will be available for a fighter to
        select as a bonus feat.
    """

    name: str
    type: str = 'General'
    fighter_feat: bool = False


class Class:
    """Represents a character class in 3.5e."""

    def __init__(self, name, bab, fort, ref, will, special, **other):
        self._name = name
        self._bab = bab
        self._fort = fort
        self._ref = ref
        self._will = will
        self._special = special
        self._other = tuple(other)
        for other_name, value in other.items():
            setattr(self, '_' + other_name, value)


class Character(core.Aggregator):
    """Represents a character in 3.5e."""
