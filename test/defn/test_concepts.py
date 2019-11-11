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
"""Tests for the concepts module."""

import defn.concepts as concepts
import defn.core as core
import defn.numbers as num


# pylint: disable=no-self-use, eval-used


class TestSize:
    """Tests for the size class."""

    def test_repr_evaluates(self):
        """Ensure that the repr can recreate a Size instance."""
        small = concepts.Size('Small', -1)
        assert eval(repr(small), {'Size': concepts.Size}) == small

    def test_small_attack_modifier(self):
        """Ensure that the attack modifier is properly computed."""
        small = concepts.Size('Small', -1)
        assert small.attack == num.Modifier(1, concepts.Size.modifier_type)

    def test_small_armor_class(self):
        """Ensure that the armor class modifier is properly computed."""
        small = concepts.Size('Small', -1)
        assert small.armor_class == num.Modifier(1, concepts.Size.modifier_type)

    def test_small_grapple(self):
        """Ensure that the grapple modifier is properly computed."""
        small = concepts.Size('Small', -1)
        assert small.grapple == num.Modifier(-4, concepts.Size.modifier_type)

    def test_small_hide(self):
        """Ensure that the hide modifier is properly computed."""
        small = concepts.Size('Small', -1)
        assert small.hide == num.Modifier(4, concepts.Size.modifier_type)


class TestAbilityScore:
    """Tests for the ability score class."""

    def test_positive_modifier(self):
        """Ensure that the modifier is correct for high scores."""
        score = concepts.AbilityScore(17)
        assert (score.modifier
                == num.Modifier(3, concepts.AbilityScore.modifier_type))

    def test_negative_modifier(self):
        """Ensure that the modifier is correct for low scores."""
        score = concepts.AbilityScore(7)
        assert (score.modifier
                == num.Modifier(-2, concepts.AbilityScore.modifier_type))


class TestAbilityType:
    """Tests for the ability type class."""

    def test_repr_evaluates(self):
        """Ensure that the repr can be used to recreate an instance."""
        ability = concepts.AbilityType('Supernatural', 'Su')
        ability_copy = eval(repr(ability),
                            {'AbilityType': concepts.AbilityType})
        assert ability == ability_copy

    def test_str(self):
        """Ensure that the string representation is as expected."""
        ability = concepts.AbilityType('Supernatural', 'Su')
        assert str(ability) == 'Supernatural (Su)'


class TestAbility:
    """Tests for the ability class"""

    def test_static_ability(self):
        """Ensure that a feature is initialized properly."""
        stonecunning = concepts.Ability(
            'Stonecunning',
            search=num.Modifier(2,
                                num.ModifierType('racial'),
                                core.Condition('to notice unusual stonework'))
        )
        assert str(stonecunning.search) == '+2 racial bonus to notice' \
                                           ' unusual stonework'

    def test_delete_features(self):
        """Ensure that features are properly removed when deleted."""
        ability = concepts.Ability('Test', test=10)

        assert ability.test == 10
        del ability.test
        assert ability == concepts.Ability('Test')


class TestSynergy:
    """Tests for the Synergy class."""

    def test_dereference_to_2(self):
        """Ensure that the proper value is given with enough ranks."""
        synergy = concepts.Synergy('bluff')

        # pylint: disable=too-few-public-methods
        class Character:
            """Mock character used for dereferencing."""

            def __init__(self, bluff):
                self.bluff = bluff

        character = Character(10)

        assert int(synergy.dereference(character)) == 2

    def test_dereference_to_0(self):
        """Ensure that zero is returned if not enough ranks."""
        synergy = concepts.Synergy('bluff')

        # pylint: disable=too-few-public-methods
        class Character:
            """Mock character used for dereferencing."""
            def __init__(self, bluff):
                self.bluff = bluff

        character = Character(4)

        assert int(synergy.dereference(character)) == 0

    def test_dereference_in_nested_reference(self):
        """Ensure that nested references are handled correctly."""
        # pylint: disable=too-few-public-methods
        class Character(core.Aggregator):
            """Mock character used for dereferencing."""
            def __init__(self, cha, bluff, diplomacy):
                super().__init__()
                # pylint: disable=invalid-name
                self.CHA = num.Modifier(cha)
                self.bluff = num.Modifier(bluff)
                self.diplomacy = core.Reference(
                    'CHA', 'Character',
                    concepts.Synergy('bluff',
                                     modifier=num.Modifier(diplomacy)),
                )

        character = Character(3, 10, 3)

        # noinspection PyTypeChecker
        assert int(character.diplomacy) == 8

    def test_repr_evaluates(self):
        """Ensure that the repr can be evaluated."""
        synergy = concepts.Synergy('appraise', 'Character', 4,
                                   core.Condition(
                                       'on checks related to alchemy'
                                   ))

        assert synergy == eval(repr(synergy), {'Synergy': concepts.Synergy,
                                               'Condition': core.Condition})


class TestSkill:
    """Tests for the Skill class."""

    def test_ranks(self):
        """Ensure that ranks are tracked."""
        appraise = concepts.Skill('Appraise',
                                  core.Reference('INT', 'Character'))

        skill = appraise(10)

        assert skill.ranks == 10

    def test_modifier(self):
        """Ensure that the modifier accounts for references."""
        appraise = concepts.Skill('Appraise',
                                  core.Reference('INT', 'Character'))

        skill = appraise(10)

        assert skill.modifier == core.Reference('INT', 'Character',
                                                num.Modifier(10))
