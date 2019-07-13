"""Definitions from the SRD."""

# pylint: disable-msg=C0103

import dnd35.concepts as concepts


# Dice
d3 = concepts.Dice(3)
d4 = concepts.Dice(4)
d6 = concepts.Dice(6)
d8 = concepts.Dice(8)
d10 = concepts.Dice(10)
d12 = concepts.Dice(12)
d20 = concepts.Dice(20)


# Progressions
good_base_save = concepts.Progression(
    'base save',
    2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12,
)
poor_base_save = concepts.Progression(
    'base save',
    0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6,
)


# Sizes
fine = concepts.Size(+8)
diminutive = concepts.Size(+4)
tiny = concepts.Size(+2)
small = concepts.Size(+1)
medium = concepts.Size(+0)
large = concepts.Size(-1)
huge = concepts.Size(-2)
gargantuan = concepts.Size(-4)
colossal = concepts.Size(-8)


# Abilities
darkvision = concepts.Ability('Darkvision')
stonecunning = concepts.Ability(
    'Stonecunning',
    search=concepts.Modifier('+2 racial bonus to notice unusual '
                             'stonework')
)
stability = concepts.Ability(
    'Stability',
    STR=concepts.Modifier('+4 on ability checks to resist being bull '
                          'rushed or tripped when standing on the ground'))
low_light_vision = concepts.Ability('Low-Light Vision')


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
