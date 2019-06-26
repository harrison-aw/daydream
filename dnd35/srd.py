"""Definitions from the SRD."""

# pylint: disable-msg=C0103

import dnd35.concepts as concepts


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


# Special
darkvision = concepts.Special('Darkvision')
stonecunning = concepts.Special('Stonecunning',
                                search=concepts.Bonus('+2 racial bonus to notice unusual stonework'))
stability = concepts.Special('Stability',
                             STR=concepts.Bonus('+4 on ability checks to resist being bull rushed or tripped when standing on the ground'))
low_light_vision = concepts.Special('Low-Light Vision')


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
    weapon_familiarity=concepts.Special('Weapon Familiarity'),
    stability=stability,
    saving_throws=concepts.Bonus('+2 racial bonus on saving throws against poison.',
                                 '+2 racial bonus on saving throws against spells and spell-like effects.'),
    attack_bonus=concepts.Bonus('+1 racial bonus on attack rolls against orcs and goblinoids.'),
    armor_class=concepts.Bonus('+4 dodge bonus to Armor Class against monsters of the giant type.'),
    appraise=concepts.Bonus('+2 racial bonus on Appraise checks that are related to stone or metal items.'),
    craft=concepts.Bonus('+2 racial bonus on Craft checks that are related to stone or metal.'),
    languages=['Common', 'Dwarven'],
    bonus_languages=['Giant', 'Gnome', 'Goblin', 'Orc', 'Terran', 'Undercommon'],
    favored_class='Fighter',
)
elf = concepts.Race(
    name='Elf',
    size=medium,
    speed=30,
    fortitude=concepts.Bonus('Immunity to magic sleep effects',
                             '+2 racial saving throw bonus against enchantment spells or effects.'),
    reflex=concepts.Bonus('Immunity to magic sleep effects',
                          '+2 racial saving throw bonus against enchantment spells or effects.'),
    will=concepts.Bonus('Immunity to magic sleep effects',
                        '+2 racial saving throw bonus against enchantment spells or effects.'),
    low_light_vision=low_light_vision,
    feats=[
        'Martial Weapon (longsword)',
        'Martial Weapon (rapier)',
        'Martial Weapon (longbow)',
        'Martial Weapon (shortbow)',
    ],
    listen=concepts.Bonus(racial=+2),
    search=concepts.Bonus(racial=+2),
    spot=concepts.Bonus(racial=+2),
    languages=['Common', 'Elven'],
    bonus_languages=['Draconic', 'Gnoll', 'Gnome', 'Goblin', 'Orc',
                     'Sylvan'],
    favored_class='Wizard',
)