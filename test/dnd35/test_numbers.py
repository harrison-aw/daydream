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
        dice_pool = numbers.NewDicePool(d6=1, d8=4)
        assert (eval(repr(dice_pool), {'NewDicePool': numbers.NewDicePool})
                == dice_pool)

    def test_equals_with_zero_counts(self):
        """Ensure that equality ignores dice with zero counts."""
        dice_pool1 = numbers.NewDicePool(d6=1, d8=4, d10=0)
        dice_pool2 = numbers.NewDicePool(d6=1, d8=4)
        assert dice_pool1 == dice_pool2

    def test_average_of_pool(self):
        """Ensure that the average of a dice pool is correct."""
        dice_pool = numbers.NewDicePool(d6=1, d8=4)
        assert dice_pool.average == 21.5

    def test_add_pools(self):
        """Ensure that two dice pools are added correctly"""
        dice_pool1 = numbers.NewDicePool(d6=1, d8=4)
        dice_pool2 = numbers.NewDicePool(d4=2, d6=2)
        assert dice_pool1 + dice_pool2 == numbers.NewDicePool(d4=2, d6=3, d8=4)

    def test_add_pool_and_die(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = numbers.NewDicePool(d6=1, d8=4)
        die = numbers.Die(6)
        assert dice_pool + die == numbers.NewDicePool(d6=2, d8=4)

    def test_add_die_and_pool(self):
        """Ensure that a single die can be added to a pool."""
        dice_pool = numbers.NewDicePool(d6=1, d8=4)
        die = numbers.Die(6)
        assert die + dice_pool == numbers.NewDicePool(d6=2, d8=4)


class TestDice:
    """Tests for the Dice class."""

    def test_create_d6(self):
        """Assert that a dice is represented correctly."""
        dice = numbers.Dice(6)
        assert str(dice) == 'd6'

    def test_create_4d8(self):
        """Create and represent a dice with multiple dice."""
        dice = numbers.Dice(8, 4)
        assert str(dice) == '4d8'

    def test_hash(self):
        """Ensure that dice are hashable."""
        dice1 = numbers.Dice(8, 4, pool=[(6, 10)])
        dice2 = numbers.Dice(pool=[(6, 10), (8, 4)])
        assert dice1 == dice2
        assert hash(dice1) == hash(dice2)

    def test_create_larger_dice_pool(self):
        """Ensure that larger dice pools can be created."""
        dice = numbers.Dice(3, None, [(6, 6), (8, 10)])
        assert str(dice) == 'd3 + 6d6 + 10d8'

    def test_repr_executes(self):
        """Ensure that the repr is accurate."""
        dice = numbers.Dice(3, None, [(6, 6)])
        new_dice = eval(repr(dice), {'Dice': numbers.Dice})
        assert dice == new_dice

    def test_add_dice_pools(self):
        """Verify that addition works as expected."""
        dice1 = numbers.Dice(3, None, [(6, 6)])
        dice2 = numbers.Dice(3, None, [(6, 6)])
        desired = numbers.Dice(pool=[(3, None), (3, None), (6, 12)])
        assert dice1 + dice2 == desired

    def test_in_place_addition(self):
        """Verify that in-place addition works as expected."""
        dice1 = numbers.Dice(3, None, [(6, 6)])
        dice2 = numbers.Dice(3, None, [(6, 6)])
        dice1 += dice2

        desired = numbers.Dice(pool=[(3, None), (3, None), (6, 12)])
        assert dice1 == desired

    def test_easy_average(self):
        """Ensure that average works correctly."""
        dice = numbers.Dice(6)
        assert dice.average == 3.5

    def test_hard_average(self):
        """Ensure that average works for complicated dice pools."""
        dice = numbers.Dice(3, None, [(6, 6), (8, 10)])
        assert dice.average == 68.0
