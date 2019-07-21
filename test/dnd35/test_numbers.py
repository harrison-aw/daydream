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
"""Unit testing for numbers module."""

import pytest

import dnd35.core as core
import dnd35.numbers as num


# pylint: disable=no-self-use, eval-used


class TestDie:
    """Tests for the Die class."""

    def test_repr_evaluates(self):
        """Ensure that the repr can evaluate."""
        die = num.Die(6)
        assert eval(repr(die), {'Die': num.Die}) == die

    def test_str(self):
        """Ensure that the string representation is correct."""
        die = num.Die(6)
        assert str(die) == 'd6'

    def test_from_string(self):
        """Ensure that die strings are properly built."""
        die = num.Die.from_string('d6')
        assert die == num.Die(6)

    def test_string_conversion_identity(self):
        """Ensure that the strings returned and consumed work the same."""
        die = num.Die(6)
        die_string = 'd6'
        assert (num.Die.from_string(str(die)) == die
                and str(num.Die.from_string(die_string)) == die_string)

    def test_bad_string_prefix(self):
        """Only accept strings that start with "d"."""
        with pytest.raises(ValueError):
            num.Die.from_string('34')

    def test_bad_string_suffix(self):
        """Only accept strings that end with an integer."""
        with pytest.raises(ValueError):
            num.Die.from_string('d1.1')

    def test_hashable(self):
        """Ensure that the object is hashable."""
        die1 = num.Die(6)
        die2 = num.Die(6)
        assert die1 == die2 and hash(die1) == hash(die2)

    def test_average(self):
        """Ensure that the average is correctly computed."""
        die = num.Die(6)
        assert die.average == 3.5


class TestDicePool:
    """Tests for DicePool."""

    def test_repr_evaluates(self):
        """Ensure that the repr can evaluate."""
        dice_pool = num.DicePool(d6=1, d8=4)
        assert (eval(repr(dice_pool), {'DicePool': num.DicePool})
                == dice_pool)

    def test_equals_with_zero_counts(self):
        """Ensure that equality ignores dice with zero counts."""
        dice_pool1 = num.DicePool(d6=1, d8=4, d10=0)
        dice_pool2 = num.DicePool(d6=1, d8=4)
        assert dice_pool1 == dice_pool2

    def test_average_of_pool(self):
        """Ensure that the average of a dice pool is correct."""
        dice_pool = num.DicePool(d6=1, d8=4)
        assert dice_pool.average == 21.5

    def test_add_pools(self):
        """Ensure that two dice pools are added correctly"""
        dice_pool1 = num.DicePool(d6=1, d8=4)
        dice_pool2 = num.DicePool(d4=2, d6=2)
        assert dice_pool1 + dice_pool2 == num.DicePool(d4=2, d6=3, d8=4)

    def test_add_pool_and_die(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = num.DicePool(d6=1, d8=4)
        die = num.Die(6)
        assert dice_pool + die == num.DicePool(d6=2, d8=4)

    def test_add_die_and_pool(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = num.DicePool(d6=1, d8=4)
        die = num.Die(6)
        assert die + dice_pool == num.DicePool(d6=2, d8=4)


class TestModifier:
    """Tests for the Modifier class."""

    def test_repr_evaluates(self):
        """Ensure that a repr can recreate an instance."""
        mod = num.Modifier(4)
        namespace = {'Modifier': num.Modifier,
                     'ModifierType': num.ModifierType}
        assert eval(repr(mod), namespace) == mod

    def test_str(self):
        """Ensure that the string representation is as expected."""
        mod_positive = num.Modifier(0)
        mod_negative = num.Modifier(-2)
        assert ((str(mod_positive), str(mod_negative))
                == ('+0 untyped bonus', '-2 untyped penalty'))

    def test_str_with_conditional(self):
        """Ensure that a conditional modifier is represented correctly."""
        mod = num.Modifier(
            value=2,
            condition=core.Condition('to learn the spells of her chosen school')
        )
        assert (str(mod)
                == '+2 untyped bonus to learn the spells of her chosen school')

    def test_add_stackable(self):
        """Ensure that stackable modifiers are combined."""
        mod1 = num.Modifier(-2)
        mod2 = num.Modifier(3)
        assert mod1 + mod2 == num.Modifier(1)

    def test_add_unstackable_bonuses(self):
        """Ensure that unstackable modifiers only have the best bonus apply."""
        mod1 = num.Modifier(1, num.ModifierType('armor'))
        mod2 = num.Modifier(3, num.ModifierType('armor'))
        assert mod1 + mod2 == num.Modifier(3, num.ModifierType('armor'))

    def test_add_unstackable_penalties(self):
        """Ensure that unstackable modifiers only have the worst penalty apply."""
        mod1 = num.Modifier(-1, num.ModifierType('armor'))
        mod2 = num.Modifier(-3, num.ModifierType('armor'))
        assert mod1 + mod2 == num.Modifier(-3, num.ModifierType('armor'))

    def test_add_different_types(self):
        """Ensure that modifiers of different types are not added."""
        mod1 = num.Modifier(1)
        mod2 = num.Modifier(3, num.ModifierType('armor'))
        with pytest.raises(num.DifferentModifierTypesError):
            mod1 + mod2  # pylint: disable=pointless-statement

    def test_add_bonus_and_penalty(self):
        """Ensure that an unstackable bonus and penalty are not combined."""
        mod1 = num.Modifier(-2, num.ModifierType('armor'))
        mod2 = num.Modifier(3, num.ModifierType('armor'))
        with pytest.raises(num.ModifierCombinationError):
            mod1 + mod2  # pylint: disable=pointless-statement

    def test_less_than(self):
        """Ensure that less than works as expected."""
        mod1 = num.Modifier(2)
        mod2 = num.Modifier(7)
        assert mod1 < mod2

    def test_bonus(self):
        """Ensure that a bonus is properly categorized."""
        bonus = num.Modifier(4)
        assert bonus.is_bonus and not bonus.is_penalty

    def test_penalty(self):
        """Ensure that a penalty is properly categorized."""
        penalty = num.Modifier(-2)
        assert penalty.is_penalty and not penalty.is_bonus

    def test_zero_is_bonus_and_penalty(self):
        """Ensure that zero is both a bonus and a penalty."""
        zero = num.Modifier(0)
        assert zero.is_bonus and zero.is_penalty

    def test_null_modifier(self):
        """Ensure that we can create a base modifier."""
        zero = num.Modifier()
        assert zero == num.Modifier(0)


class TestModifierTotal:
    """Tests for the ModifierTotal class."""

    def test_repr_evaluates(self):
        """Ensure that the repr can be used to recreate an object"""
        static_mod = num.Modifier(3, num.ModifierType('ability'))
        conditional_mod = num.Modifier(
            value=2,
            condition=core.Condition('to learn the spells of her chosen school')
        )
        total = num.ModifierTotal(static_mod, conditional_mod)
        namespace = {'ModifierTotal': num.ModifierTotal,
                     'Modifier': num.Modifier,
                     'ModifierType': num.ModifierType,
                     'Condition': core.Condition}
        assert eval(repr(total), namespace) == total

    def test_value_of_total_with_static_modifiers(self):
        """Ensure that the value of the total is correct."""
        total = num.ModifierTotal(num.Modifier(5),
                                  num.Modifier(2, num.ModifierType('armor')))
        assert total.value() == 7

    def test_value_of_total_with_conditional_modifiers(self):
        """Ensure that the value of the total is correct."""
        static_mod = num.Modifier(3, num.ModifierType('ability'))
        conditional_mod = num.Modifier(
            value=2,
            condition=core.Condition('to learn the spells of her chosen school')
        )
        total = num.ModifierTotal(static_mod, conditional_mod)
        assert total.value(*total.conditions) == 5

    def test_add_totals(self):
        """Ensure that two modifiers are added together."""
        total1 = num.ModifierTotal(num.Modifier(5),
                                   num.Modifier(2, num.ModifierType('armor')))
        total2 = num.ModifierTotal(num.Modifier(2),
                                   num.Modifier(3, num.ModifierType('armor')),
                                   num.Modifier(4, num.ModifierType('ability')))
        assert total1 + total2 == num.ModifierTotal(
            num.Modifier(7),
            num.Modifier(3, num.ModifierType('armor')),
            num.Modifier(4, num.ModifierType('ability')),
        )

    def test_add_modifier_to_total(self):
        """Ensure that a modifier can be added to a modifier total."""
        total = num.ModifierTotal(num.Modifier(5),
                                  num.Modifier(2, num.ModifierType('armor')))
        modifier = num.Modifier(2)
        assert modifier + total == num.ModifierTotal(
            num.Modifier(7),
            num.Modifier(2, num.ModifierType('armor')),
        )
