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

import dnd35e.concepts as concepts
import dnd35e.core as core
import dnd35e.numbers as num

# References
STR = core.Reference('STR', 'Character')
DEX = core.Reference('DEX', 'Character')
CON = core.Reference('CON', 'Character')
INT = core.Reference('INT', 'Character')
WIS = core.Reference('WIS', 'Character')
CHA = core.Reference('CHA', 'Character')


# Dice
D3 = num.Die(3)
D4 = num.Die(4)
D6 = num.Die(6)
D8 = num.Die(8)
D10 = num.Die(10)
D12 = num.Die(12)
D20 = num.Die(20)


# Modifier Types
UNTYPED = num.ModifierType('untyped', stacks=True)
ABILITY = num.ModifierType('ability')
ALCHEMICAL = num.ModifierType('alchemical')
ARMOR = num.ModifierType('armor')
CIRCUMSTANCE = num.ModifierType('circumstance')
COMPETENCE = num.ModifierType('competence')
DEFLECTION = num.ModifierType('deflection')
DODGE = num.ModifierType('dodge', stacks=True)
ENHANCEMENT = num.ModifierType('enhancement')
INSIGHT = num.ModifierType('insight')
LUCK = num.ModifierType('luck')
MORALE = num.ModifierType('morale')
NATURAL_ARMOR = num.ModifierType('natural armor')
PROFANE = num.ModifierType('profane')
RACIAL = num.ModifierType('racial')
RESISTANCE = num.ModifierType('resistance')
SACRED = num.ModifierType('sacred')
SHIELD = num.ModifierType('shield')
SIZE = num.ModifierType('size')
BASE_SAVE = num.ModifierType('base save')
BASE_ATTACK = num.ModifierType('base attack')


# Base saving throw progressions
GOOD_BASE_SAVE = concepts.Progression(
    BASE_SAVE,
    2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12,
)
POOR_BASE_SAVE = concepts.Progression(
    BASE_SAVE,
    0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6,
)


# Base attack bonus progressions
GOOD_BASE_ATTACK = concepts.Progression(
    BASE_ATTACK,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
)
AVERAGE_BASE_ATTACK = concepts.Progression(
    BASE_ATTACK,
    0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14, 15,
)
POOR_BASE_ATTACK = concepts.Progression(
    BASE_ATTACK,
    0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
)


# Sizes
FINE = concepts.Size('Fine', +8)
DIMINUTIVE = concepts.Size('Diminutive', +4)
TINY = concepts.Size('Tiny', +2)
SMALL = concepts.Size('Small', +1)
MEDIUM = concepts.Size('Medium', +0)
LARGE = concepts.Size('Large', -1)
HUGE = concepts.Size('Huge', -2)
GARGANTUAN = concepts.Size('Gargantuan', -4)
COLOSSAL = concepts.Size('Colossal', -8)


# Abilities
DARKVISION = concepts.Ability('Darkvision')
LOW_LIGHT_VISION = concepts.Ability('Low-Light Vision')

STONECUNNING = concepts.Ability(
    'Stonecunning',
    search=num.Modifier(+2,
                        RACIAL,
                        core.Condition('to notice unusual stonework')),
)
STABILITY = concepts.Ability(
    'Stability',
    STR=num.Modifier(+4,
                     UNTYPED,
                     core.Condition('to resist being bull rushed or tripped '
                                    'when standing on the ground')),
)
FAST_MOVEMENT = concepts.Ability('Fast movement')
ILLITERACY = concepts.Ability('Illiteracy')
RAGE = concepts.Ability


# Skills
APPRAISE = concepts.Skill('Appraise', INT)
BALANCE = concepts.Skill('Balance', DEX,
                         armor_check_penalty=True)
BLUFF = concepts.Skill('Bluff', CHA,
                       synergies=(concepts.Synergy('diplomacy'),
                                  concepts.Synergy('intimidate'),
                                  concepts.Synergy('sleight_of_hand')))
CLIMB = concepts.Skill('Climb', STR,
                       armor_check_penalty=True)
CONCENTRATION = concepts.Skill('Concentration', CON)
CRAFT_ALCHEMY = concepts.Skill('Craft (alchemy)', INT,
                               synergies=(concepts.Synergy(
                                   'Appraise',
                                   condition=core.Condition(
                                       'on checks related to alchemy')),))
KNOWLEDGE_ARCANA = concepts.Skill('Knowledge (arcana)', INT,
                                  trained_only=True,
                                  synergies=(concepts.Synergy('Spellcraft'),))


# Feats
ALERTNESS = concepts.Feat('Alertness')


# Classes
BARBARIAN = concepts.Class('Barbarian',
                           GOOD_BASE_ATTACK,
                           GOOD_BASE_SAVE,
                           POOR_BASE_SAVE,
                           POOR_BASE_SAVE,
                           [])
