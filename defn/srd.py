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
"""Definitions from the SRD."""

import defn.concepts as concepts
import defn.core as core
import defn.numbers
import defn.numbers as num

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
GOOD_BASE_SAVE = defn.numbers.Progression(
    BASE_SAVE,
    2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12,
)
POOR_BASE_SAVE = defn.numbers.Progression(
    BASE_SAVE,
    0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6,
)


# Base attack bonus progressions
GOOD_BASE_ATTACK = defn.numbers.Progression(
    BASE_ATTACK,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
)
AVERAGE_BASE_ATTACK = defn.numbers.Progression(
    BASE_ATTACK,
    0, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11, 12, 12, 13, 14, 15,
)
POOR_BASE_ATTACK = defn.numbers.Progression(
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
