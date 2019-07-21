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

"""Definitions from the SRD."""

# pylint: disable=invalid-name

import dnd35e.concepts as concepts
import dnd35e.numbers as numbers


# Dice
d3 = numbers.Die(3)
d4 = numbers.Die(4)
d6 = numbers.Die(6)
d8 = numbers.Die(8)
d10 = numbers.Die(10)
d12 = numbers.Die(12)
d20 = numbers.Die(20)


# Base saving throw progressions
good_base_save = concepts.Progression(
    'base save',
    2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12,
)
poor_base_save = concepts.Progression(
    'base save',
    0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6,
)


# Base attack bonus progressions
good_base_attack_bonus = concepts.Progression(
    'base attack',
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
)
average_base_attack_bonus = concepts.Progression(
    'base attack',
    0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14, 15,
)
poor_base_attack_bonus = concepts.Progression(
    'base attack',
    0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
)


# Sizes
fine = concepts.Size('Fine', +8)
diminutive = concepts.Size('Diminutive', +4)
tiny = concepts.Size('Tiny', +2)
small = concepts.Size('Small', +1)
medium = concepts.Size('Medium', +0)
large = concepts.Size('Large', -1)
huge = concepts.Size('Huge', -2)
gargantuan = concepts.Size('Gargantuan', -4)
colossal = concepts.Size('Colossal', -8)


# Abilities
darkvision = concepts.Ability('Darkvision')
low_light_vision = concepts.Ability('Low-Light Vision')

stonecunning = concepts.Ability(
    'Stonecunning',
    search=concepts.Modifier(
        '+2 racial bonus to notice unusual stonework'
    )
)
stability = concepts.Ability(
    'Stability',
    STR=concepts.Modifier(
        '+4 on ability checks to resist being bull rushed or tripped '
        'when standing on the ground'
    )
)


# Races
human = concepts.Race(
    name='Human',
    size=medium,
    speed=30,
    number_of_feats=1,
    skill_points_per_level=1,
    languages=['Common'],
    bonus_languages=None,
    favored_class=None,
)
dwarf = concepts.Race(
    name='Dwarf',
    constitution=+2,
    charisma=-2,
    size=medium,
    speed=20,
    darkvision=darkvision,
    stonecunning=stonecunning,
    weapon_familiarity=concepts.Ability('Weapon Familiarity'),
    stability=stability,
    saving_throws=concepts.Modifier('+2 racial bonus on saving throws '
                                    'against poison.',
                                    '+2 racial bonus on saving throws '
                                    'against spells and spell-like effects.'),
    attack_bonus=concepts.Modifier('+1 racial bonus on attack rolls '
                                   'against orcs and goblinoids.'),
    armor_class=concepts.Modifier('+4 dodge bonus to Armor Class against '
                                  'monsters of the giant type.'),
    appraise=concepts.Modifier('+2 racial bonus on Appraise checks that '
                               'are related to stone or metal items.'),
    craft=concepts.Modifier('+2 racial bonus on Craft checks that are '
                            'related to stone or metal.'),
    languages=['Common', 'Dwarven'],
    bonus_languages=['Giant', 'Gnome', 'Goblin', 'Orc', 'Terran', 'Undercommon'],
    favored_class='Fighter',
)
elf = concepts.Race(
    name='Elf',
    size=medium,
    speed=30,
    fortitude=concepts.Modifier('Immunity to magic sleep effects',
                                '+2 racial saving throw bonus against '
                                'enchantment spells or effects.'),
    reflex=concepts.Modifier('Immunity to magic sleep effects',
                             '+2 racial saving throw bonus against '
                             'enchantment spells or effects.'),
    will=concepts.Modifier('Immunity to magic sleep effects',
                           '+2 racial saving throw bonus against '
                           'enchantment spells or effects.'),
    low_light_vision=low_light_vision,
    feats=[
        'Martial Weapon (longsword)',
        'Martial Weapon (rapier)',
        'Martial Weapon (longbow)',
        'Martial Weapon (shortbow)',
    ],
    listen=concepts.Modifier(racial=+2),
    search=concepts.Modifier(racial=+2),
    spot=concepts.Modifier(racial=+2),
    languages=['Common', 'Elven'],
    bonus_languages=['Draconic', 'Gnoll', 'Gnome', 'Goblin', 'Orc',
                     'Sylvan'],
    favored_class='Wizard',
)
