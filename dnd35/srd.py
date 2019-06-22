"""Definitions from the SRD."""

from .concepts import Conditional, Size, Entity, any_

# Sizes
fine = Size(+8)
diminutive = Size(+4)
tiny = Size(+2)
small = Size(+1)
medium = Size(+0)
large = Size(-1)
huge = Size(-2)
gargantuan = Size(-4)
colossal = Size(-8)


# Races
human = Entity(name='Human',
               speed=30,
               number_of_feats=1,
               skill_points=4,
               skill_points_per_level=1,
               language=['Common'], bonus_languages=[any_],
               favored_class=any_)
dwarf = Entity(name='Dwarf',
               constitution=+2,
               charisma=-2,
               size=medium,
               speed=20,
               special_abilities=['Darkvision',
                                  'Stonecunning',
                                  'Weapon Familiarity',
                                  'Stability',
                                  '+2 racial bonus on saving throws against poison.',
                                  '+2 racial bonus on saving throws against spells and spell-like effects.'],
               attack_bonus=Conditional(0, '+1 racial bonus on attack rolls against orcs and goblinoids.'),
               armor_class=Conditional(0, '+4 dodge bonus to Armor Class against monsters of the giant type.'),
               appraise=Conditional(0, '+2 racial bonus on Appraise checks that are related to stone or metal items.'),
               craft=Conditional(0, '+2 racial bonus on Craft checks that are related to stone or metal.'),
               languages=['Common', 'Dwarven'],
               bonus_languages=['Giant', 'Gnome', 'Goblin', 'Orc', 'Terran', 'Undercommon'],
               favored_class='Fighter')
elf = Entity(name='Elf',
             size=medium,
             speed=30,
             special_abilities=['Immunity to magic sleep effects',
                                '+2 racial saving throw bonus against enchantment spells or effects.',
                                'Low-Light Vision'],
             feats=['Martial Weapon (longsword)',
                    'Martial Weapon (rapier)',
                    'Martial Weapon (longbow)',
                    'Martial Weapon (shortbow)'],
             listen=+2,
             search=+2,
             spot=+2,
             languages=['Common', 'Elven'],
             bonus_languages=['Draconic', 'Gnoll', 'Gnome', 'Goblin', 'Orc', 'Sylvan'],
             favored_class='Wizard')
