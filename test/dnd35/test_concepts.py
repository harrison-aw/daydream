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

import dnd35e.concepts as concepts
import dnd35e.numbers as numbers


class TestModifier:
    def test_handles_simple_init(self):
        modifier = concepts.Modifier(unnamed=10)
        assert modifier == 10

    def test_handles_conditional(self):
        modifier = concepts.Modifier('+1 racial bonus on attack rolls '
                                     'against orcs and goblinoids.')
        assert modifier == 0
        assert str(modifier) == '+1 racial bonus on attack rolls ' \
                                'against orcs and goblinoids.'

    def test_repr_is_readable(self):
        modifier = concepts.Modifier(unnamed=10)
        assert repr(modifier) == 'Modifier(unnamed=10)'

    def test_repr_is_evaluable(self):
        modifier = concepts.Modifier('test conditional', racial=10)
        repr_ = repr(modifier)
        modifier_evaluated = eval(repr_, {'Modifier': concepts.Modifier})
        assert modifier == modifier_evaluated

    def test_undefined_typed_bonuses_return_zero(self):
        modifier = concepts.Modifier(dodge=3)
        assert modifier['wrong'] == 0

    def test_adding_bonuses(self):
        modifier1 = concepts.Modifier('+1 test', '+1 too',
                                      unnamed=3, dodge=2, racial=3)
        modifier2 = concepts.Modifier('+1 test',
                                      unnamed=1, dodge=2, racial=2)

        sum_ = modifier1 + modifier2

        desired = concepts.Modifier('+1 test', '+1 too',
                                    unnamed=4, dodge=4, racial=3)
        assert sum_ == desired

    def test_bonus_string(self):
        modifier = concepts.Modifier(dodge=3)
        assert str(modifier) == '+3'

    def test_conditional_string(self):
        modifier = concepts.Modifier('+1 if blind', racial=1)
        assert str(modifier) == '+1\n+1 if blind'

    def test_iteration(self):
        modifier = concepts.Modifier('+1 test', '+1 too',
                                     unnamed=3, dodge=2, racial=3)
        assert set(modifier) == {'unnamed', 'dodge', 'racial'}


class TestProgression:
    def test_create_save(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        assert good_save[2] == concepts.Modifier(save=3)

    def test_repr_evaluates(self):
        good_save = concepts.Progression('save', 2, 3, 3, 4, 4)
        good_save_copy = eval(repr(good_save),
                              {'Progression': concepts.Progression})
        assert good_save == good_save_copy


class TestSize:
    def test_repr_is_evaluable(self):
        small = concepts.Size('Small', -1)
        assert eval(repr(small), {'Size': concepts.Size}) == small

    def test_small_attack_bonus(self):
        small = concepts.Size('Small', -1)
        assert small.attack_bonus == 1

    def test_small_armor_class(self):
        small = concepts.Size('Small', -1)
        assert small.armor_class == 1

    def test_small_grapple(self):
        small = concepts.Size('Small', -1)
        assert small.grapple == -4

    def test_small_hide(self):
        small = concepts.Size('Small', -1)
        assert small.hide == 4


class TestAbilityScore:
    def test_positive_modifier(self):
        score = concepts.AbilityScore(17)
        assert score.modifier == 3

    def test_negative_modifier(self):
        score = concepts.AbilityScore(7)
        assert score.modifier == -2


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
            search=concepts.Modifier('+2 racial bonus to notice '
                                     'unusual stonework')
        )
        assert str(stonecunning.search) == '+2 racial bonus to notice' \
                                           ' unusual stonework'

    def test_sneak_attack(self):
        sneak_attack = concepts.Ability(
            'Sneak attack +1d6',
            damage=numbers.DicePool(d6=1)
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
                                   damage=numbers.DicePool(d6=1)),
            third=concepts.Ability('Sneak attack +2d6', None, '',
                                   damage=numbers.DicePool(d6=2)),
        )
        assert str(sneak_attack[4]) == 'Sneak attack +2d6'


class TestClass:
    def test_rogue(self):
        sneak_attack = concepts.ClassFeature(
            'Sneak attack',
            first=concepts.Ability('Sneak attack +1d6',
                                   damage=numbers.DicePool(d6=1)),
            third=concepts.Ability('Sneak attack +2d6',
                                   damage=numbers.DicePool(d6=2)),
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
            numbers.Die(6),
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
