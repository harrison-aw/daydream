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

import dnd35.numbers as numbers


# pylint: disable=no-self-use, eval-used


class TestDie:
    """Tests for the Die class."""

    def test_repr_evaluates(self):
        """Ensure that the repr can evaluates."""
        die = numbers.Die(6)
        assert eval(repr(die), {'Die': numbers.Die}) == die

    def test_str(self):
        """Ensure that the string representation is correct."""
        die = numbers.Die(6)
        assert str(die) == 'd6'

    def test_from_string(self):
        """Ensure that die strings are properly built."""
        die = numbers.Die.from_string('d6')
        assert die == numbers.Die(6)

    def test_string_conversion_identity(self):
        """Ensure that the strings returned and consumed work the same."""
        die = numbers.Die(6)
        die_string = 'd6'
        assert (numbers.Die.from_string(str(die)) == die
                and str(numbers.Die.from_string(die_string)) == die_string)

    def test_bad_string_prefix(self):
        """Only accept strings that start with "d"."""
        with pytest.raises(ValueError):
            numbers.Die.from_string('34')

    def test_bad_string_suffix(self):
        """Only accept strings that end with an integer."""
        with pytest.raises(ValueError):
            numbers.Die.from_string('d1.1')

    def test_hashable(self):
        """Ensure that the object is hashable."""
        die1 = numbers.Die(6)
        die2 = numbers.Die(6)
        assert die1 == die2 and hash(die1) == hash(die2)

    def test_average(self):
        """Ensure that the average is correctly computed."""
        die = numbers.Die(6)
        assert die.average == 3.5


class TestDicePool:
    """Tests for DicePool."""

    def test_repr_evaluates(self):
        """Ensure that the repr can evaluates."""
        dice_pool = numbers.DicePool(d6=1, d8=4)
        assert (eval(repr(dice_pool), {'DicePool': numbers.DicePool})
                == dice_pool)

    def test_equals_with_zero_counts(self):
        """Ensure that equality ignores dice with zero counts."""
        dice_pool1 = numbers.DicePool(d6=1, d8=4, d10=0)
        dice_pool2 = numbers.DicePool(d6=1, d8=4)
        assert dice_pool1 == dice_pool2

    def test_average_of_pool(self):
        """Ensure that the average of a dice pool is correct."""
        dice_pool = numbers.DicePool(d6=1, d8=4)
        assert dice_pool.average == 21.5

    def test_add_pools(self):
        """Ensure that two dice pools are added correctly"""
        dice_pool1 = numbers.DicePool(d6=1, d8=4)
        dice_pool2 = numbers.DicePool(d4=2, d6=2)
        assert dice_pool1 + dice_pool2 == numbers.DicePool(d4=2, d6=3, d8=4)

    def test_add_pool_and_die(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = numbers.DicePool(d6=1, d8=4)
        die = numbers.Die(6)
        assert dice_pool + die == numbers.DicePool(d6=2, d8=4)

    def test_add_die_and_pool(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = numbers.DicePool(d6=1, d8=4)
        die = numbers.Die(6)
        assert die + dice_pool == numbers.DicePool(d6=2, d8=4)


class TestModifier:
    """Tests for the Modifier class."""

    def test_repr_evaluates(self):
        mod = numbers.Modifier(4)
        namespace = {'Modifier': numbers.Modifier,
                     'ModifierType': numbers.ModifierType}
        assert eval(repr(mod), namespace) == mod
