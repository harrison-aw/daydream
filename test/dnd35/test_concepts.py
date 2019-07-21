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

# pylint: disable=W,C,R

import dnd35e.core as core
import dnd35e.concepts as concepts
import dnd35e.numbers as num


class TestProgression:
    def test_create_save(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        assert good_save[2] == num.Modifier(3, num.ModifierType('save'))

    def test_repr_evaluates(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        assert (eval(repr(good_save), {'Progression': concepts.Progression})
                == good_save)


class TestSize:
    def test_repr_is_evaluable(self):
        small = concepts.Size('Small', -1)
        assert eval(repr(small), {'Size': concepts.Size}) == small

    def test_small_attack_bonus(self):
        small = concepts.Size('Small', -1)
        assert small.attack_bonus == num.Modifier(1, concepts.Size.modifier_type)

    def test_small_armor_class(self):
        small = concepts.Size('Small', -1)
        assert small.armor_class == num.Modifier(1, concepts.Size.modifier_type)

    def test_small_grapple(self):
        small = concepts.Size('Small', -1)
        assert small.grapple == num.Modifier(-4, concepts.Size.modifier_type)

    def test_small_hide(self):
        small = concepts.Size('Small', -1)
        assert small.hide == num.Modifier(4, concepts.Size.modifier_type)


class TestAbilityScore:
    def test_positive_modifier(self):
        score = concepts.AbilityScore(17)
        assert score.modifier == num.Modifier(3, concepts.AbilityScore.modifier_type)

    def test_negative_modifier(self):
        score = concepts.AbilityScore(7)
        assert score.modifier == num.Modifier(-2, concepts.AbilityScore.modifier_type)


class TestAbilityType:
    def test_repr_evaluates(self):
        ability = concepts.AbilityType('Supernatural', 'Su')
        ability_copy = eval(repr(ability),
                            {'AbilityType': concepts.AbilityType})
        assert ability == ability_copy

    def test_str(self):
        ability = concepts.AbilityType('Supernatural', 'Su')
        assert str(ability) == 'Supernatural (Su)'


class TestAbility:
    def test_static_ability(self):
        stonecunning = concepts.Ability(
            'Stonecunning',
            search=num.Modifier(2,
                                num.ModifierType('racial'),
                                core.Condition('to notice unusual stonework'))
        )
        assert str(stonecunning.search) == '+2 racial bonus to notice' \
                                           ' unusual stonework'

    def test_sneak_attack(self):
        sneak_attack = concepts.Ability(
            'Sneak attack +1d6',
            damage=num.DicePool(d6=1)
        )
        assert str(sneak_attack) == 'Sneak attack +1d6'

    def test_delete_features(self):
        ability = concepts.Ability('Test', test=10)

        assert ability.test == 10
        del ability.test
        assert ability == concepts.Ability('Test')


class TestClassFeature:
    def test_sneak_attack(self):
        sneak_attack = concepts.ClassFeature(
            'Sneak attack',
            first=concepts.Ability('Sneak attack +1d6', None, '',
                                   damage=num.DicePool(d6=1)),
            third=concepts.Ability('Sneak attack +2d6', None, '',
                                   damage=num.DicePool(d6=2)),
        )
        assert str(sneak_attack[4]) == 'Sneak attack +2d6'


class TestClass:
    def test_rogue(self):
        sneak_attack = concepts.ClassFeature(
            'Sneak attack',
            first=concepts.Ability('Sneak attack +1d6',
                                   damage=num.DicePool(d6=1)),
            third=concepts.Ability('Sneak attack +2d6',
                                   damage=num.DicePool(d6=2)),
        )
        trapfinding = concepts.ClassFeature('Trapfinding', '')
        evasion = concepts.ClassFeature(
            'Evasion',
            second=concepts.Ability('Evasion')
        )
        trap_sense = concepts.ClassFeature(
            'Trap sense',
            third=concepts.Ability('Trap sense +1'),
        )
        average_bab = concepts.Progression('base attack bonus', 0, 1, 2)
        bad_save = concepts.Progression('save', 0, 0, 1)
        good_save = concepts.Progression('save', 2, 3, 3)
        rogue = concepts.Class(
            None,
            num.Die(6),
            [],
            8,
            average_bab,
            bad_save,
            good_save,
            bad_save,
            sneak_attack,
            trapfinding,
            evasion,
            trap_sense,
        )
        print(rogue)
